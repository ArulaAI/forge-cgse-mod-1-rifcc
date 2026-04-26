.PHONY: demo test grade sync validate clean

demo:
	@echo "Forge Prowess — CGSE — Module 1: RIFCC"
	@echo "Open exercises/lab-1-rifcc-walk/instructions.md"

test:
	uv run pytest

grade:
	uv run pytest
	uv run python .forge/primitives/lab_grader/shared/grader.py . || echo "[grade] lab_grader stub"

sync:
	forge sync

validate:
	forge validate .

clean:
	rm -rf .forge/journey/*.jsonl
	find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
