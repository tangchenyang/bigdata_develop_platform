from data_stack.sugar import EnumSugar


class QualityLevel(EnumSugar):
    A = "A"
    B = "B"
    C = "C"


class DataQualityRule(EnumSugar):
    # data validity
    NOT_NULL = "not_null"
    UNIQUE = "unique"
