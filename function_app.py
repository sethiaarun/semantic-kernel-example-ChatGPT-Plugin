"""
    Azure Function App to demonstrate Microsoft Semantic Kernel with Semantic and Native Functions
    Some of examples to run this functions
    {"prompt":"square root of 64?"}
    {"prompt":"multipley 5 times 3"}
"""
import logging
import json
import azure.functions as func

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion import (
    OpenAIChatCompletion,
)
from semantic_kernel.core_skills import ConversationSummarySkill
from dotenv import dotenv_values

from plugins.MathPlugin.Math import Math
from plugins.OrchestratorPlugin.OrchestratorPlugin import Orchestrator

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


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


@app.route(route="mathfunctions")
async def mathfunctions(req: func.HttpRequest) -> func.HttpResponse:
    """openai native function for multiple"""
    logging.info("Python HTTP trigger function processed a request.")
    try:
        req_body = req.get_json()
        prompt = req_body.get("prompt")
        kernel = _openai_service()
        # Import the native functions.
        kernel.import_skill(Math(), skill_name="MathPlugin")
        orchestrator_plugin = kernel.import_skill(
            Orchestrator(kernel), skill_name="OrchestratorPlugin"
        )
        result = await kernel.run_async(
            orchestrator_plugin["RouteRequest"], input_str=prompt
        )
        response_msg = {"result": str(result)}
        return func.HttpResponse(str(result), status_code=200)
    except ValueError as ex:
        response_msg = {"error": str(ex)}
        return func.HttpResponse(json.dumps(response_msg), status_code=500)
