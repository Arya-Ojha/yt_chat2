from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

port = int(os.environ.get("PORT", 10000))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    video_id: str
    question: str

@app.post("/ask")
def ask(query: Query):
    video_id = query.video_id
    question = query.question

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript = " ".join(chunk['text'] for chunk in transcript_list)
    except TranscriptsDisabled:
        return {"answer": "Transcript is not available for this video."}
    except Exception as e:
        return {"answer": f"Error fetching transcript: {str(e)}"}
    
    

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks, embeddings)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={'k': 4})

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    prompt = PromptTemplate(
        template="""
        You are a helpful assistant.
        Answer ONLY from the provided transcript context.
        If the context is insufficient, say you don't know.

        {cexontt}
        Question: {question}
        """,
        input_variables=["context", "question"]
    )

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    parser = StrOutputParser()

    try:
        docs = retriever.get_relevant_documents(question)
        context = format_docs(docs)
        prompt_input = {"context": context, "question": question}
        answer = llm.invoke(prompt.format(**prompt_input))
        answer = parser.invoke(answer)
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Error during LLM invocation: {str(e)}"}
    



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)