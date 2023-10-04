"""Kernel util functions"""

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion import (
    OpenAIChatCompletion,
)
from semantic_kernel.core_skills import ConversationSummarySkill

from semanticutil import aiserviceconfig as aiconf
from plugins.MathPlugin.Math import Math
from plugins.OrchestratorPlugin.OrchestratorPlugin import Orchestrator

class KernelUtil:
    """Kernel util class to load Kernel and required plugins and functions"""
    @staticmethod
    def create_kernel_for_request()->sk.Kernel:
        """create kernel for the request"""
        semantic_kernel = sk.Kernel()
        ai_service_config = aiconf.dotenv_to_config()
        if ai_service_config.llm_service==aiconf.AIServiceProvider.OPENAI:
            if ai_service_config.serviceid=='chat-completion':
                semantic_kernel.add_chat_service(
                    "chat_completion",
                    OpenAIChatCompletion(
                        ai_service_config.modelid,
                        ai_service_config.apikey,
                        ai_service_config.orgid
                        ),
                )
            else:
                raise ValueError("invalid service for OpenAI")
        else:
            raise ValueError("invalid LLM service")
        
        plugins_directory = "./plugins"
        # Import the semantic functions
        semantic_kernel.import_semantic_skill_from_directory(
            plugins_directory, "OrchestratorPlugin"
        )
        # Import the native functions.
        semantic_kernel.import_skill(Math(), skill_name="MathPlugin")
        # passing the kernel to the Orchestrator object will allow the Orchestrator object to access the 
        # kernel so it can run the GetIntent, GetNumbers, Sqrt, and Multiply functions
        semantic_kernel.import_skill(
            ConversationSummarySkill(kernel=semantic_kernel),
            skill_name="ConversationSummarySkill",
        )
        return semantic_kernel
    
    @staticmethod
    async def route_request(semantic_kernel: sk.Kernel, prompt: str)->str:
        """route request using RouteRequest plugin"""
        orchestrator_plugin = semantic_kernel.import_skill(
            Orchestrator(semantic_kernel), skill_name="OrchestratorPlugin"
        )
        result = await semantic_kernel.run_async(
            orchestrator_plugin["RouteRequest"], input_str=prompt
        )
        return str(result)
