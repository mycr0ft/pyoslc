#!/usr/bin/env python3
"""Bootstrap script to set up the project with uv."""
import os
import subprocess
import sys

subprocess.check_call(["uv", "venv"])
if sys.platform == "win32":
    bin = ".venv\\Scripts"
else:
    bin = ".venv/bin"

subprocess.check_call([os.path.join(bin, "uv"), "sync"])
