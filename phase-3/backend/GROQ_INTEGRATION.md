# Groq API Integration Guide

## Overview

The Phase 3 backend now supports **two LLM providers**:
- **OpenRouter**: Access to multiple models (Claude, GPT-4, Llama, Gemini)
- **Groq**: Ultra-fast inference with optimized Llama models

Both providers use OpenAI-compatible APIs, making them interchangeable.

---

## Quick Setup

### Option 1: Using Groq (Recommended for Development)

1. **Get API Key**
   ```bash
   # Visit: https://console.groq.com/keys
   # Sign up (free tier available)
   # Create API key (starts with gsk_)
   ```

2. **Configure .env**
   ```env
   DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
   BETTER_AUTH_SECRET=your-secret-here
   LLM_PROVIDER=GROQ
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   GROQ_MODEL=llama-3.3-70b-versatile
   FRONTEND_URL=http://localhost:3000
   ```

3. **Run Docker**
   ```bash
   cd phase-3/backend
   test-docker.bat  # Windows
   ./test-docker.sh # Linux/Mac
   ```

### Option 2: Using OpenRouter (Recommended for Production)

1. **Get API Key**
   ```bash
   # Visit: https://openrouter.ai/keys
   # Sign up ($5 free credits)
   # Create API key (starts with sk-or-v1-)
   ```

2. **Configure .env**
   ```env
   DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
   BETTER_AUTH_SECRET=your-secret-here
   LLM_PROVIDER=OPENROUTER
   OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
   FRONTEND_URL=http://localhost:3000
   ```

3. **Run Docker**
   ```bash
   cd phase-3/backend
   test-docker.bat  # Windows
   ./test-docker.sh # Linux/Mac
   ```

---

## Architecture

### Code Structure

```
phase-3/backend/
├── src/
│   └── core/
│       ├── config.py              # Provider configuration
│       └── agent_service_mcp.py   # Dynamic provider selection
├── .env.example                   # Environment template
├── docker-entrypoint.sh           # Startup validation
├── test-docker.bat                # Windows test script
└── test-docker.sh                 # Linux/Mac test script
```

### How It Works

1. **Configuration Loading** (`config.py`)
   - Reads `LLM_PROVIDER` from environment
   - Loads provider-specific API keys and models
   - Defaults to OpenRouter if not specified

2. **Dynamic Provider Selection** (`agent_service_mcp.py`)
   ```python
   if settings.LLM_PROVIDER.upper() == "GROQ":
       os.environ["OPENAI_API_KEY"] = settings.GROQ_API_KEY
       os.environ["OPENAI_BASE_URL"] = settings.GROQ_BASE_URL
       self.model = settings.GROQ_MODEL
   else:
       os.environ["OPENAI_API_KEY"] = settings.OPENROUTER_API_KEY
       os.environ["OPENAI_BASE_URL"] = settings.OPENROUTER_BASE_URL
       self.model = settings.OPENROUTER_MODEL
   ```

3. **OpenAI Agents SDK**
   - Uses OpenAI-compatible API
   - Works seamlessly with both providers
   - No code changes needed to switch providers

---

## Available Models

### Groq Models

| Model | Description | Speed | Best For |
|-------|-------------|-------|----------|
| `llama-3.3-70b-versatile` | Latest Llama 3.3 70B | Ultra-fast | General tasks (Recommended) |
| `llama-3.1-70b-versatile` | Llama 3.1 70B | Ultra-fast | Complex reasoning |
| `llama-3.1-8b-instant` | Llama 3.1 8B | Instant | Simple tasks |
| `mixtral-8x7b-32768` | Mixtral 8x7B | Very fast | Long context |
| `gemma2-9b-it` | Gemma 2 9B | Fast | Instruction following |

### OpenRouter Models

| Model | Description | Cost | Best For |
|-------|-------------|------|----------|
| `anthropic/claude-3.5-sonnet` | Claude 3.5 Sonnet | ~$3/M tokens | Complex reasoning (Recommended) |
| `openai/gpt-4-turbo` | GPT-4 Turbo | ~$10/M tokens | Advanced tasks |
| `anthropic/claude-3-opus` | Claude 3 Opus | ~$15/M tokens | Highest quality |
| `meta-llama/llama-3.1-70b-instruct` | Llama 3.1 70B | ~$0.50/M tokens | Cost-effective |
| `google/gemini-pro-1.5` | Gemini Pro 1.5 | ~$2/M tokens | Multimodal |

---

## Switching Providers

### At Runtime

Simply change the `LLM_PROVIDER` in your `.env` file:

```env
# Switch to Groq
LLM_PROVIDER=GROQ
GROQ_API_KEY=gsk_your-key

# Switch to OpenRouter
LLM_PROVIDER=OPENROUTER
OPENROUTER_API_KEY=sk-or-v1-your-key
```

Then restart the container:
```bash
docker restart phase3-backend
```

### For Different Environments

**Development (.env.development)**
```env
LLM_PROVIDER=GROQ
GROQ_API_KEY=gsk_dev_key
GROQ_MODEL=llama-3.1-8b-instant  # Faster for dev
```

**Production (.env.production)**
```env
LLM_PROVIDER=OPENROUTER
OPENROUTER_API_KEY=sk-or-v1-prod-key
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet  # Higher quality
```

