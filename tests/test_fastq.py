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
    expected = "@"

    assert actual == expected


def test_fastq_quality_size_three_with_one_quality_score():
    actual = minimal(fastq_quality(size=3, min_score=5, max_score=5))
    expected = "EEE"

    assert actual == expected


def test_fastq_quality_size_three_with_one_quality_score_and_sanger_offset():
    actual = minimal(fastq_quality(size=3, min_score=5, max_score=5, offset=33))
    expected = "&&&"

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
    expected = "@ \nA\n+ \n@"

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
    assert all(64 <= ord(c) <= MAX_ASCII for c in quality)


@given(fastq(size=10, add_comment=True, additional_description=False))
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

    quality = fields[-1]
    assert all(64 <= ord(c) <= MAX_ASCII for c in quality)


@given(fastq(size=10, add_comment=True, additional_description=True))
def test_fastq_size_over_one_with_comment_and_additional_description(fastq_string: str):
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

    assert all(c not in ">@" for c in header)
    assert " " in header

    quality = fields[-1]
    assert all(64 <= ord(c) <= MAX_ASCII for c in quality)