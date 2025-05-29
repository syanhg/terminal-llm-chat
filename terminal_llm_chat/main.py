#!/usr/bin/env python3

import argparse
import sys
from terminal_llm_chat.chat import ChatSession
from terminal_llm_chat.config import Config
from terminal_llm_chat.ui import TerminalUI
from terminal_llm_chat.llm import LLMProvider

def parse_args():
    parser = argparse.ArgumentParser(description="Terminal LLM Chat - A retro terminal interface for AI chat")
    parser.add_argument("--model", type=str, help="Specify the LLM model to use")
    parser.add_argument("--system", type=str, help="Custom system prompt for the AI")
    parser.add_argument("--theme", type=str, help="UI theme (green, amber, blue, matrix, custom)")
    parser.add_argument("--setup", action="store_true", help="Run the setup wizard")
    parser.add_argument("--load", type=str, help="Load a previous conversation")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Load configuration
    config = Config()
    if args.setup:
        config.run_setup_wizard()
        return
    
    # Initialize components
    ui = TerminalUI(config, theme=args.theme)
    llm = LLMProvider(config)
    
    # Override with command line arguments if provided
    if args.model:
        llm.set_model(args.model)
    if args.system:
        llm.set_system_prompt(args.system)
    
    # Create chat session
    session = ChatSession(ui, llm, config)
    
    # Load previous conversation if requested
    if args.load:
        session.load(args.load)
    
    # Display welcome message
    ui.display_welcome()
    
    # Start the main loop
    try:
        session.run()
    except KeyboardInterrupt:
        ui.display_exit_message()
    except Exception as e:
        ui.display_error(f"An error occurred: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
