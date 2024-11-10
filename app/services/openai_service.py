import requests
import json
import os
from openai import OpenAI
#from app.utils.helper_functions import construct_messages_list, build_prompt

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
#openai_client = OpenAI(api_key=OPENAI_API_KEY)

OPENAI_EMBEDDING_MODEL = 'text-embedding-ada-002'
PROMPT_LIMIT = 3750
CHATGPT_MODEL = 'gpt-4-1106-preview'

def get_embedding(chunk):
  url = 'https://api.openai.com/v1/embeddings'
  headers = {
      'content-type': 'application/json; charset=utf-8',
      'Authorization': f"Bearer {OPENAI_API_KEY}"            
  }
  data = {
      'model': OPENAI_EMBEDDING_MODEL,
      'input': chunk
  }
  response = requests.post(url, headers=headers, data=json.dumps(data))  
  response_json = response.json()
  embedding = response_json["data"][0]["embedding"]
  # response = openai_client.embeddings.create(
  #     input=chunk, model=OPENAI_EMBEDDING_MODEL)
  # embedding = response.data[0].embedding
  return embedding


def determine_query_type(query):

  messages = [{"role": "system", "content": "You are a helpful assistant."}]
  prompt = f"There are three types of queries: general, stock, and schedule. A stock query is if the user asks for the stock price of a company. A schedule query is if the user wants to schedule a meeting. All other queries are general. If the following query is a stock query, respond ONLY with the ticker symbol of the company (i.e. 'AAPL' for Apple). If the query is schedule, respond with 'schedule'. If the query is general, respond with 'general'. \n Query: {query}"
  messages.append({"role": "user", "content": prompt})
  # Send the payload to the LLM to retrieve an answer
  url = 'https://api.openai.com/v1/chat/completions'
  headers = {
      'content-type': 'application/json; charset=utf-8',
      'Authorization': f"Bearer {OPENAI_API_KEY}"            
  }
  data = {
      'model': CHATGPT_MODEL,
      'messages': messages,
      'temperature': 1, 
      'max_tokens': 1000
  }
  response = requests.post(url, headers=headers, data=json.dumps(data))
  
  # return the final answer
  response_json = response.json()
  completion = response_json["choices"][0]["message"]["content"]
  completion.replace("\n", "")
  return completion

def get_llm_answer(prompt):

  messages = [{"role": "system", "content": "You are a helpful, accomplished, professional wealth manager who can help people with investment management and financial planning."}]
  messages.append({"role": "user", "content": prompt})
  # Send the payload to the LLM to retrieve an answer
  url = 'https://api.openai.com/v1/chat/completions'
  headers = {
      'content-type': 'application/json; charset=utf-8',
      'Authorization': f"Bearer {OPENAI_API_KEY}"            
  }
  data = {
      'model': CHATGPT_MODEL,
      'messages': messages,
      'temperature': 1, 
      'max_tokens': 1000
  }
  response = requests.post(url, headers=headers, data=json.dumps(data))
  
  # return the final answer
  response_json = response.json()
  completion = response_json["choices"][0]["message"]["content"]
  completion.replace("\n", "")
  return completion
