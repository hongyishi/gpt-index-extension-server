"""API Entry point."""
from flask import Flask, request, jsonify
import os
import string
from langchain import LLMChain, OpenAI, PromptTemplate
from prompt_template import conv_prompt_template, identity_prompt_template
from pathlib import Path

application = Flask(__name__)

# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

@application.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    application.run()
