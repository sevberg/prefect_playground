from prefect.storage import Docker
from prefect.run_configs import KubernetesRun
from prefect.executors.dask import DaskExecutor
from os import path

import flow_generator

# Fetch flow
flow = flow_generator.BasicFlow()

# Build and push image
module_dir = path.dirname(path.dirname(path.abspath(__file__)))


flow.storage = Docker(
    python_dependencies=[
        "numpy",
        "dask_kubernetes==0.11.0",
        "dask==2020.12.0",
        "distributed==2021.01.0",
    ],
    registry_url="registry.hub.docker.com/",
    image_name="sevberg/prefect_playground",
    image_tag="latest",
    files={
        path.join(
            module_dir, "requirements.txt"
        ): "/modules/prefect_playground/requirements.txt",
        path.join(module_dir, "README.md"): "/modules/prefect_playground/README.md",
        path.join(module_dir, "LICENSE"): "/modules/prefect_playground/LICENSE",
        path.join(module_dir, "setup.py"): "/modules/prefect_playground/setup.py",
        path.join(module_dir, ".version"): "/modules/prefect_playground/.version",
        path.join(
            module_dir, "prefectplayground"
        ): "/modules/prefect_playground/prefectplayground",
    },
    extra_dockerfile_commands=["RUN pip install -e /modules/prefect_playground"],
)


flow.run_config = KubernetesRun(
    cpu_request=2, memory_request="2G", env={"AWS_DEFAULT_REGION": "eu-central-1"}
)


def make_cluster(n_workers, image):
    """Start a fargate cluster using the same image as the flow run"""
    from dask_kubernetes import KubeCluster, make_pod_spec

    pod_spec = make_pod_spec(
        image=image,
        memory_limit="1900M",
        memory_request="1900M",
        cpu_limit=0.5,
        cpu_request=0.5,
    )

    return KubeCluster(pod_spec, n_workers=n_workers)


flow.executor = DaskExecutor(
    cluster_class=make_cluster,
    cluster_kwargs={"n_workers": 10, "image": flow.storage.name},
)

flow.register(project_name="prefect_playground", labels=["dev"])
