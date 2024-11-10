#import pinecone as pc
from pinecone import Pinecone, PodSpec, ServerlessSpec
from app.services.openai_service import get_embedding
import os

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

# make sure to enter your actual Pinecone environment

pc = Pinecone(api_key=PINECONE_API_KEY, environment='gcp-starter')
#pc.init(api_key=PINECONE_API_KEY, environment='gcp-starter')

EMBEDDING_DIMENSION = 1536

def delete_index():
   for index in pc.list_indexes():
      pc.delete_index(name=index['name'])

def embed_chunks_and_upload_to_pinecone(chunks, index_name):

    # delete the index if it already exists. 
    # as Pinecone's free plan only allows one index
    for index in pc.list_indexes():
        pc.delete_index(name=index['name'])
    # create a new index in Pinecone
    # the EMBEDDING_DIMENSION is based on what the
    # OpenAI embedding model outputs
    pc.create_index(name=index_name,
                    dimension=EMBEDDING_DIMENSION, 
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    ))
    index = pc.Index(index_name)
    # embed each chunk and aggregate these embeddings
    embeddings_with_ids = []
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        embeddings_with_ids.append((str(i), embedding, chunk))
    # upload the embeddings and relevant texts for each chunk
    # to the Pinecone index
    upserts = [(id, vec, {"chunk_text": text}) for id, vec, text in embeddings_with_ids]
    index.upsert(vectors=upserts)


def get_most_similar_chunks_for_query(query, index_name):
    question_embedding = get_embedding(query)
    index = pc.Index(index_name)
    query_results = index.query(vector=question_embedding, top_k=3, include_metadata=True)
    context_chunks = [x['metadata']['chunk_text'] for x in query_results['matches']]
    return context_chunks
