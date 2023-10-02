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

        get_numbers = self._kernel.skills.get_function(
            "OrchestratorPlugin", "GetNumbers"
        )

        get_number_context = (
            await self._kernel.run_async(get_numbers, input_str=request)
        ).result
        numbers = json.loads(get_number_context)

        if intent == "Sqrt":
            square_root = self._kernel.skills.get_function("MathPlugin", "Sqrt")
            sqrt_results = await self._kernel.run_async(
                square_root, input_str=numbers["number1"]
            )
            return sqrt_results["input"]
        elif intent == "Multiply":
            multiply = self._kernel.skills.get_function("MathPlugin", "Multiply")
            context_variable = ContextVariables()
            context_variable["input"] = numbers["number1"]
            context_variable["number2"] = numbers["number2"]
            multiply_results = await self._kernel.run_async(
                multiply, input_vars=context_variable
            )
            return multiply_results["input"]
        elif intent == "Add":
            add = self._kernel.skills.get_function("MathPlugin", "Add")
            context_variable = ContextVariables()
            context_variable["input"] = numbers["number1"]
            context_variable["number2"] = numbers["number2"]
            add_results = await self._kernel.run_async(
                add, input_vars=context_variable
            )
            return add_results["input"]
        else:
            return "I'm sorry, I don't understand."
