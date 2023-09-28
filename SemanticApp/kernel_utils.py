"""Kernel util functions"""
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion import (
    OpenAIChatCompletion,
)
from semantic_kernel.core_skills import ConversationSummarySkill

from SemanticApp import aiserviceconfig as aiconf

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
    semantic_kernel.import_skill(
        ConversationSummarySkill(kernel=semantic_kernel),
        skill_name="ConversationSummarySkill",
    )
    return semantic_kernel