from pkgutil import iter_modules
import logging
from typing import List

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def list_submodules(module) -> List[str]:
    submodules = []
    for submodule in iter_modules(module.__path__):
        submodules.append(submodule.name)
    return submodules

