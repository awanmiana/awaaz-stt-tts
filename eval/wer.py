"""Word Error Rate for Urdu STT eval (Phase 0; filled in Phase 4).

Metrics:
- WER: word error rate on normalized Urdu text (grapheme tokens).
- CER: character error rate on normalized Urdu text (Arabic-script sensitive).
"""

from __future__ import annotations

from typing import Any

from shared.text_norm import normalize_transcript


def _tokens(text: str) -> list[str]:
    return normalize_transcript(text, "ur").split()


def _chars(text: str) -> list[str]:
    return list(normalize_transcript(text, "ur"))


def _edit_distance(a: list[str], b: list[str]) -> int:
    """Levenshtein distance (substitutions/insertions/deletions)."""
    n, m = len(a), len(b)
    if n == 0:
        return m
    if m == 0:
        return n
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [i] + [0] * m
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(prev[j - 1], prev[j], cur[j - 1])
        prev = cur
    return prev[m]


def wer_details(ref: str, hyp: str) -> dict[str, Any]:
    """WER with sub/ins/del breakdown."""
    r, h = _tokens(ref), _tokens(hyp)
    m, n = len(r), len(h)
    d = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        d[i][0] = i
    for j in range(n + 1):
        d[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = 1 + min(d[i - 1][j - 1], d[i - 1][j], d[i][j - 1])
    # Backtrack
    i, j = m, n
    sub = ins = dele = 0
    while i > 0 or j > 0:
        if i > 0 and j > 0 and r[i - 1] == h[j - 1] and d[i][j] == d[i - 1][j - 1]:
            i, j = i - 1, j - 1
        elif i > 0 and j > 0 and d[i][j] == d[i - 1][j - 1] + 1:
            sub += 1
            i, j = i - 1, j - 1
        elif i > 0 and d[i][j] == d[i - 1][j] + 1:
            dele += 1
            i -= 1
        else:
            ins += 1
            j -= 1
    return {
        "sub": sub,
        "ins": ins,
        "del": dele,
        "ref_len": m,
        "wer": (sub + ins + dele) / max(m, 1) if m else 0.0,
    }


def wer(ref: str, hyp: str) -> float:
    return wer_details(ref, hyp)["wer"]


def cer(ref: str, hyp: str) -> float:
    r, h = _chars(ref), _chars(hyp)
    return _edit_distance(r, h) / max(len(r), 1)


if __name__ == "__main__":  # pragma: no cover
    print("wer:", wer("a b c", "a c"), wer_details("a b c", "a c"))
    print("cer:", cer("abc", "ab"))
