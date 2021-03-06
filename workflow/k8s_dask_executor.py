from prefect.storage import Docker
from prefect.run_configs import KubernetesRun
from prefect.executors.dask import DaskExecutor
from os import path

import flow_generator

# Fetch flow
flow = flow_generator.BasicFlow()

# Build and push image
module_dir = path.dirname(path.dirname(path.abspath(__file__)))


def get_requirements(*extras):
    reqs = []
    for line in open(path.join(module_dir, "requirements.txt")):
        reqs.append(line[:-1])

    reqs.extend(extras)
    return reqs


flow.storage = Docker(
    python_dependencies=get_requirements(),
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
    extra_dockerfile_commands=[
        "RUN pip install --no-deps -e /modules/prefect_playground"
    ],
)

# Create run config
flow.run_config = KubernetesRun(
    cpu_request=2, memory_request="2G", env={"AWS_DEFAULT_REGION": "eu-central-1"}
)


# Create Dask Executor
def make_cluster(n_workers, image):
    """Start a cluster using the same image as the flow run"""
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

# Register flow
flow.register(project_name="prefect_playground", labels=["dev"])
