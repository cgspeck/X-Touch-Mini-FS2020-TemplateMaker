import re

from template_maker.text_mapping import TextMapping

PLACEHOLDER = "-"


def test_sorting_patterns():
    memo = [
        TextMapping(
            pat=re.compile("Z"),
            replacement=PLACEHOLDER,
            replacement_unsanitized=PLACEHOLDER,
        ),
        TextMapping(
            pat=re.compile("A"),
            replacement=PLACEHOLDER,
            replacement_unsanitized=PLACEHOLDER,
        ),
    ]

    memo.sort()
    assert memo[0].pat.pattern == "A"


def test_sorting_same_pattern_one_user_modified():
    memo = [
        TextMapping(
            pat=re.compile("A"),
            replacement=PLACEHOLDER,
            replacement_unsanitized=PLACEHOLDER,
            is_default=True,
        ),
        TextMapping(
            pat=re.compile("A"),
            replacement=PLACEHOLDER,
            replacement_unsanitized=PLACEHOLDER,
            is_default=False,
        ),
    ]

    memo.sort()
    assert memo[0].is_default is False


def test_sorting_same_pattern_same_default_status_different_replacements():
    memo = [
        TextMapping(
            pat=re.compile(PLACEHOLDER),
            replacement="B",
            replacement_unsanitized=PLACEHOLDER,
            is_default=False,
        ),
        TextMapping(
            pat=re.compile(PLACEHOLDER),
            replacement="A",
            replacement_unsanitized=PLACEHOLDER,
            is_default=False,
        ),
    ]

    memo.sort()
    assert memo[0].replacement == "A"
