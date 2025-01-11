import logging
from typing import Dict, List

from data_stack.models.data_asset.base_data_asset import DataAsset

# todo save to table or some where
_data_asset_lineages: Dict[DataAsset, List[DataAsset]] = {}


def register_data_asset_lineage(data_asset: DataAsset, upstream_data_assets: List[DataAsset]):
    _data_asset_lineages[data_asset] = upstream_data_assets
    logging.info(f"Registered lineage for data_asset {data_asset.name}")

def get_all_data_asset_lineages():
    return _data_asset_lineages
