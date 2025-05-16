import logging
import os.path
from typing import Dict, List

from data_stack.models.data_asset.base_data_asset import DataAsset

# todo save to table or some where
_data_asset_lineages: Dict[DataAsset, List[DataAsset]] = {}


def register_data_asset_lineage(data_asset: DataAsset, upstream_data_assets: List[DataAsset]):
    _data_asset_lineages[data_asset] = upstream_data_assets
    logging.info(f"Registered lineage for data_asset {data_asset.name}")

def get_all_data_asset_lineages():
    return _data_asset_lineages

def draw_lineages(path: str):
    file_folder = os.path.dirname(path)
    file_name, file_format = os.path.basename(path).split(".")

    lineages = get_all_data_asset_lineages()
    from data_stack.utils.dag_helper import DAGHelper
    dag_helper = DAGHelper(file_folder)

    for data_asset, upstream_data_assets in lineages.items():
        dag_helper.add_node(str(data_asset))
        for upstream_data_asset in upstream_data_assets:
            dag_helper.add_node(str(upstream_data_asset))
            dag_helper.add_edge(str(upstream_data_asset), str(data_asset))

    dag_helper.draw(output_file_name=file_name, output_file_format=file_format)

