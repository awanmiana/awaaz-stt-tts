"""Project test suite runner: `python -m tests.run_tests`."""

from __future__ import annotations

import sys

import pytest


def main() -> int:
    code = pytest.main(["-q", "--tb=short", "tests"])
    return int(code)


if __name__ == "__main__":
    sys.exit(main())
