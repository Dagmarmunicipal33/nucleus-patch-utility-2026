"""Command-line interface for the nucleus patch utility.

This module exposes a thin ``argparse``-based wrapper around
``core.run`` so that QA engineers can drive patch validation from a
terminal without importing Python code directly.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Config:
    """Runtime configuration assembled from CLI arguments."""

    patch_dir: Path
    target_client: str
    dry_run: bool
    log_file: Path | None


def _build_parser() -> argparse.ArgumentParser:
    """Return a configured ``ArgumentParser`` for the patch utility."""
    parser = argparse.ArgumentParser(
        prog="nucleus-patch",
        description="Manage and test Roblox client patches.",
    )
    parser.add_argument(
        "patch_dir",
        type=Path,
        help="Directory containing patch metadata and payloads.",
    )
    parser.add_argument(
        "--client",
        default="stable",
        choices=("stable", "beta", "canary"),
        help="Target client channel to validate against.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform validation without applying changes.",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=None,
        help="Optional path for structured error logging.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Parse CLI arguments, build a ``Config``, and delegate to ``core.run``.

    Args:
        argv: Optional argument list for testing; defaults to ``sys.argv[1:]``.

    Returns:
        Process exit code: ``0`` on success, ``1`` on failure.
    """
    parser = _build_parser()
    args = parser.parse_args(argv)

    config = Config(
        patch_dir=args.patch_dir.resolve(),
        target_client=args.client,
        dry_run=args.dry_run,
        log_file=args.log_file.resolve() if args.log_file else None,
    )

    if not config.patch_dir.is_dir():
        print(f"error: patch directory not found: {config.patch_dir}", file=sys.stderr)
        return 1

    try:
        from core import run  # local import keeps CLI importable for tests
        return int(run(config) == 0)
    except Exception as exc:  # noqa: BLE001 – top-level catch for CLI
        print(f"fatal: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
