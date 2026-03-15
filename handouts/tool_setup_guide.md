# Tool Setup Guide — AI Research Workshop

## Option 1: Cursor + Gemini (FREE model, $20/mo Cursor sub)

### Install Cursor
1. Download from https://cursor.com
2. Install and open
3. Sign in / start free trial

### Set Gemini as your model
1. Open Settings (Cmd+, on Mac)
2. Go to **Models**
3. Select **Gemini 2.5 Pro** as your default chat model
4. This uses Google's free tier — no API key needed

### Quick test
- Open any file → press **Cmd+K** → type "write a hello world in python"
- Open chat panel (**Cmd+L**) → ask "explain what this file does"

---

## Option 2: Claude Code Router + Gemini ($20/mo Claude Code sub)

### Install Claude Code
```bash
npm install -g @anthropic-ai/claude-code
```

### Authenticate
```bash
claude
# Follow the login prompts — uses your Anthropic account
```

### Configure the Router
The router automatically uses cheaper/free models for simple tasks
and routes complex tasks to Claude. To configure:

```bash
# In your project directory:
claude /model
# Select the model routing option
```

### Quick test
```bash
claude "What model are you? Write a hello world in python."
```

---

## Option 3: Claude Code Direct ($20/mo + API usage)

Same install as Option 2. The difference is usage — direct mode
uses Claude (Opus or Sonnet) for everything.

```bash
claude "Use plan mode. Help me design a research experiment."
```

### Cost awareness
- Opus: ~$15/M input tokens, $75/M output tokens
- Sonnet: ~$3/M input tokens, $15/M output tokens
- A typical 2-hour coding session: $5–$30 depending on usage
- Use `/cost` in Claude Code to check your spend

---

## Verify Your Setup

Run this in your terminal to confirm everything works:

```bash
# Create a test project
mkdir ~/workshop-test && cd ~/workshop-test
git init

# Test Claude Code
claude "Create a simple Python script that prints 'Setup works!'"

# Run it
python3 test.py
```

For Cursor: open the `~/workshop-test` folder, open any file, and
use Cmd+K or Cmd+L to verify the AI features work.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `claude: command not found` | Run `npm install -g @anthropic-ai/claude-code` again |
| Cursor AI not responding | Check Settings → Models, ensure a model is selected |
| Rate limited | Switch to Gemini (free tier has generous limits) |
| No API key | Claude Code uses OAuth login, not API keys |
| Python not found | Use `python3` instead of `python` on Mac |
