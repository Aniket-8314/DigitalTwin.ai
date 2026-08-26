from app.twin.factory import Factory
from app.twin.graph import ProcessGraph


def build_process_graph(
    factory: Factory,
) -> ProcessGraph:

    graph = ProcessGraph()

    # --------------------------------
    # Add station nodes
    # --------------------------------

    for station in factory.stations:

        graph.add_node(
            station.station_id,
            "station",
        )

    # --------------------------------
    # Add buffer nodes
    # --------------------------------

    for buffer in factory.buffers:

        graph.add_node(
            buffer.buffer_id,
            "buffer",
        )

    # --------------------------------
    # Connect stations
    # --------------------------------

    for number in range(1, 31):

        current = f"S{number:02d}"

        if number < 30:

            next_station = f"S{number + 1:02d}"

            graph.add_edge(
                current,
                next_station,
            )

    # --------------------------------
    # Connect buffers
    # --------------------------------

    for position in [5, 10, 15, 20, 25]:

        station_id = f"S{position:02d}"

        buffer_id = f"B{position:02d}"

        next_station = f"S{position + 1:02d}"

        # Remove direct station-to-station
        # relationship across this boundary.

        graph.edges = [
            edge
            for edge in graph.edges
            if not (edge.source == station_id and edge.target == next_station)
        ]

        graph.add_edge(
            station_id,
            buffer_id,
        )

        graph.add_edge(
            buffer_id,
            next_station,
        )

    return graph
