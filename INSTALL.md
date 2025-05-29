# Installation Guide for Terminal LLM Chat

This document provides detailed instructions for installing and configuring Terminal LLM Chat.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Git (optional, for development installation)

## Quick Installation

### From PyPI (Recommended)

```bash
# Install the package
pip install terminal-llm-chat

# Run the application
terminal-chat
```

### From Source

```bash
# Clone the repository
git clone https://github.com/syanhg/terminal-llm-chat.git
cd terminal-llm-chat

# Option 1: Install in development mode
pip install -e .

# Option 2: Use the run script directly
chmod +x run.sh
./run.sh
```

## Virtual Environment Setup (Recommended)

It's recommended to install Terminal LLM Chat in a virtual environment to avoid conflicts with other Python packages:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Terminal LLM Chat
pip install terminal-llm-chat
# Or for development:
pip install -e .
```

## API Keys Configuration

For the application to work with commercial LLM providers, you'll need to obtain API keys:

1. **OpenAI**: Sign up at [platform.openai.com](https://platform.openai.com) and create an API key.
2. **Anthropic**: Sign up at [console.anthropic.com](https://console.anthropic.com) and create an API key.
3. **OpenRouter**: Sign up at [openrouter.ai](https://openrouter.ai) and create an API key.

For local models:

- **Ollama**: Install Ollama from [ollama.ai](https://ollama.ai) and run it locally.

## Configuration File

The configuration file is located at:
- Linux/macOS: `~/.config/terminal-llm-chat/config.ini`
- Windows: `%USERPROFILE%\.config\terminal-llm-chat\config.ini`

You can also run the setup wizard to configure the application:

```bash
terminal-chat --setup
```

## Troubleshooting

### Common Issues

1. **Missing Dependencies**: If you encounter errors about missing modules, try installing the dependencies manually:
   ```bash
   pip install requests rich tiktoken configparser
   ```

2. **API Key Issues**: Ensure your API keys are correctly configured in the config file or through the setup wizard.

3. **Permission Errors**: On Linux/macOS, you may need to make the run script executable:
   ```bash
   chmod +x run.sh
   ```

4. **Path Issues**: If the `terminal-chat` command is not found, ensure that your Python scripts directory is in your PATH.

## Uninstallation

To uninstall Terminal LLM Chat:

```bash
pip uninstall terminal-llm-chat
```

To remove configuration files:

```bash
# On Linux/macOS:
rm -rf ~/.config/terminal-llm-chat

# On Windows:
rmdir /s /q %USERPROFILE%\.config\terminal-llm-chat
```