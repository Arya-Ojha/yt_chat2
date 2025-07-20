
# AI-Powered YouTube Q&A Chrome Extension 🚀

This repository contains the complete source code for a Chrome extension that allows you to ask questions about any YouTube video and get intelligent, AI-powered answers directly in your browser.

The project is a full-stack application consisting of:
1.  A **Chrome Extension Frontend** (the user interface).
2.  A **FastAPI Backend** that handles the AI processing using LangChain and Google Gemini.

## ✨ Features

- **In-Browser Q&A:** Ask questions about the current YouTube video without leaving the page.
- **Intelligent Answers:** The extension doesn't just search for keywords; it understands the context of the video's transcript to provide relevant answers.
- **Powered by RAG:** Uses a state-of-the-art Retrieval-Augmented Generation (RAG) pipeline for high accuracy.
- **Full-Stack Architecture:** Demonstrates a real-world application of a browser extension communicating with a powerful AI backend.

## ⚙️ Project Architecture

This project operates in two main parts that work together seamlessly:

1.  **Chrome Extension (Frontend):**
    - The user interface that appears in the browser.
    - When you're on a YouTube video page, it grabs the `video_id` and your question.
    - It then sends this information via an API request to the FastAPI backend server.

2.  **FastAPI Server (Backend):**
    - This is the "brain" of the extension, running from the `main.py` file. It receives the request from the frontend.
    - It fetches the video transcript, chunks the text, and creates a searchable `FAISS` vector store.
    - It uses this store to retrieve the most relevant context for your question.
    - It generates a final answer using Google's Gemini model and sends it back to the extension.

3.  **Display:** The Chrome extension receives the answer from the backend and displays it to you in the UI.

## 🛠️ Setup and Installation

To get this project running, you need to set up both the backend server and the frontend extension.

### Part 1: Backend Server Setup

1.  **Open Your Project Directory:**
    Open a terminal in the root directory of the project (the same folder where `main.py` is located).

2.  **Create and Activate a Virtual Environment:**
    ```bash
    # For Unix/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    Install all the required packages using the `requirements.txt` file included in the project.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**
    Create a `.env` file in the root directory and add your Google API key.
    ```
    GOOGLE_API_KEY="your_google_api_key_here"
    ```

5.  **Run the Backend Server:**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```
    Leave this terminal running. The backend is now active at `http://localhost:8000`.

### Part 2: Frontend Extension Setup

1.  **Open Google Chrome:** Navigate to `chrome://extensions`.
2.  **Enable Developer Mode:** Find the "Developer mode" toggle in the top-right corner and switch it on.
3.  **Load the Extension:**
    - Click the "**Load unpacked**" button.
    - A file dialog will open. Navigate to and select the folder that contains your extension's frontend files (the one with `manifest.json`, e.g., an `extension` or `frontend` subfolder).

The extension icon should now appear in your browser's toolbar.

## 🚀 How to Use

1.  Make sure your backend server is running.
2.  Ensure the Chrome extension is loaded and enabled in your browser.
3.  Navigate to any YouTube video that has an English transcript.
4.  Click on the extension's icon in your toolbar.
5.  Type your question into the input field and submit.
6.  The AI-generated answer will appear in the extension's popup.

## 💻 Technologies Used

- **Frontend:** HTML, CSS, JavaScript, Chrome Extension APIs
- **Backend:** FastAPI, Python
- **AI/ML:** LangChain, Google Gemini (`gemini-1.5-flash`)
- **Vector Store:** FAISS
- **Embeddings:** Hugging Face Sentence Transformers
