from pathlib import Path
from shutil import rmtree


def workspace_tmp(name: str) -> Path:
    root = Path(".test-work") / name
    if root.exists():
        rmtree(root)
    root.mkdir(parents=True)
    return root
