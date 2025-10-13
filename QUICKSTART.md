# Quick Start Guide

Get started with the AI Search Assistant in minutes!

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

## Step 3: (Optional) Start Elasticsearch

If you have Docker:
```bash
docker run -d --name elasticsearch -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" elasticsearch:8.11.0
```

Or skip this step - the assistant works without Elasticsearch using AI-only mode.

## Step 4: Index Sample Data (Optional)

```bash
python index_sample_data.py
```

## Step 5: Start the CLI

```bash
python cli.py
```

## Quick Commands

Try these in the CLI:

```
/search machine learning
/ask what is artificial intelligence?
/chat tell me about cloud computing
```

Or just type naturally:
```
what is the difference between AI and ML?
```

That's it! You're ready to use the AI Search Assistant! 🎉

## Minimal Setup (No Elasticsearch)

If you just want to try the AI features without setting up Elasticsearch:

1. Install dependencies: `pip install -r requirements.txt`
2. Add your Gemini API key to `.env`
3. Run: `python cli.py`
4. Start chatting!

The assistant will work in AI-only mode without search capabilities.

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [example.py](example.py) for programmatic usage
- Customize search weights in `.env`
- Index your own documents
