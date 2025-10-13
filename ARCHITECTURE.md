# Architecture Documentation

## System Architecture

The AI Search Assistant is built on a modular architecture that combines Elasticsearch's hybrid search capabilities with Google Gemini's advanced AI reasoning.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│                        (CLI / API)                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI Search Assistant                          │
│                  (search_assistant.py)                          │
│                                                                 │
│  ┌──────────────────────┐     ┌──────────────────────┐        │
│  │ Conversation Manager │     │   Query Processor    │        │
│  └──────────────────────┘     └──────────────────────┘        │
└──────────┬─────────────────────────────────┬──────────────────┘
           │                                  │
           │                                  │
    ┌──────▼──────┐                    ┌─────▼──────┐
    │   Gemini    │                    │Elasticsearch│
    │  AI Client  │                    │   Client    │
    │             │                    │             │
    │ - Reasoning │                    │ - Keyword   │
    │ - Chat      │                    │ - Semantic  │
    │ - Summarize │                    │ - Hybrid    │
    └──────┬──────┘                    └─────┬──────┘
           │                                  │
           │                                  │
    ┌──────▼──────┐                    ┌─────▼──────┐
    │   Google    │                    │Elasticsearch│
    │   Gemini    │                    │   Server   │
    │     API     │                    │             │
    └─────────────┘                    └────────────┘
```

## Component Details

### 1. Configuration Layer (`config.py`)

**Purpose**: Centralized configuration management

**Key Features**:
- Environment variable loading
- Default values
- Configuration validation
- Type conversion

**Configuration Options**:
- Elasticsearch connection settings
- Google Cloud credentials
- Search weights (semantic vs keyword)
- Conversation parameters

### 2. Elasticsearch Client (`elasticsearch_client.py`)

**Purpose**: Manage hybrid search operations

**Key Features**:
- **Semantic Search**: Uses sentence transformers to create embeddings
- **Keyword Search**: Traditional BM25-based text matching
- **Hybrid Scoring**: Combines both methods with configurable weights
- **Index Management**: Create, update, and manage indices
- **Document Indexing**: Store documents with embeddings

**Hybrid Search Formula**:
```
final_score = (semantic_score * semantic_weight) + (keyword_score * keyword_weight)
```

**Vector Embeddings**:
- Model: `all-MiniLM-L6-v2` (384 dimensions)
- Similarity: Cosine similarity
- Storage: Elasticsearch dense_vector type

### 3. Gemini AI Client (`gemini_client.py`)

**Purpose**: Interface with Google's Gemini AI

**Key Features**:
- **Response Generation**: Create intelligent answers from search results
- **Conversation**: Maintain context across multiple turns
- **Summarization**: Condense search results into digestible summaries
- **Fallback Mode**: Graceful degradation when API is unavailable

**Prompt Engineering**:
```
System Role: Intelligent search assistant
Context: Search results from Elasticsearch
User Query: Original question
History: Previous conversation turns
```

### 4. AI Search Assistant (`search_assistant.py`)

**Purpose**: Orchestrate the entire search and reasoning pipeline

**Key Features**:
- **Unified Interface**: Single entry point for all operations
- **Context Management**: Track conversation history
- **Result Fusion**: Combine search and AI reasoning
- **Mode Selection**: Search-only, AI-only, or hybrid modes

**Workflow**:
1. Receive user query
2. Perform hybrid search (if enabled)
3. Summarize search results
4. Generate AI response with context
5. Update conversation history
6. Return comprehensive response

### 5. CLI Interface (`cli.py`)

**Purpose**: Interactive command-line interface

**Features**:
- Colored output for better UX
- Multiple command modes (/search, /ask, /chat)
- Conversation history viewing
- Help system
- Error handling and graceful degradation

## Data Flow

### Search Query Flow

```
User Query
    │
    ▼
Parse Query
    │
    ├─────────────────┬────────────────┐
    │                 │                │
    ▼                 ▼                ▼
Keyword Search   Semantic Search   Query Expansion
    │                 │                │
    │                 │                │
    ▼                 ▼                │
