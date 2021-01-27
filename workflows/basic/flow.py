from os import environ, path
from prefect import Flow, unmapped, Parameter

# from prefect.environments import DaskKubernetesEnvironment
# from prefect.environments.storage import Docker
# from prefect.tasks.aws.secrets_manager import AWSSecretsManager

from prefectplayground.tasks import generate_list


def BasicFlow():
    with Flow(
        name="basic_flow",
    ) as flow:

        # Simple list generation task
        generate_list_n_members = Parameter("generate_list_n_members", default=100)
        generate_list_min_value = Parameter("generate_list_min_value", default=1000)
        generate_list_max_value = Parameter("generate_list_max_value", default=2000)
        generate_list_cycles = Parameter("generate_list_cycles", default=1)
        generate_list_seed = Parameter("generate_list_seed", default=None)

        members = generate_list(
            n_members=generate_list_n_members,
            min_value=generate_list_min_value,
            max_value=generate_list_max_value,
            cycles=generate_list_cycles,
            seed=generate_list_seed,
        )

        print(members)

    return flow


if __name__ == "__main__":
    BasicFlow().run()
