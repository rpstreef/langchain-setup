import os

from fastapi import FastAPI
from langserve import add_routes

# Step 1
from langchain_community.document_loaders import WebBaseLoader

# Step 2, 3, 4
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

# Step 5
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Step 6
from langchain.chains import RetrievalQAWithSourcesChain

# Load environment variables
openai_api_key = os.environ.get("OPENAI_API_KEY")

app = FastAPI(
    title="LangFlow Example Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

# Step 1, load website
loader = WebBaseLoader("https://www.espn.com/")
documents = loader.load()

# Step 2, split text and load the embeddings into OpenAI
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(model_name="gpt-3.5-turbo-0125", chunk_size=1000, chunk_overlap=200, separator='\n')
docs = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Step 3, load the document into FAIS with OpenAI embeddings
db = FAISS.from_documents(docs, embeddings)

# Step 5, 
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

llm = ChatOpenAI(
    model="gpt-3.5-turbo-0125",
    temperature=0.9
)
combine_docs_chain = create_stuff_documents_chain(llm, prompt)

# Step 6
chain = RetrievalQAWithSourcesChain.from_chain_type(
    combine_docs_chain, 
    chain_type="stuff",
    retriever=db.as_retriever()
)

# Add the flow to the app
add_routes(
    app,
    chain,
    path="/langflow",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=7800)