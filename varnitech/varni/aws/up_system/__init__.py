import sys
import os

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir)
PRINT_PDM=False

def pdm(message: str, width: int = 20) -> None:
    if not PRINT_PDM: return 
    border = '=' * width
    print(f"{border} {message.center(len(message) + 4)} {border}")