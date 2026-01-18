import sys
from pathlib import Path

def add():
    external_path = Path(__file__).parent
    sys.path.append(str(external_path / "napari-feature-visualization" / "src"))