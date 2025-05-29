# Terminal LLM Chat

<p align="center">
  <img src="https://raw.githubusercontent.com/syanhg/terminal-llm-chat/main/assets/terminal-logo.png" alt="Terminal LLM Chat Logo" width="250" />
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A terminal-themed LLM chatbot with a retro interface for interacting with AI language models. Experience the nostalgic feel of a command-line interface while harnessing the power of modern AI.

## ✨ Features

- **Retro Terminal UI**: Old-school terminal aesthetics with modern functionality
- **Multiple LLM Backends**: Support for OpenAI, Anthropic, OpenRouter, or local models via Ollama
- **Streaming Responses**: See AI responses generate character by character
- **Syntax Highlighting**: Beautiful code formatting for programming-related responses
- **Command History**: Navigate through previous commands with arrow keys
- **Customizable Themes**: Choose from classic green-on-black, amber, blue, or custom color schemes
- **Session Management**: Save and load conversation histories
- **Export Options**: Save conversations as markdown, text, or HTML
- **System Prompts**: Define custom system instructions for the AI
- **Markdown Support**: Render markdown responses in the terminal
- **Low Resource Usage**: Minimal memory footprint and CPU usage

## 🚀 Installation

```bash
# Install from PyPI
pip install terminal-llm-chat

# Or install the latest development version
pip install git+https://github.com/syanhg/terminal-llm-chat.git
```

## 🔧 Configuration

On first run, you'll be prompted to set up your API keys and preferences. Alternatively, create a configuration file at `~/.config/terminal-llm-chat/config.ini`:

```ini
[API]
PROVIDER = openai  # Options: openai, anthropic, openrouter, ollama
API_KEY = your_api_key_here
MODEL = gpt-3.5-turbo  # Or claude-3-opus, llama-3, etc.

[UI]
THEME = green  # Options: green, amber, blue, custom
ANIMATION_SPEED = 10  # Character delay in ms (0 to disable)
ENABLE_SOUNDS = true  # Terminal beep and typing sounds
MAX_WIDTH = 80  # Character width for text wrapping

[SYSTEM]
DEFAULT_PROMPT = You are a helpful AI assistant responding in a terminal.
TEMPERATURE = 0.7
MAX_TOKENS = 2000
```

## 💻 Usage

### Basic Commands

```bash
# Start the chat interface
terminal-chat

# Start with a specific model
terminal-chat --model gpt-4

# Start with a custom system prompt
terminal-chat --system "You are a Linux terminal expert"

# Load a previous session
terminal-chat --load last_session
```

### In-Chat Commands

- `/help` - Show available commands
- `/clear` - Clear the screen
- `/exit` or `Ctrl+D` - Exit the application
- `/save [filename]` - Save the current conversation
- `/load [filename]` - Load a previous conversation
- `/theme [name]` - Change the color theme
- `/system [prompt]` - View or change the system instructions
- `/models` - List available AI models
- `/model [name]` - Switch to a different model
- `/tokens` - Show token usage statistics
- `/export [format]` - Export conversation (md, txt, html)

## 🎨 Themes

Terminal LLM Chat comes with several built-in themes:

- **green** - Classic green text on black background
- **amber** - Vintage amber/orange terminal look
- **blue** - IBM 3270 inspired blue terminal
- **matrix** - Cascading green Matrix-style theme
- **custom** - Define your own colors in the config file

## 🔌 Plugins

Extend functionality with plugins placed in `~/.config/terminal-llm-chat/plugins/`:

```python
# Example plugin: weather.py
from terminal_llm_chat import Plugin

class WeatherPlugin(Plugin):
    def __init__(self):
        super().__init__("weather", "Get current weather information")
    
    def on_command(self, command, args):
        if command == "weather":
            # Implement weather lookup logic
            return True, "Weather for {}: ☀️ 72°F"
        return False, ""
```

## 📋 Requirements

- Python 3.7 or higher
- Required packages: openai, rich, requests, tiktoken, configparser
- Optional: ollama (for local model support)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Inspired by classic terminal interfaces and modern CLI tools
- Thanks to all the open-source LLM providers and communities