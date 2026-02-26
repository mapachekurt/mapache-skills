"""
Configuration for agent
"""

import os
from adk.models import Gemini

# Model Configuration
MODEL = Gemini(
    model_name="gemini-2.0-flash-exp",
    temperature=0.7,
    top_p=0.9,
    max_output_tokens=8192
)

# Agent Configuration
AGENT_NAME = "search-bot"
AGENT_DESCRIPTION = "Performs web searches and returns summaries"

# Environment
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