---

## Verification

### Check Provider Selection

After starting the container, check the logs:

**With Groq:**
```
[MCP] Using Groq API with model: llama-3.3-70b-versatile
[MCP] Agent initialized with 4 MCP-backed tools
```

**With OpenRouter:**
```
[MCP] Using OpenRouter API with model: anthropic/claude-3.5-sonnet
[MCP] Agent initialized with 4 MCP-backed tools
```

### Test API

```bash
# Health check
curl http://localhost:7860/health

# Test chat (requires authentication)
curl -X POST http://localhost:7860/api/{user_id}/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message":"Create a task to test Groq integration"}'
```

---

## Performance Comparison

### Response Time

| Provider | Model | Avg Response Time | Tokens/sec |
|----------|-------|-------------------|------------|
| Groq | llama-3.3-70b-versatile | 0.5-1s | 500-800 |
| Groq | llama-3.1-8b-instant | 0.2-0.5s | 800-1200 |
| OpenRouter | claude-3.5-sonnet | 2-4s | 100-200 |
| OpenRouter | gpt-4-turbo | 3-6s | 80-150 |

### Cost Comparison (per 1000 messages)

| Provider | Model | Estimated Cost |
|----------|-------|----------------|
| Groq | llama-3.3-70b-versatile | Free (beta) |
| Groq | llama-3.1-8b-instant | Free (beta) |
| OpenRouter | claude-3.5-sonnet | $0.30-$1.50 |
| OpenRouter | gpt-4-turbo | $1.00-$5.00 |

---

## Troubleshooting

### Issue: "GROQ_API_KEY is not set"

**Solution:**
1. Verify `.env` file has `GROQ_API_KEY=gsk_...`
2. Check `LLM_PROVIDER=GROQ` is set
3. Restart container

### Issue: "Invalid API key"

**Solution:**
1. Verify key format:
   - Groq: starts with `gsk_`
   - OpenRouter: starts with `sk-or-v1-`
2. Check key is active in provider dashboard
3. No quotes around key in `.env` file

### Issue: "Model not found"

**Solution:**
1. Check model name matches provider's available models
2. Groq: Use `llama-3.3-70b-versatile` (default)
3. OpenRouter: Use `anthropic/claude-3.5-sonnet` (default)

### Issue: Rate limit exceeded

**Groq:**
- Free tier has rate limits
- Wait a few seconds between requests
- Consider upgrading to paid tier

**OpenRouter:**
- Check credit balance at https://openrouter.ai/credits
- Add more credits if needed

---

## Best Practices

### Development
- ✅ Use Groq for faster iteration
- ✅ Use `llama-3.1-8b-instant` for simple tests
- ✅ Switch to OpenRouter for final testing

### Production
- ✅ Use OpenRouter for reliability
- ✅ Use Claude 3.5 Sonnet for quality
- ✅ Monitor costs and usage
- ✅ Set up fallback provider

### Testing
- ✅ Test with both providers
- ✅ Verify response quality
- ✅ Check error handling
- ✅ Monitor performance metrics

---

## Environment Variables Reference

### Required (Choose One Provider)

**For Groq:**
```env
LLM_PROVIDER=GROQ
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**For OpenRouter:**
```env
LLM_PROVIDER=OPENROUTER
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Optional

```env
# Groq settings
GROQ_BASE_URL=https://api.groq.com/openai/v1  # Default
GROQ_MODEL=llama-3.3-70b-versatile             # Default

# OpenRouter settings
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1  # Default
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet      # Default

# Agent settings
AGENT_NAME=TodoAssistant                       # Default
AGENT_INSTRUCTIONS=You are a helpful...        # Default
MAX_TOKENS=2000                                # Default
TEMPERATURE=0.7                                # Default
```

---

## Migration Guide

### From OpenRouter-only to Dual Provider

If you have an existing deployment using only OpenRouter:

1. **Update code** (already done in this integration)
2. **Update .env.example**
3. **Update documentation**
4. **Test both providers**
5. **Deploy changes**

### Backward Compatibility

The integration is **fully backward compatible**:
- If `LLM_PROVIDER` is not set, defaults to `OPENROUTER`
- Existing `.env` files continue to work
- No breaking changes to API

---

## Support

### Groq
- Dashboard: https://console.groq.com
- Documentation: https://console.groq.com/docs
- API Keys: https://console.groq.com/keys

### OpenRouter
- Dashboard: https://openrouter.ai
- Documentation: https://openrouter.ai/docs
- API Keys: https://openrouter.ai/keys

---

## Summary

✅ **Dual provider support** - Choose between Groq and OpenRouter
✅ **Easy switching** - Change provider with one environment variable
✅ **Backward compatible** - Existing deployments continue to work
✅ **Performance optimized** - Groq for speed, OpenRouter for quality
✅ **Cost effective** - Free tier available with Groq
✅ **Production ready** - Validated startup checks and error handling

**Next Steps:**
1. Choose your provider (Groq for dev, OpenRouter for prod)
2. Get API key from provider dashboard
3. Update `.env` file
4. Run `test-docker.bat` or `test-docker.sh`
5. Test the chat API
