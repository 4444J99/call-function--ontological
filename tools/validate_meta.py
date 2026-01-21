#!/usr/bin/env python3
import json
import sys
import argparse
from jsonschema import Draft202012Validator

parser = argparse.ArgumentParser(description="Validate FUNCTIONcalled metadata sidecar files")
parser.add_argument('--schema', default='standards/FUNCTIONcalled_Metadata_Sidecar.v1.1.schema.json', help='Path to the JSON schema file')
parser.add_argument('files', nargs='+', help='Metadata files to validate')
args = parser.parse_args()

try:
    with open(args.schema) as f:
        schema = json.load(f)
except Exception as e:
    print(f"Error reading schema file {args.schema}: {e}")
    sys.exit(1)

validator = Draft202012Validator(schema)

ok = True
for path in args.files:
    try:
        with open(path) as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ {path}")
        print(f"  - error reading file: {e}")
        ok = False
        continue
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        ok = False
        print(f"❌ {path}")
        for err in errors:
            loc = '.'.join([str(p) for p in err.path]) or "(root)"
            print(f"  - {loc}: {err.message}")
    else:
        print(f"✅ {path}")
if not ok:
    sys.exit(1)
