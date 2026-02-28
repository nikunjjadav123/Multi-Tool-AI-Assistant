from app.graph_agent import router


def test_math_route():
    state = {"user_input": "2+2"}
    assert router(state) == "math_node"


def test_weather_route():
    state = {"user_input": "weather in delhi"}
    assert router(state) == "weather_node"
