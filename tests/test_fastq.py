import pytest
from hypothesis import errors, given

from hypothesis_bio.hypothesis_bio import MAX_ASCII, fastq, fastq_quality

from .minimal import minimal


def test_fastq_quality_smallest_example():
    actual = minimal(fastq_quality())
    expected = ""

    assert actual == expected


def test_fastq_quality_smallest_non_empty_with_default_ascii():
    actual = minimal(fastq_quality(size=1))
    expected = "0"  # for some reason hypothesis shrinks towards 0 for unicodes

    assert actual == expected


def test_fastq_quality_size_three_with_one_quality_score():
    actual = minimal(fastq_quality(size=3, min_score=5, max_score=5))
    expected = "&&&"

    assert actual == expected


def test_fastq_quality_size_three_with_one_quality_score_and_sanger_offset():
    actual = minimal(fastq_quality(size=3, min_score=5, max_score=5, offset=64))
    expected = "EEE"

    assert actual == expected


def test_fastq_quality_min_score_larger_than_max_score_raises_error():
    min_score = 10
    max_score = 9
    with pytest.raises(errors.InvalidArgument):
        minimal(fastq_quality(min_score=min_score, max_score=max_score))


def test_fastq_quality_offset_causes_outside_ascii_range_raises_error():
    min_score = 100
    max_score = 101
    with pytest.raises(ValueError):
        minimal(fastq_quality(min_score=min_score, max_score=max_score))


def test_fastq_smallest_example():
    actual = minimal(fastq())
    expected = "@ \n\n+ \n"

    assert actual == expected


def test_fastq_smallest_non_empty():
    actual = minimal(fastq(size=1))
    expected = "@ \nA\n+ \n0"

    assert actual == expected


@given(fastq(size=10))
def test_fastq_size_over_one(fastq_string: str):
    fields = fastq_string.split("\n")
    header_begin = fields[0][0]
    assert header_begin == "@"

    header = fields[0][1:]
    assert all(c not in ">@" for c in header)

    sequence = fields[1]
    assert all(c in "ACGT" for c in sequence)

    seq_qual_sep = fields[2][0]
    assert seq_qual_sep == "+"

    quality = fields[-1]
    assert all(33 <= ord(c) <= MAX_ASCII for c in quality)


@given(fastq(size=10, additional_description=False))
def test_fastq_size_over_one_with_comment_no_additional_description(fastq_string: str):
    fields = fastq_string.split("\n")
    header_begin = fields[0][0]
    assert header_begin == "@"

    header = fields[0][1:]
    assert all(c not in ">@" for c in header)
    assert " " in header

    sequence = fields[1]
    assert all(c in "ACGT" for c in sequence)

    seq_qual_sep = fields[2][0]
    assert seq_qual_sep == "+"

    quality = fields[-1]
    assert all(33 <= ord(c) <= MAX_ASCII for c in quality)


@given(fastq(size=10))
def test_fastq_size_over_one_with_comment(fastq_string: str):
    fields = fastq_string.split("\n")
    header_begin = fields[0][0]
    assert header_begin == "@"

    header = fields[0][1:]
    assert all(c not in ">@" for c in header)
    assert " " in header

    sequence = fields[1]
    assert all(c in "ACGT" for c in sequence)

    seq_qual_sep = fields[2][0]
    assert seq_qual_sep == "+"

    additional_description = fields[2][1:]
    assert all(c not in ">@" for c in additional_description)
    assert " " in header

    quality = fields[-1]
    assert all(33 <= ord(c) <= MAX_ASCII for c in quality)


@given(fastq(size=10, wrapped=3))
def test_fastq_wrapping_less_than_size_wraps_seq_and_quality(fastq_string: str):
    fields = fastq_string.split("\n")

    actual = len(fields)
    expected = 10

    assert actual == expected


@given(fastq(size=10, wrapped=30))
def test_fastq_wrapping_greater_than_size_doesnt_wrap(fastq_string: str):
    fields = fastq_string.split("\n")

    actual = len(fields)
    expected = 4

    assert actual == expected
