#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="terminal-llm-chat",
    version="0.1.0",
    author="Terminal LLM Chat Team",
    author_email="example@example.com",
    description="A terminal-themed LLM chatbot with a retro interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/syanhg/terminal-llm-chat",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "rich>=10.0.0",
        "tiktoken>=0.3.0",
        "configparser>=5.0.0",
    ],
    entry_points={
        "console_scripts": [
            "terminal-chat=terminal_llm_chat.main:main",
        ],
    },
)
