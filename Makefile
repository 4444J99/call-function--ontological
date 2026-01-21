PY ?= python
SCHEMA := standards/FUNCTIONcalled_Metadata_Sidecar.v1.1.schema.json
VALIDATOR := tools/validate_meta.py
NAMING_VALIDATOR := tools/validate_naming.py
SEMGREP_RULES := tools/semgrep/functioncalled.yaml
REG_BUILDER := tools/registry-builder.py
META_FILES := $(shell find . -type f -name "*.meta.json" 2>/dev/null)

.PHONY: validate validate-naming semgrep validate-all registry hook-install install-deps

# Validate metadata sidecar files against JSON schema
validate:
	@[ -f $(SCHEMA) ] || (echo "Missing $(SCHEMA)" && exit 1)
	@[ -f $(VALIDATOR) ] || (echo "Missing $(VALIDATOR)" && exit 1)
	@([ -n "$(META_FILES)" ] && $(PY) $(VALIDATOR) $(META_FILES)) || (echo "No *.meta.json files found" && exit 0)

# Validate file naming conventions
validate-naming:
	@[ -f $(NAMING_VALIDATOR) ] || (echo "Missing $(NAMING_VALIDATOR)" && exit 1)
	@$(PY) $(NAMING_VALIDATOR) --root .

# Run semgrep rules (requires semgrep to be installed)
semgrep:
	@[ -f $(SEMGREP_RULES) ] || (echo "Missing $(SEMGREP_RULES)" && exit 1)
	@command -v semgrep >/dev/null 2>&1 || (echo "semgrep not installed. Run: pip install semgrep" && exit 1)
	@semgrep --config $(SEMGREP_RULES) --exclude='*.meta.json' --exclude='*.schema.json' .

# Run all validators
validate-all: validate validate-naming semgrep
	@echo "All validations passed."

# Build the registry
registry:
	@$(PY) $(REG_BUILDER) --root . --out registry/registry.json
	@echo "Built registry/registry.json"

# Install pre-commit hook with all validators
hook-install:
	@mkdir -p .git/hooks
	@printf '%s\n' \
		'#!/usr/bin/env bash' \
		'set -e' \
		'' \
		'SCHEMA="standards/FUNCTIONcalled_Metadata_Sidecar.v1.1.schema.json"' \
		'META_VALIDATOR="tools/validate_meta.py"' \
		'NAMING_VALIDATOR="tools/validate_naming.py"' \
		'SEMGREP_RULES="tools/semgrep/functioncalled.yaml"' \
		'' \
		'# Get staged files' \
		'STAGED_META=$$(git diff --cached --name-only --diff-filter=ACM | grep -E '"'"'\.meta\.json$$'"'"' || true)' \
		'STAGED_ALL=$$(git diff --cached --name-only --diff-filter=ACM || true)' \
		'' \
		'# 1. Validate metadata sidecars' \
		'if [ -n "$$STAGED_META" ]; then' \
		'    echo "[pre-commit] Validating metadata sidecars..."' \
		'    python "$$META_VALIDATOR" $$STAGED_META || { echo "[pre-commit] Metadata validation failed."; exit 1; }' \
		'fi' \
		'' \
		'# 2. Validate file naming conventions' \
		'if [ -n "$$STAGED_ALL" ]; then' \
		'    echo "[pre-commit] Validating file naming conventions..."' \
		'    python "$$NAMING_VALIDATOR" $$STAGED_ALL || { echo "[pre-commit] Naming validation failed."; exit 1; }' \
		'fi' \
		'' \
		'# 3. Run semgrep (if installed)' \
		'if command -v semgrep >/dev/null 2>&1 && [ -n "$$STAGED_ALL" ]; then' \
		'    echo "[pre-commit] Running semgrep rules..."' \
		'    semgrep --config "$$SEMGREP_RULES" --exclude='"'"'*.meta.json'"'"' --exclude='"'"'*.schema.json'"'"' $$STAGED_ALL || { echo "[pre-commit] Semgrep check failed."; exit 1; }' \
		'fi' \
		'' \
		'echo "[pre-commit] All checks passed."' \
		> .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
	@echo "Installed .git/hooks/pre-commit"

# Install dependencies
install-deps:
	@$(PY) -m pip install --upgrade jsonschema semgrep
