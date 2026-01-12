import fire
from pathlib import Path

import napari

from dataspecloupe.explorer import Explorer


def run(views_root: str, data_path: str):
    explorer = Explorer(Path(views_root), Path(data_path))
    explorer.prepare_gui()
    napari.run()


if __name__ == '__main__':
    fire.Fire(run)
