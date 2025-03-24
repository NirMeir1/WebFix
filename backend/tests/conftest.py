import sys
from pathlib import Path

# This clearly ensures the backend folder itself is added.
backend_path = str(Path(__file__).resolve().parents[1])

if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

print("sys.path after modification:", sys.path)