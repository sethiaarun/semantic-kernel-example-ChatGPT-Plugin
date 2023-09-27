import math
from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)
from semantic_kernel.orchestration.sk_context import SKContext

class Math:
    """Math Native Functions"""
    @sk_function(
        description="Takes the square root of a number",
        name="Sqrt",
        input_description="The value to take the square root of",
    )
    def square_root(self, context: SKContext) -> str:
        return str(math.sqrt(float(context["input"])))

    @sk_function(
        description="Multiplies two numbers together",
        name="Multiply",
    )
    @sk_function_context_parameter(
        name="input",
        description="The first number to multiply",
    )
    @sk_function_context_parameter(
        name="number2",
        description="The second number to multiply",
    )
    def multiply(self, context: SKContext) -> str:
        """multiply two numbers"""
        return str(float(context["input"]) * float(context["number2"]))

    @sk_function(
        description="Add two numbers together",
        name="Add",
    )
    @sk_function_context_parameter(
        name="input",
        description="The first number",
    )
    @sk_function_context_parameter(
        name="number2",
        description="The second number",
    )
    def add(self, context: SKContext) -> str:
        """add two numbers"""
        return str(float(context["input"]) + float(context["number2"]))