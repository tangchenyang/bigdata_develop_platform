import os

import pytest

from data_stack.sugar import EnumSugar


class Tags(EnumSugar):
    SLOW = "slow"


def tags(*tags):
    """
    A decorator to conditionally skip tests based on tags.

    :param tags: Tags to associate with the test function.
    :return: pytest.mark.skipif decorator with the condition and reason.
    """
    skip_tags = os.environ.get("SKIP_TAGS", None)

    if not skip_tags or not tags:
        condition, reason = False, ""
    else:
        skip_tags = [tag.strip() for tag in skip_tags.split(",")]
        hit_skipping_tags = list(set(skip_tags).intersection(set(tags)))
        condition, reason = any(hit_skipping_tags), f"Hit skip tags: {hit_skipping_tags}"

    return pytest.mark.skipif(condition=condition, reason=reason)


