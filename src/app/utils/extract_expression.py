import ast
import re


def is_valid_expression(expr):
    try:
        ast.parse(expr)
        return True
    except Exception:
        return False


def extract_expression(text: str) -> str:
    text = text.lower().strip()

    # --------------------------------
    # Remove noise words
    # --------------------------------
    text = re.sub(r"\b(what is|calculate|evaluate|please|find|the)\b", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    # --------------------------------
    # Percentage
    # --------------------------------
    match = re.search(r"(\d+\.?\d*)\s*%\s*(of)?\s*(\d+\.?\d*)", text)
    if match:
        percent = match.group(1)
        number = match.group(3)
        return f"({percent}/100)*{number}"

    # --------------------------------
    # Geometry
    # --------------------------------
    geometry_patterns = [
        (r"area of circle radius (\d+)", r"pi*\1**2"),
        (r"circumference of circle radius (\d+)", r"2*pi*\1"),
        (r"diameter of circle radius (\d+)", r"2*\1"),
        (r"area of square side (\d+)", r"\1**2"),
        (r"perimeter of square side (\d+)", r"4*\1"),
        (r"volume of cube side (\d+)", r"\1**3"),
        (r"surface area of cube side (\d+)", r"6*\1**2"),
        (r"volume of sphere radius (\d+)", r"(4/3)*pi*\1**3"),
        (r"surface area of sphere radius (\d+)", r"4*pi*\1**2"),
    ]

    for pattern, formula in geometry_patterns:
        match = re.search(pattern, text)
        if match:
            return re.sub(pattern, formula, text)

    # --------------------------------
    # Factorial
    # --------------------------------
    text = re.sub(r"factorial of (\d+)", r"factorial(\1)", text)
    text = re.sub(r"(\d+)\s+factorial", r"factorial(\1)", text)

    # --------------------------------
    # Square root
    # --------------------------------
    text = re.sub(r"(square root of|square root|sqrt)\s+(\d+\.?\d*)", r"sqrt(\2)", text)

    # --------------------------------
    # Logarithms
    # --------------------------------
    # log = log10 (human expectation)
    text = re.sub(r"log10\s+of\s+(\d+\.?\d*)", r"log10(\1)", text)
    text = re.sub(r"log\s+of\s+(\d+\.?\d*)", r"log10(\1)", text)
    text = re.sub(r"ln\s+of\s+(\d+\.?\d*)", r"log(\1)", text)

    # --------------------------------
    # Trigonometry (convert degrees → radians)
    # --------------------------------
    text = re.sub(r"(sin|cos|tan)\s+(\d+\.?\d*)\s*degrees?", r"\1(radians(\2))", text)

    # If trig without degrees, assume degrees (human behavior)
    text = re.sub(r"\b(sin|cos|tan)\s+(\d+\.?\d*)", r"\1(radians(\2))", text)

    # --------------------------------
    # Arithmetic word conversion
    # --------------------------------
    text = text.replace("plus", "+")
    text = text.replace("minus", "-")
    text = text.replace("times", "*")
    text = text.replace("multiplied by", "*")
    text = text.replace("divide by", "/")

    # Replace power operator
    text = text.replace("^", "**")

    # --------------------------------
    # Final validation
    # --------------------------------
    if is_valid_expression(text):
        return text.strip()

    return None


def is_math(query: str) -> bool:
    query = query.lower()

    if re.search(r"\d+\s*[\+\-\*/\^%]\s*\d+", query):
        return True

    if re.search(r"\d+\s*%\s*(of)?\s*\d+", query):
        return True

    math_words = [
        # Basic arithmetic
        "add",
        "sum",
        "plus",
        "minus",
        "subtract",
        "multiply",
        "product",
        "divide",
        "division",
        "times",
        "mod",
        "modulo",
        "remainder",
        # Powers & roots
        "power",
        "raised to",
        "square",
        "cube",
        "sqrt",
        "square root",
        "cube root",
        # Logs & exponential
        "log",
        "log10",
        "ln",
        "exponential",
        "exp",
        # Trigonometry
        "sin",
        "cos",
        "tan",
        "asin",
        "acos",
        "atan",
        "radians",
        "degrees",
        "trigonometry",
        # Constants
        "pi",
        "e",
        # Factorial & number theory
        "factorial",
        "gcd",
        "lcm",
        # Geometry 2D
        "area",
        "perimeter",
        "circumference",
        "circle",
        "radius",
        "diameter",
        "square",
        "rectangle",
        "triangle",
        "trapezium",
        "parallelogram",
        "base",
        "height",
        "side",
        # Geometry 3D
        "volume",
        "surface area",
        "sphere",
        "cylinder",
        "cone",
        "cube",
        "cuboid",
        # Advanced
        "hypotenuse",
        "pythagoras",
        "geometry",
        "math",
        "calculate",
        "compute",
    ]

    if any(word in query for word in math_words) and re.search(r"\d", query):
        return True

    return False


# 0-9: numbers
# + - * / (): math operators
# '-' must be escaped in regex because it is special inside character classes

# Regex: [0-9+\-*/()]
# Matches calculation intent like "calculate 10/2 please"
