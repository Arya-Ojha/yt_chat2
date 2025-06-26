from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow frontend access (like from Chrome Extension)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can later restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Input Schema ===
class Query(BaseModel):
    video_id: str
    question: str

# === Route ===
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

    # Split transcript
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])

    # Embed & store
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vector_store = FAISS.from_documents(chunks, embeddings)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={'k': 4})

    # Prompt
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    prompt = PromptTemplate(
        template="""
        You are a helpful assistant.
        Answer ONLY from the provided transcript context.
        If the context is insufficient, say you don't know.

        {context}
        Question: {question}
        """,
        input_variables=["context", "question"]
    )

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    parser = StrOutputParser()
    
    parallel_chain = RunnableParallel({
    'context': retriever| RunnableLambda(format_docs),
    'question': RunnablePassthrough()
})
    
    main_chain = parallel_chain | prompt | llm | parser

    chain = (
        RunnableParallel({
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }) | prompt | llm | parser
    )

    try:
        answer = main_chain.invoke({"question": question})
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Error during LLM invocation: {str(e)}"}
