"""
    Azure Function App to demonstrate Microsoft Semantic Kernel with Semantic and Native Functions
    Some of examples to run this functions
    {"prompt":"square root of 64?"}
    {"prompt":"multipley 5 times 3"}
"""
import logging
import json
import time
from random import randint
from flask import Flask, request, Response, send_file

import asyncio
import httpx
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion import (
    OpenAIChatCompletion,
)
from semantic_kernel.core_skills import ConversationSummarySkill
from dotenv import dotenv_values

from plugins.MathPlugin.Math import Math
from plugins.OrchestratorPlugin.OrchestratorPlugin import Orchestrator

#app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

app = Flask(__name__)

def _openai_service() -> sk.Kernel:
    """Using native and semantic functions together with OpenAI and Semantic Kernel"""
    config = dotenv_values(".env")
    semantic_kernel = sk.Kernel()
    semantic_kernel.add_chat_service(
        "chat_completion",
        OpenAIChatCompletion(
            config.get("OPEN_AI__CHAT_COMPLETION_MODEL_ID", None),
            config.get("OPEN_AI__API_KEY", None),
            config.get("OPEN_AI__ORG_ID", None),
        ),
    )
    plugins_directory = "./plugins"
    # Import the semantic functions
    semantic_kernel.import_semantic_skill_from_directory(
        plugins_directory, "OrchestratorPlugin"
    )
    semantic_kernel.import_skill(
        ConversationSummarySkill(kernel=semantic_kernel),
        skill_name="ConversationSummarySkill",
    )
    return semantic_kernel

@app.route("/.well-known/ai-plugin.json", methods=["GET"])
def get_ai_plugin():
     """Well Known AI Plugin"""
     with open("./.well-known/ai-plugin.json", "r",encoding="UTF-8") as file_obj:
         text = file_obj.read()
         return Response(text, status=200, mimetype="text/json")

@app.route("/openapi.yaml", methods=["GET"])
def get_openapi():
    """get openai"""
    with open("./SemanticApp/openapi.yaml","r", encoding="UTF-8") as file_obj:
        text = file_obj.read()
        return Response(text, status=200, mimetype="text/yaml")

@app.post("/skills/math")
def math_skill():
    """openai native function for multiple"""
    logging.info("Python HTTP trigger function processed a request.")
    try:
        req_body = json.loads(request.data)
        prompt = req_body['prompt']
        kernel = _openai_service()
        # Import the native functions.
        kernel.import_skill(Math(), skill_name="MathPlugin")
        orchestrator_plugin = kernel.import_skill(
            Orchestrator(kernel), skill_name="OrchestratorPlugin"
        )
        result = asyncio.run(kernel.run_async(
            orchestrator_plugin["RouteRequest"], input_str=prompt
        ))
        response_msg = {"result": str(result)}
        return Response(json.dumps(response_msg), status=200, mimetype="application/json")
    except ValueError as ex:
        response_msg = {"error": str(ex)}
        return Response(json.dumps(response_msg), status=500, mimetype="application/json")

    
if __name__ == "__main__":
    app.run()