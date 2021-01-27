from os import environ, path
from prefect import Flow, unmapped, Parameter

# from prefect.environments import DaskKubernetesEnvironment
# from prefect.environments.storage import Docker
# from prefect.tasks.aws.secrets_manager import AWSSecretsManager

from prefectplayground.tasks import generate_list


def BasicFlow(generate_list_args={}):
    with Flow(
        name="basic_flow",
    ) as flow:
        members = generate_list(**generate_list_args)

        print(members)

    return flow


if __name__ == "__main__":
    BasicFlow().run()
