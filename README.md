# AI Search Assistant

An intelligent, interactive, and context-aware AI search assistant built with **Elasticsearch's hybrid search** (combining semantic and keyword search) and **Google Cloud's Gemini/Vertex AI** for advanced reasoning and natural conversation.

## Features

🔍 **Hybrid Search**
- Combines semantic search (using embeddings) with traditional keyword search
- Configurable weights for semantic vs keyword relevance
- Powered by Elasticsearch with dense vector support

🤖 **AI-Powered Reasoning**
- Integration with Google's Gemini Pro for intelligent responses
- Context-aware conversations with memory
- Summarizes search results and provides comprehensive answers

💬 **Interactive Interface**
- User-friendly CLI with colored output
- Multiple modes: search, ask, chat
- Conversation history management

🎯 **Context-Aware**
- Maintains conversation context across multiple turns
- Retrieves relevant information from indexed documents
- Combines search results with conversational AI

## Architecture

```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Search Engine  │  ◄── Hybrid Search (Semantic + Keyword)
│  (Elasticsearch)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Search Results  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Gemini AI     │  ◄── Reasoning & Response Generation
│  (Google Cloud) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ AI Response     │
└─────────────────┘
```

## Installation

### Prerequisites

1. **Python 3.8+**
2. **Elasticsearch 8.0+** (optional for offline mode)
3. **Google Cloud Account** with Gemini API access

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/masterAtGithub143AtN/devpost_compition1.git
cd devpost_compition1
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Set up Elasticsearch** (optional)
```bash
# Using Docker
docker run -d \
  --name elasticsearch \
  -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  elasticsearch:8.11.0
```

5. **Get Gemini API Key**
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- Create an API key and add it to your `.env` file

## Configuration

Edit the `.env` file with your settings:

```env
# Elasticsearch Configuration
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_INDEX=search_assistant

# Google Cloud Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Search Configuration
HYBRID_SEARCH_WEIGHT_SEMANTIC=0.6  # 60% semantic search
HYBRID_SEARCH_WEIGHT_KEYWORD=0.4   # 40% keyword search
MAX_SEARCH_RESULTS=5
CONVERSATION_CONTEXT_LENGTH=5
```

## Usage

### Index Sample Data

Before using the assistant, index some sample documents:

```bash
python index_sample_data.py
```

### Start the Interactive CLI

```bash
python cli.py
```

### CLI Commands

- `/search <query>` - Perform a hybrid search
- `/ask <question>` - Ask a question with AI-powered response
- `/chat <message>` - Have a conversation (context-aware)
- `/clear` - Clear conversation history
- `/history` - Show conversation history
- `/help` - Show help message
- `/quit` or `/exit` - Exit the assistant

You can also just type your message to chat directly!

### Example Session

```
You: /search machine learning

3 search results found:

1. Understanding Machine Learning
   Score: 8.5432
   Machine Learning is a method of data analysis that automates analytical model building...

2. Introduction to Artificial Intelligence
   Score: 7.2341
   Artificial Intelligence (AI) is the simulation of human intelligence processes...

You: what is the difference between AI and machine learning?

Assistant: Based on the search results, Artificial Intelligence (AI) is a broad field that encompasses
the simulation of human intelligence processes by machines. Machine Learning is actually a subset of AI
that focuses on enabling systems to learn and improve from experience without being explicitly programmed.

In other words:
- AI is the broader concept of machines being able to carry out tasks intelligently
- Machine Learning is a specific approach to achieving AI through automated analytical model building

Think of AI as the goal (creating intelligent machines) and Machine Learning as one of the key
techniques to achieve that goal.
```

### Programmatic Usage

You can also use the assistant programmatically:

```python
from search_assistant import AISearchAssistant

# Initialize
assistant = AISearchAssistant()

# Perform search
results = assistant.search("python programming", max_results=5)

# Ask a question
response = assistant.ask("How do I learn machine learning?")
print(response["response"])

# Chat
reply = assistant.chat("Tell me more about that")
print(reply)
```

See `example.py` for a complete working example.

## How It Works

### Hybrid Search

The system combines two search methods:

1. **Semantic Search**: Uses sentence transformers to create embeddings and find semantically similar documents
2. **Keyword Search**: Traditional full-text search using Elasticsearch's BM25 algorithm

Results from both methods are combined with configurable weights (default: 60% semantic, 40% keyword).

### AI Reasoning

Google's Gemini AI processes search results and generates intelligent responses by:

1. Receiving the user's query
2. Getting relevant search results as context
3. Analyzing the information
4. Generating a comprehensive, helpful response
5. Maintaining conversation context for follow-up questions

## Project Structure

```
devpost_compition1/
├── config.py                 # Configuration management
├── elasticsearch_client.py   # Elasticsearch hybrid search
├── gemini_client.py          # Google Gemini AI integration
├── search_assistant.py       # Main assistant logic
├── cli.py                    # Interactive CLI interface
├── index_sample_data.py      # Sample data indexing
├── example.py                # Usage examples
├── requirements.txt          # Python dependencies
├── .env.example              # Example environment config
├── .gitignore                # Git ignore patterns
└── README.md                 # This file
```

## Key Technologies

- **Elasticsearch 8.0+**: Distributed search engine with vector search support
- **sentence-transformers**: For generating semantic embeddings
- **Google Gemini Pro**: Advanced AI model for reasoning and conversation
- **Python 3.8+**: Core programming language
- **colorama**: Colored terminal output

## Features in Detail

### Hybrid Search
- Combines keyword and semantic search for better accuracy
- Adjustable weights for different use cases
- Fast and scalable with Elasticsearch

### Context-Aware Conversations
- Maintains conversation history
- References previous messages
- Provides coherent multi-turn dialogues

### Intelligent Responses
- Summarizes multiple search results
- Answers questions based on indexed knowledge
- Admits when information is insufficient
- Provides helpful, accurate information

## Troubleshooting

### Elasticsearch Connection Failed
- Ensure Elasticsearch is running: `curl http://localhost:9200`
- Check credentials in `.env` file
- Verify network connectivity

### Gemini API Errors
- Verify your API key is correct
- Check API quotas and limits
- Ensure you have internet connectivity

### No Search Results
- Index sample data first: `python index_sample_data.py`
- Verify index creation: Check Elasticsearch logs
- Try different search queries

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for the Elastic + Google Cloud DevPost Competition
- Powered by Elasticsearch and Google Gemini
- Thanks to the open-source community

## Future Enhancements

- [ ] Web interface (Flask/FastAPI)
- [ ] Multi-modal search (images, audio)
- [ ] Advanced filtering and faceting
- [ ] User authentication and personalization
- [ ] Real-time collaboration features
- [ ] Integration with more data sources
- [ ] Performance monitoring and analytics
