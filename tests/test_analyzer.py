import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from analyzer import analyze_password


def common_passwords_path() -> str:
	return os.path.join(
		os.path.dirname(os.path.dirname(__file__)),
		"data",
		"common_passwords.txt",
	)


def test_common_password_is_very_weak():
	result = analyze_password("password", common_passwords_path())
	assert result.rating in {"Very Weak", "Weak"}
	assert result.score <= 20
	assert result.checks["is_common_password"] is True


def test_strong_password_scores_high():
	result = analyze_password("Z!9vQ#2mL@7xB%4t", common_passwords_path())
	assert result.score >= 70
	assert result.checks["has_lower"]
	assert result.checks["has_upper"]
	assert result.checks["has_digit"]
	assert result.checks["has_symbol"]


def test_sequence_detection():
	result = analyze_password("abcd1234", common_passwords_path())
	assert result.checks["has_sequence"] is True


def test_keyboard_pattern_detection():
	result = analyze_password("Qwerty!234", common_passwords_path())
	assert result.checks["has_keyboard_pattern"] is True
