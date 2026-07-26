import sys
from pathlib import Path

# Allow tests to import the Flask app and Sudoku module when pytest is run
# from the repository root instead of the starter directory.
STARTER_DIR = Path(__file__).resolve().parents[1]
if str(STARTER_DIR) not in sys.path:
    sys.path.insert(0, str(STARTER_DIR))
