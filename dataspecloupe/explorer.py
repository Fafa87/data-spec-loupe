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
        self.dataframe = None

    def prepare_gui(self, viewer=None):
        viewer = viewer or napari.Viewer()

        for view in self.views:
            layer = viewer.open(view)[0]
            self.layers.append(layer)
            if view.name == "UNIQUE_LABEL":
                self.labels = layer

        if self.labels is not None:
            self.set_features(pd.read_csv(self.data_path))

    def set_features(self, dataframe):
        assert "label" in dataframe.columns
        dataframe = dataframe.rename(columns={"label": "index"})  # for napari handling
        self.dataframe = dataframe
        self.labels.features = self.dataframe

    def subset_data_columns(self, columns_list: list[str]):
        assert self.labels is not None

        if columns_list is None:
            self.labels.features = self.dataframe
        else:
            if "index" not in columns_list:
                columns_list.insert(0, "index")
            self.labels.features = self.dataframe[columns_list]
