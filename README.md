# Agent Playground

A collection of AI agents built with Google ADK (Agent Development Kit) for various use cases.

## Overview

This repository contains multiple AI agents that demonstrate different capabilities:

- **Basic Agent** - Simple Q&A assistant
- **Multi-tool Agent** - Agent with weather and time tools

## Prerequisites

- Python 3.10+
- Google Cloud account (for Vertex AI) or Google API key
- Telegram Bot Token (for Telegram agent)

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Yuds16/Agent-Playground.git
   cd Agent-Playground
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy and configure `.env` files in each agent directory
   - Set your Google API key or Vertex AI credentials
   - Add Telegram bot token for the Telegram agent

## Agents

### Basic Agent (`my_agent/`)
Simple conversational AI agent using Gemini 2.5 Flash.

```bash
adk run my_agent
```

### Multi-tool Agent (`multi_tool_agent/`)
Agent with custom tools for weather and time queries.

**Tools:**
- Get weather information (New York)
- Get current time (New York, Singapore)

```bash
adk run multi_tool_agent
```

## Configuration

Each agent has its own `.env` file for configuration:

```env
GOOGLE_GENAI_USE_VERTEXAI=0  # Use 0 for API key, 1 for Vertex AI
GOOGLE_API_KEY=your_api_key_here
```

## Usage

Run any agent using the ADK CLI:
```bash
adk run <agent_directory>
```

Type `exit` to stop the agent.

Run on the web interface:
```bash
adk web
```

Pick agent from the list and interact via web UI.

## License

This project is for educational and experimental purposes.