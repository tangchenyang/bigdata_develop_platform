class DataAsset:
    asset_type = None

    def __init__(self, description: str = None):
        """

        :param description:
        """

        if self.__class__.asset_type is None:
            raise NotImplementedError(f"Subclass must override asset_type")

        self.description = description
