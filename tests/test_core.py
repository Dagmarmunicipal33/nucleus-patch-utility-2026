"""pytest tests for core functionality of the Roblox client patch utility."""

import pytest
from ... import core

def test_validate_patch():
    """Test the validate_patch function with a valid patch."""
    patch = {
        "version": "1.0.0",
        "scripts": ["script1.lua", "script2.lua"],
        "dependencies": ["dependency1", "dependency2"]
    }
    assert core.validate_patch(patch) is True

def test_validate_patch_invalid():
    """Test the validate_patch function with an invalid patch."""
    patch = {
        "version": "1.0.0",
        "scripts": ["script1.lua", "script2.lua"],
    }
    assert core.validate_patch(patch) is False

def test_execute_scripts():
    """Test the execute_scripts function with a list of scripts."""
    scripts = ["script1.lua", "script2.lua"]
    assert core.execute_scripts(scripts) is True
