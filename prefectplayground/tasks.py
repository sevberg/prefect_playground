from prefect import task
import numpy as np
from typing import List, Sized


@task(log_stdout=True)
def generate_list(
    n_members: int = 100,
    min_value: int = 1000,
    max_value: int = 2000,
    cycles: int = 1,
    seed: int = None,
) -> List[int]:
    """Generate a list of length `n_members` between `min_value` and `max_value`.

    `cycles` can be used to increase runtime"""

    if seed is not None:
        np.random.seed(seed)

    for _ in range(cycles):
        output = np.random.choice(np.arange(min_value, max_value + 1), size=n_members)

    return output.tolist()
