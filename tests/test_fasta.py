from hypothesis import given
from minimal import minimal

from hypothesis_bio import fasta

def test_smallest_example():
    seq = minimal(fasta)
    pieces = seq.split('\n')
    comment = pieces[0]
    fasta_read = pieces[1]
    assert comment[0] == ">"
    assert fasta_read == ""


def test_smallest_non_empty_example():
    assert minimal(fasta(min_size=1)) == "A"


def test_2_mer():
    assert minimal(fasta(min_size=2)) == "AA"


def test_max_size():
    assert len(minimal(fasta(max_size=10))) <= 10
