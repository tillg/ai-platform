from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
<<<<<<< HEAD
=======

>>>>>>> gitbutler/integration

def add_inner_working(
    original_inner_working: Dict[str, Any], titel: str, additional_inner_working
) -> Dict[str, Any]:
    new_inner_working = original_inner_working.copy()
    if isinstance(additional_inner_working, dict):
        new_inner_working[titel] = additional_inner_working.copy()
    else:
        # Assume additional_inner_working is an object with a __dict__ attribute
        new_inner_working[titel] = additional_inner_working.__dict__.copy()

    # # If the additional inner working has a list of inner workings, we need to add
    # them to the new inner working
    # if hasattr(new_inner_working[titel], "inner_working"):
    #     new_inner_working[titel] = new_inner_working[titel] +
    #       additional_inner_working["inner_working"]
    #     del new_inner_working[titel]["inner_working"]
    # logger.info(f"{new_inner_working=}")
    return new_inner_working
