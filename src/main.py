from __future__ import annotations

import argparse
import json
import os
import sys
from getpass import getpass

from analyzer import analyze_password


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Password Strength Analyzer")
	parser.add_argument("--password", type=str, help="Password to analyze")
	parser.add_argument("--json", action="store_true", help="Output JSON")
	return parser.parse_args()


def main() -> int:
	args = parse_args()
	password = args.password
	if not password:
		password = getpass("Enter password: ")

	common_passwords_path = os.path.join(
		os.path.dirname(os.path.dirname(__file__)),
		"data",
		"common_passwords.txt",
	)
	result = analyze_password(password, common_passwords_path)

	if args.json:
		print(json.dumps(result.to_dict(), indent=2))
	else:
		print("Password Strength Analysis")
		print("-" * 30)
		print(f"Score: {result.score}/100")
		print(f"Rating: {result.rating}")
		print(f"Entropy: {result.entropy_bits:.2f} bits")
		print(f"Estimated crack time: {result.crack_time}")
		print("Checks:")
		for key, value in result.checks.items():
			status = "OK" if value else "FAIL"
			print(f"  {key}: {status}")
		if result.penalties:
			print("Penalties:")
			for key, value in result.penalties.items():
				print(f"  {key}: -{value}")

	return 0


if __name__ == "__main__":
	raise SystemExit(main())
