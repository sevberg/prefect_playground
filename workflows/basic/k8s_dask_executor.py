import prefect
from prefect.storage import Docker
from prefect.run_configs import ECSRun
from prefect.executors.dask import DaskExecutor
from os import path
from datetime import datetime

# from dask_cloudprovider.aws import FargateCluster

import flow_generator

# Fetch flow
flow = flow_generator.BasicFlow()

# Build and push image
module_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


flow.storage = Docker(
    python_dependencies=[
        "numpy",
        "dask_kubernetes==0.11.0",
        "dask==2020.12.0",
        # "dask-cloudprovider[aws]",
    ],
    registry_url="public.ecr.aws/m5p2l3e5/",
    image_name="prefect_playground",
    # image_tag=datetime.now().strftime("%Y%m%d_%H%M%S"),  # Unique tag avoids AWS caching
    image_tag="latest",
    files={
        path.join(
            module_dir, "requirements.txt"
        ): "/modules/prefect_playground/requirements.txt",
        path.join(module_dir, "README.md"): "/modules/prefect_playground/README.md",
        path.join(module_dir, "setup.py"): "/modules/prefect_playground/setup.py",
        path.join(module_dir, ".version"): "/modules/prefect_playground/.version",
        path.join(
            module_dir, "prefectplayground"
        ): "/modules/prefect_playground/prefectplayground",
    },
    extra_dockerfile_commands=["RUN pip install -e /modules/prefect_playground"],
)

flow.run_config = ECSRun(
    task_role_arn="arn:aws:iam::495775544086:role/ECS-task-execution-role",
    image="prefecthq/prefect:0.14.5",
    memory="2048",
    cpu="1024",
)

# flow.run_config = KubernetesRun(
#     cpu_request=2, memory_request="2Gi", env={"AWS_DEFAULT_REGION": "eu-central-1"}
# )

# flow.run_config = prefect.run_configs.L

# flow.run_config = KubernetesRun(
#     job_template_path="my_custom_template.yaml"
# )


# def make_cluster(n_workers, image):
#     """Start a fargate cluster using the same image as the flow run"""
#     from dask_kubernetes import KubeCluster, make_pod_spec

#     pod_spec = make_pod_spec(
#         # image=image,
#         image = 'daskdev/dask:latest',
#         memory_limit="3G",
#         memory_request="3G",
#         cpu_limit=1,
#         cpu_request=1,
#         # env={'EXTRA_PIP_PACKAGES': 'fastparquet git+https://github.com/dask/distributed'}
#     )

#     return KubeCluster(pod_spec, n_workers=n_workers)


def make_cluster(n_workers, image):
    """Start a fargate cluster using the same image as the flow run"""

    # return FargateCluster(
    #     n_workers=n_workers, image=image, region_name="eu-central-1"
    # )  # prefect.context.image)
    from dask_cloudprovider.aws import ECSCluster

    cluster = ECSCluster(
        run_task_kwargs={
            "cluster": "accure_compute_2xlarge_Batch_5e1ca55c-c98e-36f3-a199-d76f2f96caa4",
        },
        cluster_arn="arn:aws:ecs:eu-central-1:495775544086:cluster/accure_compute_2xlarge_Batch_5e1ca55c-c98e-36f3-a199-d76f2f96caa4",
        image=image,
        n_workers=n_workers,
    )


flow.executor = DaskExecutor(
    # cluster_class=make_cluster,
    # cluster_kwargs={"n_workers": 60, "image": flow.storage.name},
)

flow.register(project_name="prefect_playground", labels=["dev"])
# flow.run()
