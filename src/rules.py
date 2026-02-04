from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class CharsetInfo:
	has_lower: bool
	has_upper: bool
	has_digit: bool
	has_symbol: bool

	@property
	def count(self) -> int:
		return sum([self.has_lower, self.has_upper, self.has_digit, self.has_symbol])

	@property
	def pool_size(self) -> int:
		size = 0
		if self.has_lower:
			size += 26
		if self.has_upper:
			size += 26
		if self.has_digit:
			size += 10
		if self.has_symbol:
			size += 33
		return size


def charset_info(password: str) -> CharsetInfo:
	has_lower = any(ch.islower() for ch in password)
	has_upper = any(ch.isupper() for ch in password)
	has_digit = any(ch.isdigit() for ch in password)
	has_symbol = any(not ch.isalnum() for ch in password)
	return CharsetInfo(has_lower, has_upper, has_digit, has_symbol)


def length_score(length: int) -> int:
	if length < 8:
		return 0
	if length < 12:
		return 20
	if length < 16:
		return 30
	return 40


def variety_score(info: CharsetInfo) -> int:
	return min(info.count * 10, 40)


def base_score(length: int, info: CharsetInfo) -> int:
	return length_score(length) + variety_score(info)


def entropy_bits(length: int, info: CharsetInfo) -> float:
	pool = max(info.pool_size, 1)
	return length * math.log2(pool)


def rating_for_score(score: int) -> str:
	if score <= 20:
		return "Very Weak"
	if score <= 40:
		return "Weak"
	if score <= 60:
		return "Medium"
	if score <= 80:
		return "Strong"
	return "Very Strong"


def apply_penalties(score: int, penalties: Dict[str, int]) -> int:
	adjusted = score - sum(penalties.values())
	return max(0, min(100, adjusted))
