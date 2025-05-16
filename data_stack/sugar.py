import enum


class EnumSugar(enum.Enum):

    @classmethod
    def members(cls):
        return [member for member in cls]

    @classmethod
    def names(cls):
        return [member.name for member in cls]

    @classmethod
    def values(cls):
        return [member.value for member in cls]

    @classmethod
    def valueOf(cls, value):
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise ValueError(f"{value} is not a valid value of {cls.__name__}")


