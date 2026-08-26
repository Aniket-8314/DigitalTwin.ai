from dataclasses import dataclass, field


@dataclass
class ProcessNode:
    node_id: str
    node_type: str


@dataclass
class ProcessEdge:
    source: str
    target: str


@dataclass
class ProcessGraph:
    nodes: dict[str, ProcessNode] = field(default_factory=dict)

    edges: list[ProcessEdge] = field(default_factory=list)

    def add_node(
        self,
        node_id: str,
        node_type: str,
    ) -> None:

        self.nodes[node_id] = ProcessNode(
            node_id=node_id,
            node_type=node_type,
        )

    def add_edge(
        self,
        source: str,
        target: str,
    ) -> None:

        self.edges.append(
            ProcessEdge(
                source=source,
                target=target,
            )
        )

    def get_downstream(
        self,
        node_id: str,
    ) -> list[str]:

        return [edge.target for edge in self.edges if edge.source == node_id]

    def get_upstream(
        self,
        node_id: str,
    ) -> list[str]:

        return [edge.source for edge in self.edges if edge.target == node_id]
