from pathlib import Path
from typing import Optional

import yaml

import external

external.add()

import napari_feature_visualization

import napari
import pandas as pd


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
        self.config_path = None
        self.config = None
        self.viewer: Optional[napari.Viewer] = None

    def prepare_gui(self, viewer=None):
        self.viewer = viewer or napari.Viewer()

        # TODO make sure that mapping between images and view is stored and used for views with gaps
        for view in self.views:
            layer = self.viewer.open(view)[0]
            self.layers.append(layer)
            if view.name == "UNIQUE_LABEL":
                self.labels = layer

        if self.labels is not None:
            self.set_features(pd.read_csv(self.data_path))

        if self.category_features:
            napari_feature_visualization.add_category_features(self.category_features)

    def _adapt_data_frame(self, dataframe):
        assert "label" in dataframe.columns
        dataframe = dataframe.rename(columns={"label": "index"})  # for napari handling
        return dataframe

    @property
    def category_features(self):
        if self.config is None:
            return []
        return self.config["category_features"]

    def set_config(self, config_path):
        self.config_path = Path(config_path)
        # load config yaml file
        with open(config_path, "r") as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def set_features(self, dataframe):
        assert "label" in dataframe.columns
        dataframe = self._adapt_data_frame(dataframe)
        self.dataframe = dataframe
        self.labels.features = self.dataframe

    def subset_data_columns(self, columns_list: list[str]):
        assert self.labels is not None

        # replace label with index
        columns_list = ["index" if c == "label" else c for c in columns_list]

        if columns_list is None:
            self.labels.features = self.dataframe
        else:
            if "index" not in columns_list:
                columns_list.insert(0, "index")
            self.labels.features = self.dataframe[columns_list]

    def set_view(self, view_number: int):
        new_step = list(self.viewer.dims.current_step)
        new_step[0] = view_number
        self.viewer.dims.current_step = tuple(new_step)

    def set_selected_objects(self, selected_rows, selected_value=1):
        assert self.labels is not None

        dataframe = self.labels.features
        if "SELECTED" not in dataframe.columns:
            dataframe["SELECTED"] = 0
        else:
            dataframe[dataframe["SELECTED"]==selected_value] = 0

        if len(selected_rows) > 0:
            selected_rows = self._adapt_data_frame(selected_rows)
            dataframe.loc[dataframe["index"].isin(selected_rows["index"]),"SELECTED"] = selected_value

            if "view" in selected_rows.columns:
                views = list(selected_rows["view"])
                self.set_view(views[0])