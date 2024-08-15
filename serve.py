from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the Groq model with API key
groq_api_key = os.getenv("GROQ_API_KEY")
model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# Set up output parser
parser = StrOutputParser()

# Create translation chain
chain = prompt_template | model | parser

# Initialize FastAPI app
app = FastAPI(title="Langchain Server",
              version="1.0",
              description="A simple API server using Langchain runnable interfaces")

# Add chain routes to the FastAPI app
add_routes(
    app,
    chain,
    path="/chain"
)

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
