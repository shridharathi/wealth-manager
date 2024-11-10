import json
import pickle
import re

from fastapi import FastAPI, APIRouter
from app.services import openai_service, pinecone_service, polygon_service
from app.utils.helper_functions import chunk_text, build_prompt
from app.services.openai_service import determine_query_type


app = FastAPI(title="RAG-LLM-app")
router = APIRouter()

PINECONE_INDEX_NAME = "rag-llm-app"

@router.post('/embed-and-store')
def embed_and_store():
    text = ""
    with open('knowledge.txt', 'r') as f:
        text = f.read()
    chunks = chunk_text(text)
    pinecone_service.embed_chunks_and_upload_to_pinecone(chunks, PINECONE_INDEX_NAME)
    response_json = {
        "message": "Ready! Ask away:"
    }
    return response_json


@router.post('/handle-query')
def handle_query(question):
    #question = request.json['question']
        
    context = pinecone_service.get_most_similar_chunks_for_query(question, PINECONE_INDEX_NAME)
    query_type = determine_query_type(question)
    if query_type != "general":
        if query_type == "schedule":
            answer = "You can schedule an in-person consult at this link: https://calendly.com/shridharathinarayanan/30min"
            return answer
        stock_data = polygon_service.get_stock_data(query_type)
        context.append(stock_data)
    prompt = build_prompt(question, context)
    print(f"Prompt: {prompt}")
    answer = openai_service.get_llm_answer(prompt)
    answer = re.sub(r'["\n$]', '', answer)
    print(f"Response: {answer}")
    return answer  


@router.post('/delete-index')
def delete_index():
    pinecone_service.delete_index()
    return {"message": f"Indexes deleted successfully"}

app.include_router(router)

if __name__ == "__main__":
    import uvicorn  # pylint: disable=import-outside-toplevel
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=1,
        use_colors=True,
    )
    