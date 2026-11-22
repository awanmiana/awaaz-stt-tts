"""eval/wer tests."""

from eval.wer import cer, wer


def test_wer_identical():
    assert wer("ہیلو", "ہیلو") == 0.0


def test_wer_substitution():
    assert wer("a b", "a c") == 0.5


def test_wer_insertion():
    assert wer("a b", "a b c") == 0.5


def test_cer():
    assert cer("ab", "a") == 0.5
