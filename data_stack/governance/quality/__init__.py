from data_stack.sugar import EnumSugar


class QualityType(EnumSugar):
    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"


class DataQualityRule(EnumSugar):
    # data validity
    NOT_NULL = "not_null"
    UNIQUE = "unique"
