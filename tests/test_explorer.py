from pathlib import Path

import napari

from dataspecloupe.explorer import Explorer

TESTS_ROOT = Path(__file__).parent
NANO_ROOT = TESTS_ROOT / "data" / "nano"

def test_explorer():
    explorer = Explorer(NANO_ROOT / "views_nano", data_path=NANO_ROOT / "data_nano.tsv")
    explorer.prepare_gui()

    napari.run()

