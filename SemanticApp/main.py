"""
    Azure Function App to demonstrate Microsoft Semantic Kernel with Semantic and Native Functions
    Some of examples to run this functions
    {"prompt":"square root of 64?"}
    {"prompt":"multipley 5 times 3"}
"""
import logging
import json
import asyncio
from flask import Flask, request, Response

from semanticutil.kernel_utils import KernelUtil
#app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

app = Flask(__name__)


AI_PLUGIN_FILE  ="./ai-plugin/ai-plugin_az_func.json"

@app.get("/.well-known/ai-plugin.json")
def get_ai_plugin():
    """
    ChatGPT manifest file, ai-plugin.json; 
    It will look in the "".well-known" folder
    """
    logging.info("getting aiplugin file:%s",AI_PLUGIN_FILE)
    with open(AI_PLUGIN_FILE, "r", encoding="UTF-8") as file_read:
        text = file_read.read()
    return Response(text, status=200, mimetype="application/json")

@app.get("/openapi.yaml")
def get_openapi():
    """ ChatGPT will use this route to find our API specification, openapi.yaml"""
    logging.info("getting aiplugin file:%s",AI_PLUGIN_FILE)
    with open("./SemanticApp/openapi.yaml", "r", encoding="UTF-8") as file_read:
        text = file_read.read()
    return Response(text, status=200, mimetype="text/yaml")
 
@app.post("/skills/math")
def math_skill():
    """openai native function for multiple"""
    logging.info("Python HTTP trigger function for a request.")
    try:
        req_body = json.loads(request.data)
        prompt = req_body['prompt']
        kernel = KernelUtil.create_kernel_for_request()
        result = asyncio.run(KernelUtil.route_request(kernel,prompt))
        response_msg = {"result": str(result)}
        return Response(json.dumps(response_msg), status=200, mimetype="application/json")
    except ValueError as ex:
        response_msg = {"error": str(ex)}
        return Response(json.dumps(response_msg), status=500, mimetype="application/json")

if __name__ == "__main__":
    app.run()
