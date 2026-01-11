from pathlib import Path

import napari
import pandas as pd
from skimage.data import cells3d


class Explorer:
    def __init__(self, views_root: Path, data_path: Path):
        self.views_root = views_root
        self.data_path = data_path

        self.views = []
        for view in self.views_root.iterdir():
            self.views.append(view)
        self.layers = []
        self.labels = None


    def prepare_gui(self, viewer=None):
        viewer = viewer or napari.Viewer()

        for view in self.views:
            layer = viewer.open(view)[0]
            self.layers.append(layer)
            if view.name == "UNIQUE_LABEL":
                self.labels = layer

        if self.labels is not None:
            dataframe = pd.read_csv(self.data_path)
            self.labels.features = dataframe



