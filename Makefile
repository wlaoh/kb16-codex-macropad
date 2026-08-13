.PHONY: validate cheat-sheet

validate:
	python3 scripts/validate_layout.py

cheat-sheet:
	python3 scripts/build_cheat_sheet.py
