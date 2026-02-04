from __future__ import annotations

import math


GUESSES_PER_SECOND = 1e8


def estimate_crack_time_seconds(entropy_bits: float) -> float:
	if entropy_bits <= 0:
		return 0.0
	average_guesses = 2 ** max(entropy_bits - 1.0, 0.0)
	return average_guesses / GUESSES_PER_SECOND


def humanize_seconds(seconds: float) -> str:
	if seconds <= 1:
		return "< 1 second"
	units = [
		(60, "seconds"),
		(60, "minutes"),
		(24, "hours"),
		(365, "days"),
		(10, "years"),
		(10, "decades"),
		(10, "centuries"),
		(1000, "millennia"),
	]
	value = seconds
	for base, label in units:
		if value < base:
			return f"{value:.1f} {label}"
		value /= base
	if value >= 1e9:
		return "> 1 billion millennia"
	return f"{value:.1f} millennia"
