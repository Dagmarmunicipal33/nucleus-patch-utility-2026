"""
Utility helpers for managing Roblox client patches.

This module provides small utility functions to assist with patch management,
script execution, and error logging.
"""

import subprocess
from typing import Tuple, List, Optional

def execute_script(script_path: str, args: Optional[List[str]] = None) -> Tuple[bool, str]:
    """
    Execute a script and return its success status and output.

    Args:
        script_path: Path to the script to execute.
        args: Optional list of arguments to pass to the script.

    Returns:
        A tuple containing a boolean indicating success, and the script output.
    """
    try:
        result = subprocess.run(
            [script_path] + (args if args else []),
            check=True,
            capture_output=True,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stdout + e.stderr

def log_error(error_message: str, log_file: str = "error.log") -> None:
    """
    Log an error message to a specified file.

    Args:
        error_message: The error message to log.
        log_file: The file to log the error to. Defaults to "error.log".
    """
    with open(log_file, "a") as f:
        f.write(f"{error_message}\n")

def validate_patch(patch_file: str) -> bool:
    """
    Validate a patch file by checking its existence and readability.

    Args:
        patch_file: Path to the patch file to validate.

    Returns:
        A boolean indicating whether the patch file is valid.
    """
    try:
        with open(patch_file, "r") as f:
            pass
        return True
    except (IOError, OSError):
        return False
