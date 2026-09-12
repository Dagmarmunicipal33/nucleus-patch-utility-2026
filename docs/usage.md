# Usage

This document describes how to use **nucleus-patch-utility-2026**.

## Install

```bash
pip install -e .
```

## Basic example

```python
from nucleus_patch_utility_2026.core import Config, run

cfg = Config(verbose=True, targets=["alpha", "beta"])
run(cfg)
```

## CLI

```bash
nucleus_patch_utility_2026 alpha beta -v
```

## Theme

This project is oriented around: A Python-based utility for managing and testing Roblox client patches. Developed for QA engineers and developers to streamline patch validation workflows. It includes a feature for automated script execution and error logging..
