from pydantic import BaseModel, Field
from langchain_core.tools import tool
import math


class CalculatorInput(BaseModel):
    expression: str = Field(description="Mathematical expression like 2+2, sqrt(16)")


@tool(args_schema=CalculatorInput)
def calculator(expression: str) -> str:
    """Evaluate math expression safely"""

    print("Calculator Tool Executed")
    
    allowed_names = {
        "pi": math.pi,
        "e": math.e,
        "sqrt": math.sqrt,
        "pow": math.pow,
        "exp": math.exp,
        "log": math.log10,
        "ln": math.log,
        "log10": math.log10,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "radians": math.radians,
        "degrees": math.degrees,
        "abs": abs,
        "round": round,
        "floor": math.floor,
        "ceil": math.ceil,
        "factorial": math.factorial,
    }

    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)

        if isinstance(result, float):
            result = round(result, 6)
            if result.is_integer():
                result = int(result)

        return str(result)

    except Exception as e:
        print("Calculator error:", e)
        return "error"