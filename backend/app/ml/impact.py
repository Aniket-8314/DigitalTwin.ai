def downstream_nodes(
    graph,
    station_id: str,
    max_depth: int = 4,
) -> list[str]:

    visited = set()
    result = []

    current = [station_id]

    for _ in range(max_depth):

        next_nodes = []

        for node_id in current:

            for edge in graph.edges:

                if edge.source != node_id:
                    continue

                target = edge.target

                if target in visited:
                    continue

                visited.add(target)

                result.append(target)

                next_nodes.append(target)

        current = next_nodes

        if not current:
            break

    return result
