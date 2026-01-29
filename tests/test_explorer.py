from pathlib import Path

import napari
import pandas as pd

from dataspecloupe.explorer import Explorer

TESTS_ROOT = Path(__file__).parent
NANO_ROOT = TESTS_ROOT / "data" / "nano"


def test_explorer():
    explorer = Explorer(NANO_ROOT / "views_nano", data_path=NANO_ROOT / "data_nano.tsv")
    explorer.prepare_gui()
    explorer.subset_data_columns(
        ['index', 'trench_lineage', 'lineage_cellid', 'parent_lineage_cellid', 'cell_generation'])
    napari.run()


def test_features_subset():
    dataframe = pd.read_csv(NANO_ROOT / "data_nano.tsv")
    column_subset = dataframe[["label", "total_intensity_Trans"]]
    assert ["label", "total_intensity_Trans"] == list(column_subset.columns)


def test_category_columns():
    explorer = Explorer(NANO_ROOT / "views_nano", data_path=NANO_ROOT / "data_nano.tsv")
    explorer.set_config(NANO_ROOT / "data_config.yaml")

    assert "track_label" in explorer.category_features
    assert "bbox_min_x" not in explorer.category_features
