# Wealth Manager Chatbot

Ask questions about how to manage your wealth and investment information.

This chatbot is seeded with JP Morgan's Guide to Mutual Fund Investing and Preparing for retirement documents, as well as other text on saving strategies for different income levels and plans for high income individuals. Additionally, you can inquire on most updated live stock prices of companies or ask to schedule a live appointment with a human advisor.

Specifically, queries you might find helpful to use as a test suite are:

What should I consider when investing in mutual funds?
How can I diversify my investment portfolio?
What factors should I evaluate before investing in high-yield bonds?
How can real estate contribute to a diversified investment strategy?
What's the advantage of investing in non traditional funds?
What are the risks and benefits of investing in international stock markets?
I'm 45 years old, earn $150,000 a year, and have $500,000 in my retirement account. Is this sufficient for a comfortable retirement?
I'm 30, earn $100k, and just started saving for retirement. How much should I aim to save each year?
I'm 52, make 130k, and have 300k saved for retirement. Am I on the right track?
What is Nvidia currently selling at?
What is the current price of Amazon stock?
If I purchased shares of SMCI at $1090 each, is it a good time to sell them now?
Should I sell Microsoft now if I bought it at 86 a share?
Should I hold on to Tesla shares bought at $400 given the current market volatility?

About the tech:
This chatbot uses a FastAPI backend and Streamlit frontend. To respond to queries, it pulls from a knowledge base ("knowledge.txt" which you can add more text to if needed) to find context most relevant to the query and provide a precise answer (RAG). This is done by creating context chunks from the knowledge base, embedding them with OpenAI, storing them in a Pinecone vector database, and using Pinecone's cosine similarity to find the most relevant context to the query. This chatbot also taps into Polygon for real-time ticker prices and connects users to Calendly to set up in-person appointments.

Question 4:
To handle the virality of the chatbot, the first thing to address is that there will be an exponential increase in user requests to the service APIs used; I would employ load balancing for traffic management. Additionally, if this chatbot becomes viral at a global scale, content delivery networks (like AWS CloudFront) would be useful not only for more efficient responses, but also to cache financial information relevant to the user's nation in the knowledge base. To support multi-tenancy, users of similar income groups or with similar involvements can access deployments of chatbots with one common knowledge base to reduce storage. Since we are dealing with sensitive financial information, information should be encrypted in transit to prevent interception and any PII of clients stored in context or knowledge base for a client's deployment of the chatbot should be redacted or deleted every 45 days to comply with GDPR regulations.

Setup:

Create .env file in root directory

`OPENAI_API_KEY=<YOUR_API_KEY>`

`PINECONE_API_KEY=<YOUR_API_KEY>`

`POLYGON_API_KEY=<YOUR_API_KEY>`

Create Virtual Environment

`python3 -m venv venv`

`source venv/bin/activate`

Install Python dependencies

`pip install -r requirements.txt`

Launch Backend Server

`uvicorn run:app --host 0.0.0.0 --port 8000 --reload`

Launch Frontend Webpage

`streamlit run webpage.py`

Hit the "Boot me up" button to chunk, embed, and store the knowledge base. Then, you can submit your questions.