Score: BM25      Score: Cosine        │
    │                 │                │
    └────────┬────────┘                │
             ▼                         │
      Hybrid Score ◄──────────────────┘
             │
             ▼
      Ranked Results
             │
             ▼
      Result Summary
             │
             ▼
    Gemini AI Processing
             │
             ▼
     Final Response
```

### Conversation Flow

```
User Message
    │
    ▼
Retrieve Context
    │
    ├── Conversation History (last 5 turns)
    │
    └── Search Results (top 3)
    │
    ▼
Build Prompt
    │
    ▼
Gemini Generate
    │
    ▼
Update History
    │
    ▼
Return Response
```

## Storage and Indexing

### Elasticsearch Document Structure

```json
{
  "title": "Document Title",
  "content": "Full document text content...",
  "embedding": [0.123, -0.456, ...],  // 384-dimensional vector
  "metadata": {
    "category": "AI",
    "author": "Author Name",
    "date": "2024-01-01"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Index Mapping

```json
{
  "mappings": {
    "properties": {
      "title": {"type": "text"},
      "content": {"type": "text"},
      "embedding": {
        "type": "dense_vector",
        "dims": 384,
        "index": true,
        "similarity": "cosine"
      },
      "metadata": {"type": "object"},
      "timestamp": {"type": "date"}
    }
  }
}
```

## Performance Considerations

### Search Performance

- **Elasticsearch Indexing**: O(log n) for insertion
- **Keyword Search**: O(log n) using inverted index
- **Semantic Search**: O(n) for vector similarity (optimized with approximate algorithms)
- **Hybrid Combination**: O(n) linear combination

### Optimization Strategies

1. **Approximate Vector Search**: Use Elasticsearch's HNSW algorithm
2. **Result Caching**: Cache frequent queries
3. **Batch Processing**: Index documents in batches
4. **Connection Pooling**: Reuse Elasticsearch connections

### Scalability

- **Horizontal Scaling**: Elasticsearch cluster with multiple nodes
- **Vertical Scaling**: Increase resources for AI API calls
- **Load Balancing**: Distribute queries across replicas
- **Sharding**: Partition large indices

## Security

### API Key Management

- Store in environment variables (.env)
- Never commit to version control
- Rotate keys regularly
- Use service accounts with minimal permissions

### Data Protection

- Encrypt data in transit (HTTPS)
- Encrypt sensitive data at rest
- Implement access controls
- Audit logging

## Error Handling

### Graceful Degradation

1. **Elasticsearch Unavailable**: Fall back to AI-only mode
2. **Gemini API Error**: Return search results with simple summary
3. **Network Issues**: Retry with exponential backoff
4. **Invalid Input**: Validate and sanitize user input

### Logging

- INFO: Normal operations
- WARNING: Degraded functionality
- ERROR: Failed operations with context
- DEBUG: Detailed execution flow

## Future Enhancements

### Planned Features

1. **Multi-Modal Search**: Images, audio, video
2. **Query Expansion**: Automatic synonym and related term expansion
3. **Personalization**: User-specific result ranking
4. **Analytics**: Search quality metrics and user behavior
5. **Real-Time Updates**: Streaming results as they're found
6. **Advanced Filtering**: Faceted search, date ranges, categories
7. **A/B Testing**: Experiment with different search weights
8. **Caching Layer**: Redis for frequently accessed results

### API Design (Future)

```
POST /api/v1/search
POST /api/v1/ask
POST /api/v1/chat
GET  /api/v1/history
DELETE /api/v1/history
POST /api/v1/index
```

## Technology Stack

- **Python 3.8+**: Core language
- **Elasticsearch 8.0+**: Search engine with vector support
- **sentence-transformers**: Embedding generation
- **Google Gemini API**: AI reasoning and generation
- **python-dotenv**: Environment management
- **colorama**: Terminal colors
- **numpy**: Numerical operations

## Development Guidelines

### Code Style

- Follow PEP 8
- Use type hints
- Document all public methods
- Write descriptive variable names

### Testing

- Unit tests for individual components
- Integration tests for workflows
- Mock external dependencies
- Aim for >80% code coverage

### Deployment

- Use virtual environments
- Pin dependency versions
- Document deployment steps
- Implement health checks
