from app.simulation.generator import create_factory
from app.twin.graph_builder import build_process_graph


factory = create_factory()

graph = build_process_graph(factory)


print("DIGITALTWIN.AI")
print("Process Graph")
print("=" * 45)


print("Nodes:", len(graph.nodes))

print("Edges:", len(graph.edges))


print("\nS14 downstream:")

print(graph.get_downstream("S14"))


print("\nS14 upstream:")

print(graph.get_upstream("S14"))


print("\nB15 downstream:")

print(graph.get_downstream("B15"))


print("\nB15 upstream:")

print(graph.get_upstream("B15"))
