from __future__ import annotations

import os
import re
from typing import Iterable, List, Set


SEQUENCE_MIN_LENGTH = 4


def load_common_passwords(path: str) -> Set[str]:
	if not os.path.isfile(path):
		return set()
	with open(path, "r", encoding="utf-8") as handle:
		return {line.strip().lower() for line in handle if line.strip()}


def normalize_password(password: str) -> str:
	return password.strip()


def has_sequence(password: str, min_length: int = SEQUENCE_MIN_LENGTH) -> bool:
	if len(password) < min_length:
		return False
	lower = password.lower()

	def is_sequence(segment: str) -> bool:
		if len(segment) < min_length:
			return False
		diffs = [ord(segment[i + 1]) - ord(segment[i]) for i in range(len(segment) - 1)]
		return all(d == 1 for d in diffs) or all(d == -1 for d in diffs)

	for i in range(len(lower) - min_length + 1):
		for j in range(i + min_length, len(lower) + 1):
			segment = lower[i:j]
			if segment.isalpha() or segment.isdigit():
				if is_sequence(segment):
					return True
			else:
				break
	return False


def has_keyboard_pattern(password: str) -> bool:
	patterns = [
		"qwertyuiop",
		"asdfghjkl",
		"zxcvbnm",
		"1234567890",
		"!@#$%^&*()",
	]
	lower = password.lower()
	for pattern in patterns:
		if _contains_pattern(lower, pattern, 4):
			return True
		if _contains_pattern(lower, pattern[::-1], 4):
			return True
	return False


def _contains_pattern(value: str, pattern: str, min_length: int) -> bool:
	for length in range(min_length, len(pattern) + 1):
		for i in range(len(pattern) - length + 1):
			if pattern[i : i + length] in value:
				return True
	return False


def has_repeated_chars(password: str, repeat_length: int = 3) -> bool:
	if repeat_length <= 1:
		return False
	pattern = re.compile(r"(.)\1{%d,}" % (repeat_length - 1))
	return bool(pattern.search(password))


def has_repeated_blocks(password: str, block_length: int = 2) -> bool:
	if len(password) < block_length * 2:
		return False
	seen = set()
	for i in range(len(password) - block_length + 1):
		block = password[i : i + block_length]
		if block in seen:
			return True
		seen.add(block)
	return False


def unique_char_count(password: str) -> int:
	return len(set(password))


def chunked(iterable: Iterable[str], size: int) -> List[str]:
	if size <= 0:
		return ["".join(iterable)]
	items = list(iterable)
	return ["".join(items[i : i + size]) for i in range(0, len(items), size)]
