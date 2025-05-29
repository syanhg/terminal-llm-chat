#!/bin/bash

# Run Terminal LLM Chat

# Ensure virtual environment is activated if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install the package in development mode if not already installed
if ! pip show terminal-llm-chat > /dev/null 2>&1; then
    pip install -e .
fi

# Run the chat application
python -m terminal_llm_chat.main "$@"