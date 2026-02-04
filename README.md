# Password Strength Analyzer

Password Strength Analyzer is a lightweight Python CLI that scores passwords on a 0–100 scale, assigns a rating (Very Weak → Very Strong), estimates entropy, and provides a rough crack-time estimate. It runs locally, makes no network calls, and never saves passwords to disk.

## Features

- Score 0–100 with rating: Very Weak / Weak / Medium / Strong / Very Strong
- Checks:
	- Length thresholds (8 / 12 / 16)
	- Character set variety (lower/upper/digit/symbol)
	- Repeated characters and repeated blocks
	- Sequences (e.g., 1234, abcd)
	- Keyboard patterns (e.g., qwerty, asdf)
	- Common password list match
- Entropy estimation (bits) and rough crack time
- CLI with `--password` and `--json`

## Project Structure

```
src/
	main.py
	analyzer.py
	rules.py
	crack_time.py
	utils.py
data/
	common_passwords.txt
tests/
	test_analyzer.py
```

## Usage

Run with a direct password argument:

```
python src/main.py --password "S0mething!Stronger" 
```

Prompt for the password securely:

```
python src/main.py
```

JSON output:

```
python src/main.py --password "S0mething!Stronger" --json
```

## Notes

- This tool provides a heuristic score, not a guarantee of security.
- Crack time uses a rough offline attack rate (1e8 guesses/sec) and average guess count.
- Passwords are processed in memory only.

## Testing

```
pytest
```
