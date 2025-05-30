# Insurance Plan RAG Chatbot

A chatbot that uses Retrieval-Augmented Generation (RAG) to answer questions about insurance plans and benefits.

## Features

- Real-time chat interface with AI
- Document-based responses using RAG
- Support for multiple insurance plan documents
- Modern UI with Next.js and Tailwind CSS

## Tech Stack

### Backend

- FastAPI
- LangChain
- ChromaDB for vector storage
- OpenAI for embeddings and chat

### Frontend

- Next.js 14
- TypeScript
- Tailwind CSS
- Lucide React for icons

## Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- OpenAI API key

### Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up your environment variables:

```bash
export OPENAI_API_KEY=your_api_key_here
```

5. Run the server:

```bash
python -m uvicorn app.main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Run the development server:

```bash
npm run dev
```

## Usage

1. Place your insurance plan documents in `backend/app/rag/docs/`
2. The system will automatically process and index the documents
3. Access the chat interface at `http://localhost:3000`
4. Start asking questions about insurance plans and benefits

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── rag/
│   │   │   ├── docs/          # Insurance plan documents
│   │   │   │   └── __init__.py
│   │   └── main.py           # FastAPI application
│   └── requirements.txt
└── frontend/
    ├── app/
    │   ├── components/
    │   │   └── Chat.tsx      # Chat interface
    │   ├── layout.tsx
    │   └── page.tsx
    ├── package.json
    └── tailwind.config.ts
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
