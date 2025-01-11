import pytest

from data_stack.sugar import EnumSugar


class DummyEnum(EnumSugar):
    MEMBER1 = "member1"
    MEMBER2 = "member2"
    MEMBER3 = "member3"


class TestMembers:
    def test_members_should_return_all_members_when_call_func_members(self):
        assert DummyEnum.members() == [DummyEnum.MEMBER1, DummyEnum.MEMBER2, DummyEnum.MEMBER3]


class TestNames:
    def test_names_should_return_all_names_when_call_func_names(self):
        assert DummyEnum.names() == ["MEMBER1", "MEMBER2", "MEMBER3"]


class TestValues:
    def test_values_should_return_all_values_when_call_func_values(self):
        assert DummyEnum.values() == ["member1", "member2", "member3"]


class TestValueOf:
    def test_value_of_should_return_correct_member_when_given_valid_value(self):
        assert DummyEnum.valueOf("member1") == DummyEnum.MEMBER1
        assert DummyEnum.valueOf("member2") == DummyEnum.MEMBER2

    def test_value_of_should_raise_exception_when_given_invalid_value(self):
        with pytest.raises(ValueError, match="member10 is not a valid value of DummyEnum"):
            DummyEnum.valueOf("member10")
