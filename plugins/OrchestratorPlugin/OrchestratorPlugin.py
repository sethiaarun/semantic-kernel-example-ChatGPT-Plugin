"""Semantic Kernel Orchestrator using Native and Semantic Functions"""
import json
from semantic_kernel import ContextVariables, Kernel
from semantic_kernel.skill_definition import sk_function
from semantic_kernel.orchestration.sk_context import SKContext


class Orchestrator:
    """Orchestrator class"""

    def __init__(self, kernel: Kernel):
        self._kernel = kernel

    @sk_function(
            description="Extracts numbers from JSON",
            name="ExtractNumbersFromJson"
    )
    def extract_numbers_from_json(self, context: SKContext):
        """Mative function - the input variable is coming from the pipeline, here it is from the GetNumber semantic function"""
        numbers = json.loads(context["input"])

        # Loop through numbers and add them to the context
        for key, value in numbers.items():
            if key == "number1":
                # Add the first number to the input variable
                context["input"] = str(value)
            else:
                # Add the rest of the numbers to the context
                context[key] = str(value)

        return context

    @sk_function(
        description="Routes the request to the appropriate function",
        name="RouteRequest",
    )
    async def route_request(self, context: SKContext) -> str:
        """route request"""
        # Save the original user request
        request = context["input"]

        # Add the list of available functions to the context variables
        context_variable = ContextVariables()
        context_variable["input"] = request
        context_variable["options"] = "Sqrt, Multiply, Add"

        # Retrieve the intent from the user request
        # From given input get the intent, it provides list of Options for the LLM to choose from
        get_intent = self._kernel.skills.get_function("OrchestratorPlugin", "GetIntent")
        intent = (
            await self._kernel.run_async(get_intent, input_vars=context_variable)
        ).result.strip()

        # Prepare the functions to be called in the pipeline
        get_numbers = self._kernel.skills.get_function(
            "OrchestratorPlugin", "GetNumbers"
        )
        # extract numbers from the response we got from GetNumbers
        extract_numbers_from_json = self._kernel.skills.get_function(
            "OrchestratorPlugin", "ExtractNumbersFromJson"
        )
        create_response = self._kernel.skills.get_function(
            "OrchestratorPlugin", "CreateResponse"
        )

        if intent == "Sqrt":
            math_function  = self._kernel.skills.get_function("MathPlugin", "Sqrt")
        elif intent == "Multiply":
            math_function = self._kernel.skills.get_function("MathPlugin", "Multiply")
        elif intent == "Add":
            math_function = self._kernel.skills.get_function("MathPlugin", "Add")
        else:
            return "I'm sorry, I don't understand."

         # Create a new context object with the original request
        pipeline_variables = ContextVariables()
        pipeline_variables["original_request"] = request
        pipeline_variables["input"] = request

        # Run the functions in a pipeline
        output = await self._kernel.run_async(
            get_numbers,
            extract_numbers_from_json,
            math_function,
            create_response,
            input_vars=pipeline_variables,
        )

        return output["input"]