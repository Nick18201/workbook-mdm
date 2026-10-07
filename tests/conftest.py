import os
import sys

# Make both `server.*` and `workbook_generator.*` importable, as in the Docker image (PYTHONPATH=/app:/app/Scripts)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for path in (ROOT, os.path.join(ROOT, "Scripts")):
    if path not in sys.path:
        sys.path.insert(0, path)
