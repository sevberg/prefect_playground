from prefect.storage import Docker
from prefect.run_configs import KubernetesRun
from prefect.executors.dask import DaskExecutor
from os import path
from datetime import datetime

import flow_generator

# Fetch flow
flow = flow_generator.BasicFlow()

# Build and push image
module_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


flow.storage = Docker(
    python_dependencies=[
        "numpy",
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

flow.run_config = KubernetesRun(
    cpu_request=2, memory_request="2Gi", env={"SOME_VAR": "value"}
)


flow.executor = DaskExecutor(cluster_kwargs={"n_workers": 5, "threads_per_worker": 1})

flow.register(project_name="prefect_playground", labels=["dev"])
