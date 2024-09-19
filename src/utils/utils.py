import fnmatch
import json
import os
import pathlib
import shutil
import socket
import re as re
from datetime import datetime, timedelta
from sys import exit
from typing import Dict, List, Optional

import coloredlogs
import logging
import unidecode
from requests import Response, Session
from pydantic import field_validator, validate_call

INTERNAL_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
coloredlogs.install()


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


internalDateFormat = "%Y-%m-%d %H:%M:%S"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def transform_date2string(date_to_transform: datetime) -> str:
    try:
        date_str = date_to_transform.strftime(INTERNAL_DATE_FORMAT)
    except:
        logger.error(
            f"Error transforming date: {date_to_transform}. Continuing with empty date string.")
        date_str = ""
    return date_str


def transform_string2date(string_to_transform: str) -> Optional[datetime]:
    """Transforms a String that holds a date in my standard format to a Date. 
        In case it can't transform it, it return None."""
    try:
        date_obj = datetime.strptime(string_to_transform, internalDateFormat)
    except:
        logger.info("transformString2Date", "Error transforming string to date: ",
                    string_to_transform)
        date_obj = None
    return date_obj


def get_now_as_string() -> str:
    return transform_date2string(datetime.now())


def get_min_date_as_string() -> str:
    return transform_date2string(datetime(1970, 1, 1))


def strip_blanks(string):
    return string.strip(" \t")


def are_variables_set(var_names) -> bool:
    # log("areVariablesSet", "Checking if vars are set: ", varNames)
    for varName in var_names:
        if not is_variable_set(varName):
            return False
    # log("areVariablesSet", "All vars are set: ", varNames)
    return True


def is_variable_set(var_name: str) -> bool:
    if (os.getenv(var_name) is None) or (os.getenv(var_name) == ""):
        logger.info("isVariableSet", "Error",
                    f'Variable {var_name} is not set in environment.')
        return False
    return True


def date_string_distance_in_days(date_str1: str, date_str2: str) -> int:
    date1 = transform_string2date(date_str1)
    date2 = transform_string2date(date_str2)
    if not (date1 and date2):
        return -1
    diff: timedelta = abs(date1 - date2)
    return diff.days


def date_string_distance_in_hours(date_str1: str, date_str2: str) -> int:
    date1 = transform_string2date(date_str1)
    date2 = transform_string2date(date_str2)
    if not (date1 and date2):
        return -1
    diff: timedelta = abs(date1 - date2)
    diff_in_seconds = 0
    if diff.days > 0:
        diff_in_seconds += diff.days * 24 * 60 * 60
    diff_in_seconds += diff.seconds
    diff_in_hours = diff_in_seconds / (60 * 60)
    # log("dateStringDistanceInHours", "Date1: ", dateStr1,
    #     ", Date2: ", dateStr2, ", Diff in h: ", diffInHours)
    return diff_in_hours



def load_page(http_session: Session, url: str) -> Optional[Response]:
    try:
        page = http_session.get(url)
        return page
    except:
        logger.error("loadPage", url, ": Error!")
        return None


@validate_call
def simplify_text(some_text: str) -> str:
    """
    Simplifies a text to be used as a filename
    """
    simplified_text = some_text.replace('"', "'")
    simplified_text = unidecode.unidecode(simplified_text)
    simplified_text = re.sub("[^0-9A-Za-z-_]+", "_", simplified_text)
    simplified_text = re.sub('_+', '_', simplified_text)
    logger.info(f"Original text: {some_text}, Simplified text: {simplified_text}")
    return simplified_text


def find_project_root(current_directory):
    """
    Recursively searches for a directory containing a .git folder,
    starting from the current directory and moving upwards in the directory tree.
    Returns the path to the directory containing the .git folder.
    """
    if os.path.exists(os.path.join(current_directory, '.git')):
        return current_directory
    else:
        parent_directory = os.path.dirname(current_directory)
        if parent_directory == current_directory:
            # This means we have reached the root of the filesystem without finding a .git directory
            raise FileNotFoundError(
                "Could not find project root containing a .git directory.")
        return find_project_root(parent_directory)

def _matches_any_pattern(file_name, patterns):
    for pattern in patterns:
        if fnmatch.fnmatch(file_name, pattern):
            return True
    return False

@validate_call
def get_files(directory, *, patterns_to_match: Optional[List[str]] = ["*"], patterns_to_ignore: Optional[List[str]] = []) -> List[str]:
    result_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if _matches_any_pattern(file, patterns_to_match):
                if not _matches_any_pattern(file, patterns_to_ignore):
                    result_files.append(os.path.join(root, file))
    return result_files