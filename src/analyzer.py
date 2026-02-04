from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, Optional

import crack_time
from rules import apply_penalties, base_score, charset_info, entropy_bits, rating_for_score
from utils import (
	has_keyboard_pattern,
	has_repeated_blocks,
	has_repeated_chars,
	has_sequence,
	load_common_passwords,
	normalize_password,
)


@dataclass
class AnalysisResult:
	password_length: int
	score: int
	rating: str
	entropy_bits: float
	crack_time: str
	checks: Dict[str, bool]
	penalties: Dict[str, int]

	def to_dict(self) -> Dict[str, object]:
		payload = asdict(self)
		payload["entropy_bits"] = round(self.entropy_bits, 2)
		return payload


def analyze_password(password: str, common_passwords_path: Optional[str] = None) -> AnalysisResult:
	normalized = normalize_password(password)
	length = len(normalized)
	info = charset_info(normalized)

	is_common = False
	if common_passwords_path:
		common_passwords = load_common_passwords(common_passwords_path)
		is_common = normalized.lower() in common_passwords

	has_seq = has_sequence(normalized)
	has_keyboard = has_keyboard_pattern(normalized)
	has_repeat_chars = has_repeated_chars(normalized)
	has_repeat_blocks = has_repeated_blocks(normalized)

	penalties: Dict[str, int] = {}
	if has_seq:
		penalties["sequence"] = 15
	if has_keyboard:
		penalties["keyboard_pattern"] = 15
	if has_repeat_chars:
		penalties["repeated_chars"] = 10
	if has_repeat_blocks:
		penalties["repeated_blocks"] = 8
	if is_common:
		penalties["common_password"] = 40

	score = apply_penalties(base_score(length, info), penalties)
	if length < 8:
		score = min(score, 25)
	if is_common:
		score = min(score, 20)

	rating = rating_for_score(score)
	entropy = entropy_bits(length, info)
	crack_seconds = crack_time.estimate_crack_time_seconds(entropy)

	checks = {
		"length_at_least_8": length >= 8,
		"length_at_least_12": length >= 12,
		"length_at_least_16": length >= 16,
		"has_lower": info.has_lower,
		"has_upper": info.has_upper,
		"has_digit": info.has_digit,
		"has_symbol": info.has_symbol,
		"has_sequence": has_seq,
		"has_keyboard_pattern": has_keyboard,
		"has_repeated_chars": has_repeat_chars,
		"has_repeated_blocks": has_repeat_blocks,
		"is_common_password": is_common,
	}

	return AnalysisResult(
		password_length=length,
		score=score,
		rating=rating,
		entropy_bits=entropy,
		crack_time=crack_time.humanize_seconds(crack_seconds),
		checks=checks,
		penalties=penalties,
	)
