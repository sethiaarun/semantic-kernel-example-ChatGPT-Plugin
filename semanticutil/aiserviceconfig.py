"""AI Service configuration"""
from dataclasses import dataclass
from enum import Enum

import semantic_kernel as sk
from dotenv import dotenv_values

class AIServiceProvider(Enum):
    """List of AI Service provider"""
    OPENAI = "OPENAI"

@dataclass
class AIServiceConfig:
    """AI Service data class for the configuration"""
    llm_service: AIServiceProvider
    serviceid: str
    modelid:str
    apikey: str
    orgid: str = None
    endpoint: str = None
    

def dotenv_to_config()->AIServiceConfig:
    """load configuration from dot env file"""
    config = dotenv_values(".env")
    llm_service=config.get('LLM_SERVICE')
    if llm_service==AIServiceProvider.OPENAI.value:
        api_key,org_id = sk.openai_settings_from_dot_env()
        return AIServiceConfig(
            llm_service=AIServiceProvider.OPENAI,
            serviceid=config.get('SERVICE_ID'),
            modelid=config.get('MODEL_ID'),
            apikey=api_key,
            orgid=org_id,
            endpoint=None
        )
    else:
      raise ValueError("No valid llm service found")
      