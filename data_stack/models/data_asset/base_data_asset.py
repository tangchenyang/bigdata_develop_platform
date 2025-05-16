from data_stack.models.data_asset.asset_type import AssetType


class DataAsset:
    asset_type: AssetType = None

    def __init__(self, name, description: str = None):
        """
        :param description:
        """

        if self.__class__.asset_type is None:
            raise NotImplementedError(f"Subclass must override asset_type")
        self.name = name
        self.description = description

    def __str__(self):
        return f"{self.asset_type.name}-{self.name}"

    def __repr__(self):
        return self.__str__()
