import logging
from typing import Dict, List

from data_stack.models.data_asset.base_data_asset import DataAsset
from data_stack.utils.dag_helper import DAGHelper

# todo save to table or some where
_data_asset_lineages: Dict[DataAsset, List[DataAsset]] = {}


def register_data_asset_lineage(data_asset: DataAsset, upstream_data_assets: List[DataAsset]):
    _data_asset_lineages[data_asset] = upstream_data_assets
    logging.info(f"Registered lineage for data_asset {data_asset.name}")

def get_all_data_asset_lineages():
    return _data_asset_lineages


def to_graph():
    lineages = get_all_data_asset_lineages()
    dag_helper = DAGHelper()

    for data_asset, upstream_data_assets in lineages.items():
        dag_helper.add_node(str(data_asset))
        for upstream_data_asset in upstream_data_assets:
            dag_helper.add_node(str(upstream_data_asset))
            dag_helper.add_edge(str(upstream_data_asset), str(data_asset))
    logging.info(f"Built data lineage graph")
    return dag_helper.graph

def draw_lineages(path: str):
    DAGHelper(to_graph()).draw(path)
