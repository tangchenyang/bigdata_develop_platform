from data_warehouse.models.data_asset.base_data_asset import DataAsset


class File(DataAsset):
    def __init__(self, name):
        super().__init__(name)
