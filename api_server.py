"""
Simple Flask API server for the AI Search Assistant.
This provides a RESTful API interface to the search assistant.

Usage:
    pip install flask flask-cors
    python api_server.py
    
Then access:
    http://localhost:5000/api/health
    http://localhost:5000/api/search?q=machine+learning
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from search_assistant import AISearchAssistant
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize search assistant
try:
    assistant = AISearchAssistant()
    logger.info("Search assistant initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize search assistant: {e}")
    assistant = None


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    if assistant:
        return jsonify({
            'status': 'healthy',
            'message': 'AI Search Assistant is running'
        }), 200
    else:
        return jsonify({
            'status': 'unhealthy',
            'message': 'Search assistant not initialized'
        }), 503


@app.route('/api/search', methods=['GET', 'POST'])
def search():
    """
    Search endpoint.
    
    GET: /api/search?q=query&max_results=5
    POST: /api/search with JSON body {"query": "...", "max_results": 5}
    """
    if not assistant:
        return jsonify({'error': 'Service unavailable'}), 503
    
    try:
        # Get query from GET or POST
        if request.method == 'GET':
            query = request.args.get('q', '')
            max_results = int(request.args.get('max_results', 5))
        else:
            data = request.get_json()
            query = data.get('query', '')
            max_results = data.get('max_results', 5)
        
        if not query:
            return jsonify({'error': 'Query parameter required'}), 400
        
        # Perform search
        results = assistant.search(query, max_results=max_results)
        
        return jsonify({
            'query': query,
            'results': results,
            'count': len(results)
        }), 200
    
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/ask', methods=['POST'])
def ask():
    """
    Ask a question endpoint.
    
    POST: /api/ask with JSON body {"question": "...", "use_search": true}
    """
    if not assistant:
        return jsonify({'error': 'Service unavailable'}), 503
    
    try:
        data = request.get_json()
        question = data.get('question', '')
        use_search = data.get('use_search', True)
        
        if not question:
            return jsonify({'error': 'Question parameter required'}), 400
        
        # Ask question
        result = assistant.ask(question, use_search=use_search)
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Ask error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat endpoint for conversational interaction.
    
    POST: /api/chat with JSON body {"message": "..."}
    """
    if not assistant:
        return jsonify({'error': 'Service unavailable'}), 503
    
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message parameter required'}), 400
        
        # Chat
        response = assistant.chat(message)
        
        return jsonify({
            'message': message,
            'response': response
        }), 200
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/history', methods=['GET', 'DELETE'])
def history():
    """
    Conversation history endpoint.
    
    GET: Get conversation history
    DELETE: Clear conversation history
    """
    if not assistant:
        return jsonify({'error': 'Service unavailable'}), 503
    
    try:
        if request.method == 'GET':
            history_data = assistant.get_conversation_history()
            return jsonify({
                'history': history_data,
                'count': len(history_data)
            }), 200
        
        elif request.method == 'DELETE':
            assistant.clear_conversation()
            return jsonify({'message': 'History cleared'}), 200
    
    except Exception as e:
        logger.error(f"History error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/index', methods=['POST'])
def index_document():
    """
    Index a document endpoint.
    
    POST: /api/index with JSON body:
    {
        "id": "doc1",
        "title": "Document Title",
        "content": "Document content...",
        "metadata": {"key": "value"}
    }
    """
    if not assistant:
        return jsonify({'error': 'Service unavailable'}), 503
    
    try:
        data = request.get_json()
        doc_id = data.get('id')
        title = data.get('title', '')
        content = data.get('content', '')
        metadata = data.get('metadata', {})
        
        if not all([doc_id, title, content]):
            return jsonify({'error': 'id, title, and content required'}), 400
        
        # Index document
        success = assistant.index_document(doc_id, title, content, metadata)
        
        if success:
            return jsonify({
                'message': 'Document indexed successfully',
                'id': doc_id
            }), 201
        else:
            return jsonify({'error': 'Failed to index document'}), 500
    
    except Exception as e:
        logger.error(f"Index error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/')
def index():
    """Root endpoint with API documentation."""
    return jsonify({
        'name': 'AI Search Assistant API',
        'version': '1.0.0',
        'endpoints': {
            'GET /api/health': 'Health check',
            'GET /api/search': 'Search with query parameter ?q=query',
            'POST /api/search': 'Search with JSON body',
            'POST /api/ask': 'Ask a question',
            'POST /api/chat': 'Chat conversation',
            'GET /api/history': 'Get conversation history',
            'DELETE /api/history': 'Clear conversation history',
            'POST /api/index': 'Index a document'
        },
        'documentation': 'See README.md for full documentation'
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


def main():
    """Run the API server."""
    print("=" * 70)
    print("  AI Search Assistant API Server")
    print("=" * 70)
    print()
    print("Starting server...")
    print("API will be available at: http://localhost:5000")
    print()
    print("Endpoints:")
    print("  GET  /api/health      - Health check")
    print("  GET  /api/search      - Search")
    print("  POST /api/ask         - Ask question")
    print("  POST /api/chat        - Chat")
    print("  GET  /api/history     - Get history")
    print("  DELETE /api/history   - Clear history")
    print("  POST /api/index       - Index document")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    print()
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )


if __name__ == '__main__':
    main()
