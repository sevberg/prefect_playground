from os import environ, path
from prefect import Flow, unmapped, Parameter

from prefectplayground.tasks import add_matrix, generate_list


def BasicFlow() -> Flow:
    with Flow(
        name="basic_flow",
    ) as flow:

        # Simple list generation task
        generate_list_n_members = Parameter("generate_list_n_members", default=100)
        generate_list_min_value = Parameter("generate_list_min_value", default=20)
        generate_list_max_value = Parameter("generate_list_max_value", default=30)
        generate_list_cycles = Parameter("generate_list_cycles", default=1)
        generate_list_seed = Parameter("generate_list_seed", default=0)

        members = generate_list(
            n_members=generate_list_n_members,
            min_value=generate_list_min_value,
            max_value=generate_list_max_value,
            cycles=generate_list_cycles,
            seed=generate_list_seed,
        )

        # Mapped task
        add_matrix_size = Parameter("add_matrix_size", default=5000)
        add_matrix_seed = Parameter("add_matrix_seed", default=1)

        member_means = add_matrix.map(
            cycles=members,
            seed=unmapped(add_matrix_seed),
            size=unmapped(add_matrix_size),
        )

    return flow


if __name__ == "__main__":
    BasicFlow().run()
