#!/usr/bin/env python3
"""
Validate file names against the FUNCTIONcalled naming convention.

Pattern: {Layer}.{Role}.{Domain}.{Extension}
Layers: core|interface|logic|application (or aliases: bones|skins|breath|body)
"""

import argparse
import os
import re
import sys
from pathlib import Path

# Canonical layers and their aliases
LAYERS = {
    'core': 'bones',
    'interface': 'skins',
    'logic': 'breath',
    'application': 'body',
}
LAYER_ALIASES = {v: k for k, v in LAYERS.items()}
ALL_LAYERS = set(LAYERS.keys()) | set(LAYERS.values())

# Pattern: optional "example." prefix, then Layer.Role.Domain.Extension
# Role and Domain can have multiple segments separated by dots
NAMING_PATTERN = re.compile(
    r'^(?:example\.)?'  # Optional example prefix
    r'(?P<profile>light|full\.)?'  # Optional profile for example files
    r'(?P<layer>' + '|'.join(ALL_LAYERS) + r')\.'  # Layer (required)
    r'(?P<role>[a-z][a-z0-9]*(?:\.[a-z][a-z0-9]*)*)\.'  # Role (one or more segments)
    r'(?P<domain>[a-z][a-z0-9]*(?:\.[a-z][a-z0-9]*)*)\.'  # Domain (one or more segments)
    r'(?P<ext>[a-z]+)$',  # File extension
    re.IGNORECASE
)

# Files/directories to exclude from validation
EXCLUDE_PATTERNS = [
    r'^\..*',  # Dotfiles
    r'^_.*',  # Underscore-prefixed files
    r'^README.*',
    r'^LICENSE.*',
    r'^CLAUDE\.md$',  # Claude Code config file
    r'^Makefile$',
    r'^.*\.meta\.json$',  # Metadata sidecars validated separately
    r'^\.gitkeep$',
    r'^template\.[a-z]+$',  # Template files are exempt
    r'^.*\.schema\.json$',  # Schema files
    r'^registry\.json$',
    r'^.*\.example\.json$',
]

EXCLUDE_DIRS = [
    '.git',
    '.github',
    '.venv',  # Virtual environment
    '__pycache__',
    'node_modules',
    'tools',  # Tools directory exempt
    'standards',  # Standards directory exempt
    'registry',  # Registry directory exempt
    'archive',  # Archive directory exempt
]


def is_excluded(path: Path, root: Path) -> bool:
    """Check if a file or its parent directories should be excluded."""
    # Check directory exclusions
    parts = path.relative_to(root).parts
    for part in parts[:-1]:  # Check all parent directories
        if part in EXCLUDE_DIRS:
            return True

    # Check file exclusions
    filename = path.name
    for pattern in EXCLUDE_PATTERNS:
        if re.match(pattern, filename, re.IGNORECASE):
            return True

    return False


def validate_name(filename: str) -> tuple[bool, str]:
    """
    Validate a filename against the FUNCTIONcalled naming convention.

    Returns:
        (is_valid, message)
    """
    match = NAMING_PATTERN.match(filename)
    if match:
        layer = match.group('layer').lower()
        # Normalize alias to canonical name
        canonical_layer = LAYER_ALIASES.get(layer, layer)
        return True, f"Valid: layer={canonical_layer}, role={match.group('role')}, domain={match.group('domain')}"

    return False, f"Does not match pattern {{Layer}}.{{Role}}.{{Domain}}.{{Extension}}"


def validate_directory(root: str, verbose: bool = False) -> list[tuple[str, str]]:
    """
    Walk directory and validate all non-excluded files.

    Returns:
        List of (filepath, error_message) tuples for invalid files
    """
    root_path = Path(root).resolve()
    errors = []
    checked = 0

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Filter out excluded directories
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

        current_path = Path(dirpath)

        for filename in filenames:
            filepath = current_path / filename

            if is_excluded(filepath, root_path):
                if verbose:
                    print(f"⏭️  Skipped: {filepath.relative_to(root_path)}")
                continue

            checked += 1
            is_valid, message = validate_name(filename)

            if is_valid:
                if verbose:
                    print(f"✅ {filepath.relative_to(root_path)}: {message}")
            else:
                errors.append((str(filepath.relative_to(root_path)), message))
                print(f"❌ {filepath.relative_to(root_path)}: {message}")

    if not errors:
        print(f"\n✅ All {checked} checked files follow the naming convention.")
    else:
        print(f"\n❌ {len(errors)} of {checked} files do not follow the naming convention.")

    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate file names against FUNCTIONcalled naming convention"
    )
    parser.add_argument(
        '--root',
        default='.',
        help='Root directory to validate (default: current directory)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show all files including skipped and valid ones'
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='Specific files to validate (overrides --root scan)'
    )

    args = parser.parse_args()

    if args.files:
        # Validate specific files
        errors = []
        for filepath in args.files:
            filename = Path(filepath).name
            is_valid, message = validate_name(filename)
            if is_valid:
                print(f"✅ {filepath}: {message}")
            else:
                errors.append((filepath, message))
                print(f"❌ {filepath}: {message}")

        if errors:
            sys.exit(1)
    else:
        # Scan directory
        errors = validate_directory(args.root, verbose=args.verbose)
        if errors:
            sys.exit(1)


if __name__ == '__main__':
    main()
