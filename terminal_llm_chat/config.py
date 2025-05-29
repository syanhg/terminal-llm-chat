#!/usr/bin/env python3

import os
import configparser
from pathlib import Path

class Config:
    def __init__(self, config_dir=None):
        # Set default config directory
        if config_dir is None:
            self.config_dir = os.path.expanduser("~/.config/terminal-llm-chat")
        else:
            self.config_dir = config_dir
        
        # Create config directory if it doesn't exist
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Config file path
        self.config_path = os.path.join(self.config_dir, "config.ini")
        
        # Initialize config parser
        self.config = configparser.ConfigParser()
        
        # Load config or create default if it doesn't exist
        if os.path.exists(self.config_path):
            self.config.read(self.config_path)
        else:
            self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration file"""
        self.config["API"] = {
            "PROVIDER": "openai",
            "API_KEY": "",
            "MODEL": "gpt-3.5-turbo"
        }
        
        self.config["UI"] = {
            "THEME": "green",
            "ANIMATION_SPEED": "10",
            "ENABLE_SOUNDS": "true",
            "MAX_WIDTH": "80"
        }
        
        self.config["SYSTEM"] = {
            "DEFAULT_PROMPT": "You are a helpful AI assistant responding in a terminal.",
            "TEMPERATURE": "0.7",
            "MAX_TOKENS": "2000"
        }
        
        self.config["CUSTOM_THEME"] = {
            "USER_COLOR": "green",
            "AI_COLOR": "cyan",
            "SYSTEM_COLOR": "yellow",
            "ERROR_COLOR": "red"
        }
        
        self.save()
    
    def get(self, section, key, default=None):
        """Get a config value with a fallback to default"""
        try:
            return self.config[section][key]
        except (KeyError, configparser.NoSectionError):
            return default
    
    def get_bool(self, section, key, default=False):
        """Get a boolean config value"""
        try:
            return self.config.getboolean(section, key)
        except (KeyError, configparser.NoSectionError, ValueError):
            return default
    
    def get_int(self, section, key, default=0):
        """Get an integer config value"""
        try:
            return self.config.getint(section, key)
        except (KeyError, configparser.NoSectionError, ValueError):
            return default
    
    def get_float(self, section, key, default=0.0):
        """Get a float config value"""
        try:
            return self.config.getfloat(section, key)
        except (KeyError, configparser.NoSectionError, ValueError):
            return default
    
    def set(self, section, key, value):
        """Set a config value"""
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = str(value)
    
    def save(self):
        """Save config to file"""
        with open(self.config_path, 'w') as f:
            self.config.write(f)
    
    def run_setup_wizard(self):
        """Run the interactive setup wizard"""
        print("\n=== Terminal LLM Chat Setup Wizard ===")
        print("\nThis wizard will help you configure your Terminal LLM Chat settings.")
        
        # LLM Provider setup
        print("\n=== LLM Provider Configuration ===")
        provider_options = ["openai", "anthropic", "openrouter", "ollama"]
        
        print("\nAvailable LLM providers:")
        for i, provider in enumerate(provider_options, 1):
            print(f"  {i}. {provider}")
        
        while True:
            try:
                provider_choice = int(input("\nSelect provider (1-4): "))
                if 1 <= provider_choice <= len(provider_options):
                    provider = provider_options[provider_choice - 1]
                    break
                print(f"Please enter a number between 1 and {len(provider_options)}")
            except ValueError:
                print("Please enter a valid number")
        
        self.set("API", "PROVIDER", provider)
        
        # API Key (skip for ollama as it's local)
        if provider != "ollama":
            api_key = input(f"\nEnter your {provider} API key: ")
            self.set("API", "API_KEY", api_key)
        
        # Model selection
        default_models = {
            "openai": "gpt-3.5-turbo",
            "anthropic": "claude-3-opus",
            "openrouter": "openai/gpt-3.5-turbo",
            "ollama": "llama3"
        }
        
        model = input(f"\nEnter model name (default: {default_models[provider]}): ")
        if not model:
            model = default_models[provider]
        self.set("API", "MODEL", model)
        
        # UI theme selection
        print("\n=== UI Configuration ===")
        theme_options = ["green", "amber", "blue", "matrix", "custom"]
        
        print("\nAvailable themes:")
        for i, theme in enumerate(theme_options, 1):
            print(f"  {i}. {theme}")
        
        while True:
            try:
                theme_choice = int(input("\nSelect theme (1-5): "))
                if 1 <= theme_choice <= len(theme_options):
                    theme = theme_options[theme_choice - 1]
                    break
                print(f"Please enter a number between 1 and {len(theme_options)}")
            except ValueError:
                print("Please enter a valid number")
        
        self.set("UI", "THEME", theme)
        
        # Animation speed
        speed = input("\nEnter animation speed in ms (0-50, 0 to disable, default: 10): ")
        if not speed:
            speed = "10"
        self.set("UI", "ANIMATION_SPEED", speed)
        
        # Enable sounds
        sounds = input("\nEnable terminal sounds? (yes/no, default: yes): ").lower()
        self.set("UI", "ENABLE_SOUNDS", "true" if sounds in ["", "y", "yes"] else "false")
        
        # System prompt
        print("\n=== AI Configuration ===")
        default_prompt = "You are a helpful AI assistant responding in a terminal."
        system_prompt = input(f"\nEnter system prompt (default: '{default_prompt}'): ")
        if not system_prompt:
            system_prompt = default_prompt
        self.set("SYSTEM", "DEFAULT_PROMPT", system_prompt)
        
        # Temperature
        temp = input("\nEnter temperature (0.0-2.0, default: 0.7): ")
        if not temp:
            temp = "0.7"
        self.set("SYSTEM", "TEMPERATURE", temp)
        
        # Save configuration
        self.save()
        
        print("\n=== Configuration Complete ===")
        print(f"\nConfiguration saved to {self.config_path}")
        print("\nYou can start Terminal LLM Chat by running: terminal-chat")
