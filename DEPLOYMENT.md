# Deployment Guide

Complete guide for deploying the AI Search Assistant in various environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Considerations](#production-considerations)

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step-by-Step Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/masterAtGithub143AtN/devpost_compition1.git
cd devpost_compition1
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

Required configuration:
```env
# Minimal setup - just Gemini API key for AI-only mode
GEMINI_API_KEY=your_gemini_api_key_here

# Optional - for full functionality
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
```

#### 5. Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key to your `.env` file

#### 6. Run Validation

```bash
python validate.py
```

Expected output: All checks should pass (26/26)

#### 7. Start Using

```bash
# AI-only mode (no Elasticsearch needed)
python cli.py

# With search (requires Elasticsearch)
python index_sample_data.py  # Index sample data first
python cli.py
```

## Docker Deployment

### Quick Start with Docker Compose

#### 1. Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  elasticsearch:
    image: elasticsearch:8.11.0
    container_name: ai-search-elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data
    networks:
      - ai-search-net

  ai-assistant:
    build: .
    container_name: ai-search-assistant
    depends_on:
      - elasticsearch
    environment:
      - ELASTICSEARCH_HOST=elasticsearch
      - ELASTICSEARCH_PORT=9200
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - .:/app
    networks:
      - ai-search-net
    command: python cli.py

volumes:
  es_data:
    driver: local

networks:
  ai-search-net:
    driver: bridge
```

#### 2. Create `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run validation
RUN python validate.py

CMD ["python", "cli.py"]
```

#### 3. Create `.dockerignore`

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
.env
.git/
.gitignore
*.md
!README.md
.vscode/
.idea/
```

#### 4. Deploy

```bash
# Set your API key
export GEMINI_API_KEY=your_key_here

# Start services
docker-compose up -d

# View logs
docker-compose logs -f ai-assistant

# Stop services
docker-compose down
```

### Manual Docker Deployment

```bash
# Build image
docker build -t ai-search-assistant .

# Run Elasticsearch
docker run -d \
  --name elasticsearch \
  -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  elasticsearch:8.11.0

# Run AI Assistant
docker run -it \
  --name ai-assistant \
  --link elasticsearch \
  -e ELASTICSEARCH_HOST=elasticsearch \
  -e GEMINI_API_KEY=your_key_here \
  ai-search-assistant
```

## Cloud Deployment

### Google Cloud Platform (GCP)

#### Option 1: Cloud Run

```bash
# 1. Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-search-assistant

# 2. Deploy to Cloud Run
gcloud run deploy ai-search-assistant \
  --image gcr.io/PROJECT_ID/ai-search-assistant \
  --platform managed \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=your_key \
  --allow-unauthenticated
```

#### Option 2: GKE (Kubernetes)

```bash
# 1. Create cluster
gcloud container clusters create ai-search-cluster \
  --num-nodes=3 \
  --zone=us-central1-a

# 2. Apply Kubernetes manifests
kubectl apply -f k8s/

# 3. Expose service
kubectl expose deployment ai-assistant --type=LoadBalancer --port=80
```

#### Using Elastic Cloud

```bash
# 1. Create Elastic Cloud deployment
# Visit: https://cloud.elastic.co

# 2. Get connection details
export ELASTICSEARCH_HOST=your-deployment.elastic-cloud.com
export ELASTICSEARCH_USER=elastic
export ELASTICSEARCH_PASSWORD=your_password

# 3. Update .env and deploy
```

### AWS Deployment

#### Option 1: ECS Fargate

```bash
# 1. Push image to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

docker tag ai-search-assistant ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/ai-search-assistant
docker push ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/ai-search-assistant

# 2. Create ECS task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# 3. Create ECS service
aws ecs create-service --cluster default --service-name ai-assistant \
  --task-definition ai-search-assistant --desired-count 1
```

#### Option 2: EC2

```bash
# 1. Launch EC2 instance (Ubuntu 22.04)

# 2. SSH into instance
ssh -i your-key.pem ubuntu@ec2-instance

# 3. Setup application
git clone https://github.com/masterAtGithub143AtN/devpost_compition1.git
cd devpost_compition1
./scripts/setup.sh

# 4. Run as service (systemd)
sudo systemctl enable ai-search-assistant
sudo systemctl start ai-search-assistant
```

### Azure Deployment

#### Container Instances

```bash
# 1. Create resource group
az group create --name ai-search-rg --location eastus

# 2. Deploy container
az container create \
  --resource-group ai-search-rg \
  --name ai-assistant \
  --image ai-search-assistant \
  --cpu 1 --memory 1.5 \
  --environment-variables GEMINI_API_KEY=your_key \
  --ports 80
```

## Production Considerations

### Security

#### 1. API Key Management

**Use Secret Management Services:**

```bash
# GCP Secret Manager
gcloud secrets create gemini-api-key --data-file=key.txt
gcloud secrets versions access latest --secret=gemini-api-key

# AWS Secrets Manager
aws secretsmanager create-secret --name gemini-api-key --secret-string "your-key"
aws secretsmanager get-secret-value --secret-id gemini-api-key

# Azure Key Vault
az keyvault secret set --vault-name my-vault --name gemini-api-key --value "your-key"
az keyvault secret show --vault-name my-vault --name gemini-api-key
```

#### 2. Network Security

- Use private networks for internal communication
- Implement firewall rules
- Enable TLS/SSL for all connections
- Use VPN for admin access

#### 3. Access Control

```python
# Add authentication middleware
from functools import wraps
from flask import request, abort

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != os.getenv('API_KEY'):
            abort(401)
        return f(*args, **kwargs)
    return decorated_function
```

### Performance

#### 1. Caching

```python
from functools import lru_cache
import redis

# In-memory cache
@lru_cache(maxsize=1000)
def cached_search(query):
    return assistant.search(query)

# Redis cache
redis_client = redis.Redis(host='localhost', port=6379)

def cached_search_redis(query):
    cached = redis_client.get(f"search:{query}")
    if cached:
        return json.loads(cached)
    
    results = assistant.search(query)
    redis_client.setex(f"search:{query}", 3600, json.dumps(results))
    return results
```

#### 2. Connection Pooling

```python
from elasticsearch import Elasticsearch

# Use connection pooling
es = Elasticsearch(
    hosts=['localhost:9200'],
    maxsize=25,
    timeout=30,
    retry_on_timeout=True
)
```

#### 3. Load Balancing

```nginx
# nginx.conf
upstream ai_assistant {
    least_conn;
    server backend1.example.com:5000;
    server backend2.example.com:5000;
    server backend3.example.com:5000;
}

server {
    listen 80;
    location / {
        proxy_pass http://ai_assistant;
    }
}
```

### Monitoring

#### 1. Logging

```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
handler = RotatingFileHandler(
    'ai-search.log',
    maxBytes=10000000,
    backupCount=5
)
logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
```

#### 2. Metrics

```python
from prometheus_client import Counter, Histogram

# Define metrics
search_requests = Counter('search_requests_total', 'Total search requests')
search_duration = Histogram('search_duration_seconds', 'Search duration')

# Use metrics
with search_duration.time():
    results = assistant.search(query)
search_requests.inc()
```

#### 3. Health Checks

```python
@app.route('/health')
def health_check():
    checks = {
        'elasticsearch': check_elasticsearch(),
        'gemini': check_gemini(),
        'memory': check_memory()
    }
    
    if all(checks.values()):
        return jsonify({'status': 'healthy', 'checks': checks}), 200
    else:
        return jsonify({'status': 'unhealthy', 'checks': checks}), 503
```

### Backup and Recovery

#### 1. Elasticsearch Snapshots

```bash
# Create snapshot repository
curl -X PUT "localhost:9200/_snapshot/my_backup" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "/mount/backups/my_backup"
  }
}
'

# Create snapshot
curl -X PUT "localhost:9200/_snapshot/my_backup/snapshot_1?wait_for_completion=true"

# Restore snapshot
curl -X POST "localhost:9200/_snapshot/my_backup/snapshot_1/_restore"
```

#### 2. Configuration Backup

```bash
# Backup configuration
tar -czf backup-$(date +%Y%m%d).tar.gz .env config/ data/

# Automated daily backups
0 2 * * * /path/to/backup-script.sh
```

### Scaling

#### Horizontal Scaling

```yaml
# Kubernetes horizontal pod autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-assistant-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-assistant
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

#### Elasticsearch Scaling

```bash
# Add more nodes to cluster
curl -X PUT "localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d'
{
  "persistent": {
    "cluster.routing.allocation.disk.watermark.low": "85%",
    "cluster.routing.allocation.disk.watermark.high": "90%"
  }
}
'
```

## Troubleshooting

### Common Issues

1. **Elasticsearch connection failed**
   ```bash
   # Check if Elasticsearch is running
   curl http://localhost:9200
   
   # Check logs
   docker logs elasticsearch
   ```

2. **Gemini API errors**
   ```bash
   # Verify API key
   echo $GEMINI_API_KEY
   
   # Check quota
   # Visit: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas
   ```

3. **Out of memory**
   ```bash
   # Increase Docker memory
   docker update --memory="2g" container_name
   
   # Or in docker-compose.yml:
   mem_limit: 2g
   ```

## Maintenance

### Regular Tasks

- [ ] Monitor logs daily
- [ ] Review error rates weekly
- [ ] Update dependencies monthly
- [ ] Backup data weekly
- [ ] Rotate API keys quarterly
- [ ] Review and optimize queries monthly
- [ ] Test disaster recovery quarterly

### Updates

```bash
# Update dependencies
pip list --outdated
pip install -U package_name

# Update application
git pull origin main
pip install -r requirements.txt
python validate.py
# Restart services
```

## Support

For issues and questions:
- Check the [README](README.md)
- Review [ARCHITECTURE](ARCHITECTURE.md)
- Open an issue on GitHub
- Contact the maintainers
