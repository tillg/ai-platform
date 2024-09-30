import json
import logging
import os
from typing import Dict, Optional
from utils.robust_jsonify import robust_jsonify
from utils.utils import get_now_as_string
from pydantic import validate_call
from jinja2 import Environment, BaseLoader, FileSystemLoader
import ai_commons.constants as constants

logger = logging.getLogger(__name__)

@validate_call
def write_dict_to_file(*, dictionary: Dict, full_filename: str) -> Dict:
    """Writes a dictionary to a file. Also updates the _stats element."""
    if not isinstance(dictionary, dict):
        raise TypeError("Expected a dictionary, but got a " +
                        str(type(dictionary)))
    dictionary.setdefault("_stats", {"lastWritten": get_now_as_string()})
    dictionary["_stats"]["lastWritten"] = get_now_as_string()
    dictionary["_stats"]["counter"] = len(dictionary) - 1
    stats = dictionary["_stats"]
    del dictionary["_stats"]
    dictionary = dict(sorted(dictionary.items()))
    sorted_dictionary = {"_stats": stats, **dictionary}
    dict_dump = robust_jsonify(sorted_dictionary, sort_keys=False, indent=2)

    # Make sure that the directory in which we want to write exists.
    directory = os.path.dirname(os.path.abspath(full_filename))
    try:
        os.makedirs(directory)
    except FileExistsError:
        # directory already exists, so no need to create it - all good
        pass

    with open(full_filename, 'w') as file:
        file.write(dict_dump)
    return sorted_dictionary


def read_dict_from_json_file(*, full_filename: str, skip_file_not_found=True) -> Dict:
    """Reads a dictionary from a file. Checks that the dictionary read has a _stats.lastWritten entry."""
    data = {}
    try:
        with open(full_filename, "r+") as file:
            data = json.load(file)
            if data is None:
                return {}
            if data.get("_stats", {}).get("lastWritten") is None:
                logger.warning(
                    f"Read file {full_filename} successfully but does not contain _stats.lastWritten.")
            return data
    except IOError as e:
        if not skip_file_not_found:
            logger.error(f"Could not open file {full_filename}")
            raise e
        else:
            logger.warning(f"Could not open file {
                        full_filename} - returning empty dict.")
    return data


def read_dict_from_template_file(*, full_filename: str, skip_file_not_found=True) -> Dict:
    """Reads a dictionary from a file and replaces keys with the variables."""
    template_filename = full_filename + ".jinja"

    # Check if this file exists
    if not os.path.exists(template_filename):
        return read_dict_from_json_file(full_filename=full_filename, skip_file_not_found=skip_file_not_found)
    
    data = {}
    try:
        template_dir = os.path.dirname(template_filename)
        template_name = os.path.basename(template_filename)
        template = Environment(loader=FileSystemLoader(template_dir)).get_template(template_name)
        constants_dict = {key: value for key, value in vars(
            constants).items() if not key.startswith('__')}
        json_str = template.render(constants_dict)
        data = json.loads(json_str)
        if data is None:
            return {}
        return data
    except IOError as e:
        if not skip_file_not_found:
            logger.error(f"Could not open file {template_filename}")
            raise e
        else:
            logger.warning(f"Could not open file {
                template_filename} - returning empty dict.")
    return data


def read_dict_from_file(*, full_filename: str, skip_file_not_found=True) -> Dict:
    """Reads a dictionary from a file. By default tries to read it from a template file."""
    return read_dict_from_template_file(full_filename=full_filename, skip_file_not_found=skip_file_not_found)