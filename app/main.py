import os

from typing import List, Union, Optional
from fastapi import FastAPI
from langserve import add_routes

from langchain import hub


# this is crucial to avoid the typing errors!
from langchain_core.pydantic_v1 import BaseModel, Field

# Step 1
from langchain_community.document_loaders import WebBaseLoader

# Step 2, 3, 4
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

# Step 5
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain.schema.runnable import RunnablePassthrough

# Step 6
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.memory import ConversationBufferMemory

from langchain.schema import SystemMessage, HumanMessage, AIMessage, BaseMessage, StrOutputParser


# Load environment variables
openai_api_key = os.environ.get("OPENAI_API_KEY")

app = FastAPI(
    title="LangFlow Example Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

# Step 1, load website
# text_splitter = CharacterTextSplitter.from_tiktoken_encoder(model_name="gpt-3.5-turbo-0125", chunk_size=1000, chunk_overlap=200, separator='\n')

loader = WebBaseLoader(
    web_paths=("https://rolfstreefkerk.com/posts/a-holistic-approach-to-health-and-weight-tracking/",),
    # bs_kwargs=dict(
    #     parse_only=bs4.SoupStrainer(
    #         class_=("post-content", "post-title", "post-header")
    #     )
    # ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.9, streaming=True)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | lambda x: format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Add the flow to the app
add_routes(
    app,
    rag_chain,
    path="/langflow",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=7800)