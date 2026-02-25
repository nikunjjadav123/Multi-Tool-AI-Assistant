from graph_agent import graph

state = graph.get_state(
    config={"configurable": {"thread_id": "user_1"}}
)

print("\nRecovered State:\n")
print(state)