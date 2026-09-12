"""nucleus-patch-utility: core patch-validation runner for Roblox client QA."""

from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class Config:
    """Holds parameters for a single patch-validation run."""

    patch_dir: Path
    scripts: list[str] = field(default_factory=list)
    timeout_s: int = 30
    log_file: Path | None = None

    def __post_init__(self) -> None:
        if not self.patch_dir.is_dir():
            raise FileNotFoundError(f"patch_dir does not exist: {self.patch_dir}")
        if self.timeout_s <= 0:
            raise ValueError("timeout_s must be positive")


def _setup_logging(log_file: Path | None) -> logging.Logger:
    """Configure and return a logger that writes to console and optionally a file."""
    logger = logging.getLogger("nucleus.patch")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    logger.addHandler(stream_handler)

    if log_file is not None:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        )
        logger.addHandler(file_handler)

    return logger


def _execute_script(script_path: Path, timeout_s: int, logger: logging.Logger) -> int:
    """Run a single validation script and return its exit code."""
    try:
        result = subprocess.run(
            ["python", str(script_path)],
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
        if result.stdout:
            logger.debug("stdout: %s", result.stdout.strip())
        if result.stderr:
            logger.warning("stderr: %s", result.stderr.strip())
        return result.returncode
    except subprocess.TimeoutExpired:
        logger.error("Script %s timed out after %ds", script_path.name, timeout_s)
        return 124
    except OSError as exc:
        logger.error("Failed to execute %s: %s", script_path, exc)
        return 1


def run(config: Config) -> int:
    """
    Execute all configured validation scripts against the patch directory.

    Returns 0 if every script succeeded, otherwise the first non-zero exit code.
    """
    logger = _setup_logging(config.log_file)
    logger.info("Starting patch validation for %s", config.patch_dir)

    for script_name in config.scripts:
        script_path = config.patch_dir / script_name
        if not script_path.is_file():
            logger.error("Script not found: %s", script_path)
            return 1
        logger.info("Running %s", script_name)
        exit_code = _execute_script(script_path, config.timeout_s, logger)
        if exit_code != 0:
            logger.error("Script %s failed with exit code %d", script_name, exit_code)
            return exit_code

    logger.info("All patch validation scripts passed.")
    return 0
