from app.simulation.dataset import generate_dataset


if __name__ == "__main__":

    generate_dataset(
        vehicles_count=50,
        steps=100,
    )
