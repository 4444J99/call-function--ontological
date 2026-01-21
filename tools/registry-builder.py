#!/usr/bin/env python3
import os
import json
import argparse
import hashlib

def compute_hash(path):
    """Compute SHA256 hash of a file"""
    hasher = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None

def build_registry(root):
    root = os.path.abspath(root)
    resources = []
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith('.meta.json'):
                meta_path = os.path.join(dirpath, filename)
                base_name = filename[:-len('.meta.json')]
                file_path = os.path.join(dirpath, base_name)
                rel_meta = os.path.relpath(meta_path, root)
                rel_file = os.path.relpath(file_path, root)
                try:
                    with open(meta_path) as f:
                        meta = json.load(f)
                except Exception:
                    meta = {}
                entry = {
                    "name": meta.get("name", base_name),
                    "path": rel_file,
                    "meta": rel_meta
                }
                file_hash = compute_hash(file_path)
                if file_hash:
                    entry["hash"] = file_hash
                resources.append(entry)
    return {"resources": resources}


def main():
    parser = argparse.ArgumentParser(description="Build a FUNCTIONcalled registry from metadata files")
    parser.add_argument('--root', default='.', help='Root directory to scan')
    parser.add_argument('--out', default='registry/registry.json', help='Output registry file path')
    args = parser.parse_args()
    registry = build_registry(args.root)
    out_path = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(registry, f, indent=2)
    print(f"Wrote registry to {args.out}")

if __name__ == '__main__':
    main()
