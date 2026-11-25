#!/usr/bin/env python3
"""One-star review writer: Monday, reviewed as if it were a restaurant.

The review lives in REVIEW and is only written out once validate()
has walked every guard below and found nothing to complain about.
Guards run one after another and the first failure ends the program,
so a bad line can never reach the output file.
"""

import sys

REVIEW = "One star. Arrived late, cold coffee, rude manager named Monday. Would not recommend, will be back."
LIMIT_CHARS = 180
LIMIT_WORDS = 25
OUTPUT_PATH = "/output/entry.txt"
CLOSERS = (".", "!", "?")
ONLY_MARKS = set(".,!?;:'\"-() ")


def fail(reason):
    print(f"invalid review: {reason}", file=sys.stderr)
    raise SystemExit(1)


def _must_exist(line):
    if not line or not line.strip():
        fail("review is empty")


def _must_fit_chars(line):
    if len(line) > LIMIT_CHARS:
        fail(f"review is {len(line)} chars, over the {LIMIT_CHARS} limit")


def _must_fit_words(line):
    if len(line.split()) > LIMIT_WORDS:
        fail(f"review is {len(line.split())} words, over the {LIMIT_WORDS} limit")


def _must_be_clean(line):
    if any(ord(ch) < 32 for ch in line):
        fail("review has control characters")


def _must_be_tidy(line):
    if line != line.strip() or "  " in line or "\n" in line:
        fail("review has leading/trailing/double spaces or a newline")


def _must_have_letters(line):
    if not any(ch.isalpha() for ch in line):
        fail("review has no letters")


def _must_have_substance(line):
    if all(ch in ONLY_MARKS for ch in line):
        fail("review is only punctuation")


def _must_not_be_numbers(line):
    if line.strip().isdigit():
        fail("review is only digits")


def _must_close(line):
    if not line.rstrip().endswith(CLOSERS):
        fail("review must end with punctuation")


def _must_open_one_star(line):
    if not line.startswith("One star"):
        fail("a one-star review must open with 'One star'")


def _must_have_no_star_glyph(line):
    # Literal star symbols are decoration, not a review: the rating is
    # spelled out in words, so ★ and ☆ are turned away at the door.
    if "★" in line or "☆" in line:
        fail("review must not contain star symbols, the rating is spelled out")


def validate(line):
    _must_exist(line)
    _must_fit_chars(line)
    _must_fit_words(line)
    _must_be_clean(line)
    _must_be_tidy(line)
    _must_have_letters(line)
    _must_have_substance(line)
    _must_not_be_numbers(line)
    _must_close(line)
    _must_open_one_star(line)
    _must_have_no_star_glyph(line)


def main():
    validate(REVIEW)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as fp:
        fp.write(REVIEW + "\n")


if __name__ == "__main__":
    main()
