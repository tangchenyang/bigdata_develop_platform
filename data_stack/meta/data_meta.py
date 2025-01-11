import logging
from typing import Dict, List

from data_stack.models.data_asset.base_data_asset  import DataAsset

registered_data_assets: Dict[str, DataAsset] = {}

def register_data_asset(data_asset: DataAsset):
    if data_asset.name in registered_data_assets:
        raise ValueError(f"Data asset {data_asset.name} already registered")
    registered_data_assets[data_asset.name] = data_asset

    logging.info(f"Registered data asset {data_asset.name}")

def register_data_assets(data_assets: List[DataAsset]):
    for data_asset in data_assets:
        register_data_asset(data_asset)

def get_data_asset_by_name(name: str):
    if name not in registered_data_assets:
        raise KeyError(f"Not found a data asset named {name}")

    return registered_data_assets.get(name)
