#!/usr/bin/env python3

import os
import json
from datetime import datetime
from typing import List, Dict

class ChatSession:
    def __init__(self, ui, llm, config):
        self.ui = ui
        self.llm = llm
        self.config = config
        self.messages = []
        self.history_file = os.path.join(config.config_dir, "history")
        self.conversations_dir = os.path.join(config.config_dir, "conversations")
        
        # Create history and conversations directories if they don't exist
        os.makedirs(self.history_file, exist_ok=True)
        os.makedirs(self.conversations_dir, exist_ok=True)
        
        # Add system message
        self.add_message("system", self.llm.system_prompt)
    
    def add_message(self, role, content):
        """Add a message to the conversation"""
        self.messages.append({"role": role, "content": content})
    
    def run(self):
        """Run the main chat loop"""
        while True:
            user_input = self.ui.get_user_input()
            
            # Check if it's a command
            if user_input.startswith("/"):
                self.handle_command(user_input)
                continue
            
            # Process normal user message
            self.add_message("user", user_input)
            
            # Get AI response
            try:
                response = self.llm.get_completion(self.messages)
                self.add_message("assistant", response)
                self.ui.display_ai_message(response)
            except Exception as e:
                self.ui.display_error(f"Error getting AI response: {str(e)}")
    
    def handle_command(self, command):
        """Handle chat commands"""
        cmd_parts = command.split()
        cmd = cmd_parts[0].lower()
        args = cmd_parts[1:] if len(cmd_parts) > 1 else []
        
        # Available commands
        commands = {
            "/help": self.cmd_help,
            "/clear": self.cmd_clear,
            "/cls": self.cmd_clear,
            "/clear-screen": self.cmd_clear,
            "/exit": self.cmd_exit,
            "/quit": self.cmd_exit,
            "/save": self.cmd_save,
            "/load": self.cmd_load,
            "/theme": self.cmd_theme,
            "/system": self.cmd_system,
            "/models": self.cmd_models,
            "/model": self.cmd_model,
            "/tokens": self.cmd_tokens,
            "/export": self.cmd_export
        }
        
        if cmd in commands:
            commands[cmd](args)
        else:
            self.ui.display_error(f"Unknown command: {cmd}. Type /help for available commands.")
    
    def cmd_help(self, args):
        """Display help information"""
        commands = {
            "/help": "Show available commands",
            "/clear, /cls": "Clear the screen",
            "/exit, /quit": "Exit the application",
            "/save [filename]": "Save the current conversation",
            "/load [filename]": "Load a previous conversation",
            "/theme [name]": "Change the color theme",
            "/system [prompt]": "View or change the system instructions",
            "/models": "List available AI models",
            "/model [name]": "Switch to a different model",
            "/tokens": "Show token usage statistics",
            "/export [format]": "Export conversation (md, txt, html)"
        }
        self.ui.display_help(commands)
    
    def cmd_clear(self, args):
        """Clear the screen"""
        self.ui.clear_screen()
        self.ui.display_system_message(f"Using model: {self.llm.model}")
    
    def cmd_exit(self, args):
        """Exit the application"""
        self.ui.display_exit_message()
        exit(0)
    
    def cmd_save(self, args):
        """Save the current conversation"""
        filename = args[0] if args else f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if not filename.endswith(".json"):
            filename += ".json"
        
        filepath = os.path.join(self.conversations_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump({
                    "messages": self.messages,
                    "model": self.llm.model,
                    "timestamp": datetime.now().isoformat()
                }, f, indent=2)
            self.ui.display_system_message(f"Conversation saved to {filename}")
        except Exception as e:
            self.ui.display_error(f"Error saving conversation: {str(e)}")
    
    def cmd_load(self, args):
        """Load a previous conversation"""
        if not args:
            self.ui.display_error("Please specify a file to load")
            return
        
        filename = args[0]
        if not filename.endswith(".json"):
            filename += ".json"
        
        filepath = os.path.join(self.conversations_dir, filename)
        
        if not os.path.exists(filepath):
            self.ui.display_error(f"File not found: {filename}")
            return
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self.messages = data["messages"]
            if "model" in data:
                self.llm.set_model(data["model"])
            
            self.ui.clear_screen()
            self.ui.display_system_message(f"Loaded conversation from {filename}")
            
            # Display conversation
            for msg in self.messages:
                if msg["role"] == "user":
                    self.ui.display_user_message(msg["content"])
                elif msg["role"] == "assistant":
                    self.ui.display_ai_message(msg["content"], streaming=False)
        except Exception as e:
            self.ui.display_error(f"Error loading conversation: {str(e)}")
    
    def cmd_theme(self, args):
        """Change the color theme"""
        if not args:
            current_theme = self.ui.theme
            available_themes = list(self.ui.themes.keys())
            self.ui.display_system_message(f"Current theme: {current_theme}")
            self.ui.display_system_message(f"Available themes: {', '.join(available_themes)}")
            return
        
        theme = args[0].lower()
        if theme not in self.ui.themes:
            self.ui.display_error(f"Unknown theme: {theme}")
            return
        
        self.ui.theme = theme
        self.ui.setup_theme()
        self.config.set("UI", "THEME", theme)
        self.config.save()
        self.ui.display_system_message(f"Theme changed to {theme}")
    
    def cmd_system(self, args):
        """View or change the system instructions"""
        if not args:
            self.ui.display_system_message(f"Current system prompt: {self.llm.system_prompt}")
            return
        
        new_prompt = " ".join(args)
        self.llm.set_system_prompt(new_prompt)
        
        # Update the system message in the conversation
        for i, msg in enumerate(self.messages):
            if msg["role"] == "system":
                self.messages[i]["content"] = new_prompt
                break
        
        self.config.set("SYSTEM", "DEFAULT_PROMPT", new_prompt)
        self.config.save()
        self.ui.display_system_message(f"System prompt updated")
    
    def cmd_models(self, args):
        """List available AI models"""
        try:
            models = self.llm.get_available_models()
            self.ui.display_system_message(f"Current model: {self.llm.model}")
            self.ui.display_system_message(f"Available models:\n{', '.join(models)}")
        except Exception as e:
            self.ui.display_error(f"Error fetching models: {str(e)}")
    
    def cmd_model(self, args):
        """Switch to a different model"""
        if not args:
            self.ui.display_system_message(f"Current model: {self.llm.model}")
            self.ui.display_system_message("Use /models to see available models")
            return
        
        model = args[0]
        self.llm.set_model(model)
        self.config.set("API", "MODEL", model)
        self.config.save()
        self.ui.display_system_message(f"Model changed to {model}")
    
    def cmd_tokens(self, args):
        """Show token usage statistics"""
        # This is a placeholder - a real implementation would track token usage
        self.ui.display_system_message("Token usage tracking not implemented in this example.")
    
    def cmd_export(self, args):
        """Export conversation in different formats"""
        if not args:
            self.ui.display_error("Please specify a format: md, txt, html")
            return
        
        format_type = args[0].lower()
        if format_type not in ["md", "txt", "html"]:
            self.ui.display_error("Supported formats: md, txt, html")
            return
        
        filename = args[1] if len(args) > 1 else f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if not filename.endswith(f".{format_type}"):
            filename += f".{format_type}"
        
        filepath = os.path.join(self.conversations_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                if format_type == "md":
                    f.write(f"# Conversation with {self.llm.model}\n\n")
                    for msg in self.messages:
                        if msg["role"] == "system":
                            continue
                        if msg["role"] == "user":
                            f.write(f"## User\n\n{msg['content']}\n\n")
                        elif msg["role"] == "assistant":
                            f.write(f"## AI ({self.llm.model})\n\n{msg['content']}\n\n")
                elif format_type == "txt":
                    for msg in self.messages:
                        if msg["role"] == "system":
                            continue
                        if msg["role"] == "user":
                            f.write(f"User: {msg['content']}\n\n")
                        elif msg["role"] == "assistant":
                            f.write(f"AI: {msg['content']}\n\n")
                elif format_type == "html":
                    f.write(f"<!DOCTYPE html>\n<html>\n<head>\n")
                    f.write(f"<title>Conversation with {self.llm.model}</title>\n")
                    f.write(f"<style>\n")
                    f.write(f"body {{ font-family: Arial, sans-serif; margin: 20px; }}\n")
                    f.write(f".user {{ background-color: #e6f7ff; padding: 10px; border-radius: 5px; margin-bottom: 10px; }}\n")
                    f.write(f".ai {{ background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px; }}\n")
                    f.write(f"h2 {{ font-size: 1em; margin-top: 0; }}\n")
                    f.write(f"</style>\n</head>\n<body>\n")
                    f.write(f"<h1>Conversation with {self.llm.model}</h1>\n")
                    
                    for msg in self.messages:
                        if msg["role"] == "system":
                            continue
                        if msg["role"] == "user":
                            f.write(f"<div class=\"user\">\n<h2>User:</h2>\n<p>{msg['content']}</p>\n</div>\n")
                        elif msg["role"] == "assistant":
                            f.write(f"<div class=\"ai\">\n<h2>AI ({self.llm.model}):</h2>\n<p>{msg['content']}</p>\n</div>\n")
                    
                    f.write(f"</body>\n</html>")
            
            self.ui.display_system_message(f"Conversation exported to {filename}")
        except Exception as e:
            self.ui.display_error(f"Error exporting conversation: {str(e)}")
