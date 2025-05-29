#!/usr/bin/env python3

import json
import requests
from typing import Dict, List, Tuple, Optional

class LLMProvider:
    def __init__(self, config):
        self.config = config
        self.provider = config.get("API", "PROVIDER", "openai")
        self.api_key = config.get("API", "API_KEY", "")
        self.model = config.get("API", "MODEL", "gpt-3.5-turbo")
        self.system_prompt = config.get("SYSTEM", "DEFAULT_PROMPT", "You are a helpful AI assistant.")
        self.temperature = config.get_float("SYSTEM", "TEMPERATURE", 0.7)
        self.max_tokens = config.get_int("SYSTEM", "MAX_TOKENS", 2000)
    
    def set_model(self, model_name):
        """Set the active model"""
        self.model = model_name
    
    def set_system_prompt(self, prompt):
        """Set the system prompt"""
        self.system_prompt = prompt
    
    def get_available_models(self) -> List[str]:
        """Get a list of available models from the provider"""
        if self.provider == "openai":
            return self._get_openai_models()
        elif self.provider == "anthropic":
            return self._get_anthropic_models()
        elif self.provider == "openrouter":
            return self._get_openrouter_models()
        elif self.provider == "ollama":
            return self._get_ollama_models()
        else:
            return [self.model]  # Return current model as fallback
    
    def _get_openai_models(self) -> List[str]:
        """Get available OpenAI models"""
        try:
            url = "https://api.openai.com/v1/models"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # Filter for chat models
            chat_models = [model["id"] for model in data["data"] 
                          if model["id"].startswith(("gpt-")) and 
                          not model["id"].endswith(("instruct"))]
            return sorted(chat_models)
        except Exception as e:
            print(f"Error fetching OpenAI models: {str(e)}")
            return ["gpt-3.5-turbo", "gpt-4"]
    
    def _get_anthropic_models(self) -> List[str]:
        """Get available Anthropic models"""
        # Anthropic doesn't have a models endpoint in their API v1
        # So we return a static list of known models
        return [
            "claude-3-opus",
            "claude-3-sonnet",
            "claude-3-haiku",
            "claude-2.1",
            "claude-2.0",
            "claude-instant-1.2"
        ]
    
    def _get_openrouter_models(self) -> List[str]:
        """Get available OpenRouter models"""
        try:
            url = "https://openrouter.ai/api/v1/models"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            return [model["id"] for model in data["data"]]
        except Exception as e:
            print(f"Error fetching OpenRouter models: {str(e)}")
            return ["openai/gpt-3.5-turbo", "anthropic/claude-3-opus"]
    
    def _get_ollama_models(self) -> List[str]:
        """Get available Ollama models"""
        try:
            url = "http://localhost:11434/api/tags"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            return [model["name"] for model in data["models"]]
        except Exception as e:
            print(f"Error fetching Ollama models: {str(e)}")
            return ["llama3", "mistral", "gemma"]
    
    def get_completion(self, messages: List[Dict], stream=True) -> str:
        """Get completion from the LLM provider"""
        if self.provider == "openai":
            return self._get_openai_completion(messages, stream)
        elif self.provider == "anthropic":
            return self._get_anthropic_completion(messages, stream)
        elif self.provider == "openrouter":
            return self._get_openrouter_completion(messages, stream)
        elif self.provider == "ollama":
            return self._get_ollama_completion(messages, stream)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _get_openai_completion(self, messages: List[Dict], stream=True) -> str:
        """Get completion from OpenAI API"""
        # Placeholder implementation - in a real application, this would
        # handle streaming responses properly
        if not self.api_key:
            return "ERROR: OpenAI API key not configured. Run --setup to configure."
        
        # Dummy implementation for example purposes
        prompt = messages[-1]["content"] if messages else ""
        return f"This is a simulated OpenAI response to: {prompt}"
    
    def _get_anthropic_completion(self, messages: List[Dict], stream=True) -> str:
        """Get completion from Anthropic API"""
        # Placeholder implementation
        if not self.api_key:
            return "ERROR: Anthropic API key not configured. Run --setup to configure."
        
        # Dummy implementation for example purposes
        prompt = messages[-1]["content"] if messages else ""
        return f"This is a simulated Anthropic response to: {prompt}"
    
    def _get_openrouter_completion(self, messages: List[Dict], stream=True) -> str:
        """Get completion from OpenRouter API"""
        # Placeholder implementation
        if not self.api_key:
            return "ERROR: OpenRouter API key not configured. Run --setup to configure."
        
        # Dummy implementation for example purposes
        prompt = messages[-1]["content"] if messages else ""
        return f"This is a simulated OpenRouter response to: {prompt}"
    
    def _get_ollama_completion(self, messages: List[Dict], stream=True) -> str:
        """Get completion from Ollama API"""
        # Placeholder implementation
        try:
            # Dummy implementation for example purposes
            prompt = messages[-1]["content"] if messages else ""
            return f"This is a simulated Ollama response to: {prompt}"
        except Exception as e:
            return f"ERROR: Could not connect to Ollama. Make sure it's running locally: {str(e)}"
