import { AstraDB } from "@datastax/astra-db-ts";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
import 'dotenv/config'
import sampleData from './sample_data.json';
import OpenAI from 'openai';
import { SimilarityMetric } from "../app/hooks/useConfiguration";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL:process.env.BASE_URL
});

const { ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_API_ENDPOINT, ASTRA_DB_NAMESPACE } = process.env;

const astraDb = new AstraDB(ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_API_ENDPOINT, ASTRA_DB_NAMESPACE);

const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,
  chunkOverlap: 200,
});

const similarityMetrics: SimilarityMetric[] = [
  'cosine',
  'euclidean',
  'dot_product',
]

const createCollection = async (similarity_metric: SimilarityMetric = 'cosine') => {
  try {
    const res = await astraDb.createCollection(`chat_${similarity_metric}`, {
      vector: {
        dimension: 1536,
        metric: similarity_metric,
      }
    });
    console.log(res);
  } catch (e) {
    console.log(`chat_${similarity_metric} already exists or error:`, e);
  }
};

const loadSampleData = async (similarity_metric: SimilarityMetric = 'cosine') => {
  const collection = await astraDb.collection(`chat_${similarity_metric}`);
  for await (const { url, title, content } of sampleData) {
    const chunks = await splitter.splitText(content);
    let i = 0;
    for await (const chunk of chunks) {
      try {
        const response = await openai.embeddings.create({ input: chunk, model: 'text-embedding-ada-002' });
        const data = response.data;
        
        if (!data || !data[0] || !data[0].embedding) {
          console.error('Invalid response from OpenAI embeddings:', response);
          continue;
        }

        const res = await collection.insertOne({
          document_id: `${url}-${i}`,
          $vector: data[0].embedding,
          url,
          title,
          content: chunk
        });
        console.log(`Inserted document ${url}-${i}`);
        i++;
      } catch (e) {
        console.error(`Error processing chunk ${i} of ${url}:`, e);
      }
    }
  }
  console.log('data loaded');
};

similarityMetrics.forEach(metric => {
  createCollection(metric).then(() => loadSampleData(metric));
});
