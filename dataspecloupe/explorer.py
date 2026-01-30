import re
from pathlib import Path
from typing import Optional

import yaml
from magicgui import magicgui

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
        self.view_to_number = None

        self.selection_dock = None
        self.selection_control = None
        self.selection_subset = []

        if self.views:
            self.view_to_number = self.determine_views_mapping(self.views[0])

    def determine_views_mapping(self, folder):
        all_files = [p.stem for p in Path(folder).iterdir()]
        pattern = re.compile(r'view_(\d+)')
        view_num = lambda filename: int(pattern.search(filename).group(1))

        res = {}
        for i, f in enumerate(sorted(all_files, key=view_num)):
            res[view_num(f)] = i

        return res

    def prepare_gui(self, viewer=None):
        self.viewer = viewer or napari.Viewer()
        @magicgui(
            selected_idx={"widget_type": "Slider", "label": "View subset", "min": 0, "max": 0, "step": 1},
            auto_call=True
        )
        def view_subset_selection(selected_idx: int):
            if len(self.selection_subset) > selected_idx:
                selected_view_number = self.selection_subset[selected_idx]
                self.set_view(selected_view_number)

        self.selection_control = view_subset_selection
        self.selection_dock = self.viewer.window.add_dock_widget(view_subset_selection,
                                                                 area='bottom',
                                                                 name='View subset slider')
        self.update_subset_sliders()

        for view in self.views:
            layer = self.viewer.open(view)[0]
            self.layers.append(layer)
            if view.name == "UNIQUE_LABEL":
                self.labels = layer

        if self.labels is not None:
            self.set_features(pd.read_csv(self.data_path))

        if self.category_features:
            napari_feature_visualization.add_category_features(self.category_features)

    def update_subset_sliders(self):
        if self.selection_subset:
            self.selection_control.selected_idx.max = len(self.selection_subset) - 1
            self.selection_control.selected_idx.value = 0
            self.selection_control.changed.emit()
            self.selection_dock.show()
        else:
            self.selection_dock.hide()

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
        new_step[0] = self.view_to_number[view_number]
        self.viewer.dims.current_step = tuple(new_step)

    def set_view_subset(self, view_numbers: list[int]):
        if len(view_numbers) <= 1:
            self.selection_subset = []
            self.update_subset_sliders()
        else:
            self.selection_subset = list(view_numbers)
            self.update_subset_sliders()
            self.set_view(view_numbers[0])

    def set_selected_objects(self, selected_rows, selected_value=1):
        assert self.labels is not None

        dataframe = self.labels.features
        if "SELECTED" not in dataframe.columns:
            dataframe["SELECTED"] = 0
        else:
            dataframe[dataframe["SELECTED"] == selected_value] = 0

        if len(selected_rows) > 0:
            selected_rows = self._adapt_data_frame(selected_rows)
            dataframe.loc[dataframe["index"].isin(selected_rows["index"]), "SELECTED"] = selected_value

            if "view" in selected_rows.columns:
                views = list(set(selected_rows["view"]))
                self.set_view_subset(views)
