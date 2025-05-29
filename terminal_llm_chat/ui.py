#!/usr/bin/env python3

import os
import sys
import time
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.panel import Panel

class TerminalUI:
    def __init__(self, config, theme=None):
        self.config = config
        self.theme = theme or config.get("UI", "THEME", "green")
        self.console = Console()
        self.animation_speed = int(config.get("UI", "ANIMATION_SPEED", 10))
        self.enable_sounds = config.get_bool("UI", "ENABLE_SOUNDS", True)
        self.max_width = int(config.get("UI", "MAX_WIDTH", 80))
        self.setup_theme()
    
    def setup_theme(self):
        """Configure terminal colors based on the selected theme"""
        self.themes = {
            "green": {"user": "green", "ai": "green", "system": "bright_green", "error": "red"},
            "amber": {"user": "yellow", "ai": "yellow", "system": "bright_yellow", "error": "red"},
            "blue": {"user": "blue", "ai": "cyan", "system": "bright_blue", "error": "red"},
            "matrix": {"user": "green", "ai": "bright_green", "system": "green", "error": "red"},
            "custom": {
                "user": self.config.get("CUSTOM_THEME", "USER_COLOR", "green"),
                "ai": self.config.get("CUSTOM_THEME", "AI_COLOR", "cyan"),
                "system": self.config.get("CUSTOM_THEME", "SYSTEM_COLOR", "yellow"),
                "error": self.config.get("CUSTOM_THEME", "ERROR_COLOR", "red")
            }
        }
        
        # Default to green if theme not found
        if self.theme not in self.themes:
            self.theme = "green"
            
        self.colors = self.themes[self.theme]
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def play_beep(self):
        """Play terminal beep sound if enabled"""
        if self.enable_sounds:
            sys.stdout.write('\a')
            sys.stdout.flush()
    
    def display_welcome(self):
        """Display welcome message and ASCII art"""
        self.clear_screen()
        
        # ASCII art for Terminal LLM Chat
        welcome_text = """
        ╔════════════════════════════════════════════════════════════╗
        ║                                                            ║
        ║        ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗  ║
        ║        ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║  ║
        ║           ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║  ║
        ║           ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║  ║
        ║           ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║  ║
        ║           ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝  ║
        ║                                                            ║
        ║                  ██╗     ██╗     ███╗   ███╗              ║
        ║                  ██║     ██║     ████╗ ████║              ║
        ║                  ██║     ██║     ██╔████╔██║              ║
        ║                  ██║     ██║     ██║╚██╔╝██║              ║
        ║                  ███████╗███████╗██║ ╚═╝ ██║              ║
        ║                  ╚══════╝╚══════╝╚═╝     ╚═╝              ║
        ║                                                            ║
        ║          ██████╗██╗  ██╗ █████╗ ████████╗                ║
        ║         ██╔════╝██║  ██║██╔══██╗╚══██╔══╝                ║
        ║         ██║     ███████║███████║   ██║                   ║
        ║         ██║     ██╔══██║██╔══██║   ██║                   ║
        ║         ╚██████╗██║  ██║██║  ██║   ██║                   ║
        ║          ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝                   ║
        ║                                                            ║
        ╚════════════════════════════════════════════════════════════╝
        
           v0.1.0 | Type your message or /help for commands
        """
        
        self.console.print(Panel(welcome_text, style=f"bold {self.colors['system']}"))
        self.console.print(f"\nUsing model: [bold]{self.config.get('API', 'MODEL')}[/bold]\n", style=self.colors['system'])
    
    def display_exit_message(self):
        """Display exit message"""
        self.console.print("\n\nTerminating session. Goodbye!\n", style=f"bold {self.colors['system']}")
    
    def display_error(self, error_message):
        """Display error message"""
        self.console.print(f"\nERROR: {error_message}\n", style=f"bold {self.colors['error']}")
        self.play_beep()
    
    def display_user_input_prompt(self):
        """Display the user input prompt"""
        self.console.print("\n> ", style=f"bold {self.colors['user']}", end="")
    
    def display_user_message(self, message):
        """Display user message"""
        self.console.print(f"\n> {message}", style=self.colors['user'])
    
    def display_ai_message(self, message, streaming=True):
        """Display AI message with optional character-by-character animation"""
        self.console.print("\nAI:", style=f"bold {self.colors['ai']}")
        
        if not streaming or self.animation_speed <= 0:
            # Render markdown if not streaming
            self.console.print(Markdown(message))
            return
        
        # Character-by-character streaming with markdown support
        # This is a simplified version - a real implementation would need 
        # more sophisticated markdown parsing
        buffer = ""
        in_code_block = False
        code_lang = ""
        code_buffer = ""
        
        for char in message:
            if buffer.endswith("```") and not in_code_block:
                in_code_block = True
                code_lang = ""
                code_buffer = ""
                self.console.print(buffer[:-3], end="")
                self.console.print("```", style="bright_black", end="")
                buffer = ""
            elif buffer.endswith("```") and in_code_block:
                in_code_block = False
                syntax = Syntax(code_buffer, code_lang, theme="monokai")
                self.console.print("")
                self.console.print(syntax)
                buffer = ""
            elif in_code_block and char == '\n' and not code_lang and code_buffer == "":
                # First line in code block defines the language
                code_lang = buffer.strip()
                buffer = ""
                continue
            elif in_code_block:
                code_buffer += char
            else:
                buffer += char
            
            if not in_code_block:
                self.console.print(char, end="", flush=True)
                time.sleep(self.animation_speed / 1000)
        
        # Print any remaining buffer
        if buffer:
            self.console.print(buffer)
    
    def display_system_message(self, message):
        """Display system message"""
        self.console.print(f"\nSYSTEM: {message}", style=self.colors['system'])
    
    def display_help(self, commands):
        """Display help information"""
        self.console.print("\nAvailable Commands:\n", style=f"bold {self.colors['system']}")
        for cmd, desc in commands.items():
            self.console.print(f"  {cmd:<15} - {desc}", style=self.colors['system'])
    
    def get_user_input(self):
        """Get user input with command history support"""
        self.display_user_input_prompt()
        return input()
