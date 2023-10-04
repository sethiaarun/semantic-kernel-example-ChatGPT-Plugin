#pylint: disable=W0223 
import logging
import signal
import json
import asyncio
import tornado
import tornado_swirl as swirl
from tornado import gen
from tornado.options import define, options

from semanticutil.kernel_utils import KernelUtil


define("port", default=8888, help="run on the given port", type=int)

@swirl.schema
class ErrorResponse(object):
    """Error response object.

    Properties:
        code (int) -- Required.  Error code.
        error (string) -- Error description.
    """
    pass

@swirl.schema
class MathSkillBody(object):
    """Math Skill result object.

    Properties:
        prompt (string) -- Requested user prompt
    """
    pass

@swirl.schema
class MathResult(object):
    """Math Skill result object.

    Properties:
        result (string) -- Math skill result in json format string
    """
    pass

@swirl.restapi('/.well-known/ai-plugin.json')
class AIPluginHandler(tornado.web.RequestHandler):
    """ai-pluin handler"""
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def get(self):
        """ChatGPT manifest file, ai-plugin.json

        200 Response:
            x (string) -- openapi manifest in application/json format

        """
        logging.info("/.well-known/ai-plugin.json")
        with open("./.well-known/ai-plugin.json", "r", encoding="UTF-8") as file_read:
            text = file_read.read()
            return self.write(text)

@swirl.restapi('/openapi.yaml')
class OpenAPIHandler(tornado.web.RequestHandler):
    """open api handler"""
    def set_default_headers(self):
        self.set_header("Content-Type", 'text/yaml')

    def get(self):
        """ChatGPT will use this route to find our API specification, openapi.yaml
        
        200 Response:
            x (string) -- openapi API specification in text/yaml format

        """
        logging.info("/openapi.yaml")
        with open("./SemanticApp/openapi.yaml", "r", encoding="UTF-8") as file_read:
            text = file_read.read()
            return self.write(text)

@swirl.restapi('/skills/math')
class MathSkill(tornado.web.RequestHandler):
    """Math skill api"""
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    @gen.coroutine
    def post(self):
        """Microsoft Semantic Math Plugin Example Using OpenAI 

        Request Body:
            test (MathSkillBody) -- Required.  The user prompt like what is square root of 144?
        
        200 Response:
            test (MathResult) -- Response with initial request
        
        Error Responses:
            500 (ErrorResponse) -- Internal Server Error.
        """
        logging.info("****************************** Math skill request **************************** ")
        try:
            req_body = json.loads(self.request.body)
            logging.info("request body:%s",req_body)
            prompt = req_body['prompt']
            kernel = KernelUtil.create_kernel_for_request()
            result = yield KernelUtil.route_request(kernel,prompt)
            response_msg = {"result": str(result)}
            self.set_status(200)
            return self.write(json.dumps(response_msg))
        except ValueError as ex:
            response_msg = {"code":"500","error": str(ex)}
            self.set_status(500)
            return self.write(json.dumps(response_msg))



async def main():
    """main function"""
    swirl.describe(title="Microsoft Semantic ChatGPT Plugin", description="Example API for Math Skills Plugin")
    app = swirl.Application(swirl.api_routes())
    app.listen(options.port)
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()
    

if __name__ == "__main__":
    asyncio.run(main())