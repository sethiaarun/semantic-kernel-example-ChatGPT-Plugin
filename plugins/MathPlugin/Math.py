"""Math Native functions for Semantic Kernel"""
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
        """square root"""
        return str(math.sqrt(float(context["input"])))

    @sk_function(
        description="Multiply two numbers. When increasing by a percentage, don't forget to add 1 to the percentage.",
        name="multiply",
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
        name="add",
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

    @sk_function(
        description="Subtract two numbers together",
        name="subtract",
    )
    @sk_function_context_parameter(
        name="input",
        description="The first number to subtract from",
    )
    @sk_function_context_parameter(
        name="number2",
        description="The second number to subtract away",
    )
    def subtract(self, context: SKContext) -> str:
        """subtract two numbers"""
        return str(float(context["input"]) - float(context["number2"]))

    @sk_function(
        description="Divide two numbers together",
        name="divide",
    )
    @sk_function_context_parameter(
        name="input",
        description="The first number to divide from",
    )
    @sk_function_context_parameter(
        name="number2",
        description="The second number to divide by",
    )
    def divide(self, context: SKContext) -> str:
        """add two numbers"""
        return str(float(context["input"]) / float(context["number2"]))
