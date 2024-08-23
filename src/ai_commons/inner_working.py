from typing import Any, Dict, List, Optional


def add_inner_working(
        original_inner_working: Dict[str, Any], titel: str, additional_inner_working) -> Dict[str, Any]:
    new_inner_working = original_inner_working.copy()
    new_inner_working[titel] = additional_inner_working
    return new_inner_working
