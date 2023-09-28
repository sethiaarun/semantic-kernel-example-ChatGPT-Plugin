"""
    Azure Function App to demonstrate Microsoft Semantic Kernel with Semantic and Native Functions
    Some of examples to run this functions
    {"prompt":"square root of 64?"}
    {"prompt":"multipley 5 times 3"}
"""
import logging
import json
import asyncio
from flask import Flask, request, Response, send_from_directory

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion import (
    OpenAIChatCompletion,
)
from semantic_kernel.core_skills import ConversationSummarySkill
from dotenv import dotenv_values

from plugins.MathPlugin.Math import Math
from plugins.OrchestratorPlugin.OrchestratorPlugin import Orchestrator
from SemanticApp import kernel_utils as ku
#app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

app = Flask(__name__)

@app.route("/.well-known/ai-plugin.json", methods=["GET"])
def get_ai_plugin():
    """
    ChatGPT manifest file, ai-plugin.json; 
    It will look in the "".well-known" folder
    """
    return send_from_directory('./.well-known/', 'ai-plugin.json', mimetype='text/yaml')

@app.route("/openapi.yaml", methods=["GET"])
def get_openapi():
    """ ChatGPT will use this route to find our API specification, openapi.yaml"""
    return send_from_directory('./SemanticApp', 'openapi.yaml', mimetype='text/yaml')
    
@app.post("/skills/math")
def math_skill():
    """openai native function for multiple"""
    logging.info("Python HTTP trigger function processed a request.")
    try:
        req_body = json.loads(request.data)
        prompt = req_body['prompt']
        kernel = ku.create_kernel_for_request()
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
