#! /usr/bin/env python3
# refs/tags/<tag_name> -> <tag_name> and write to build_tag
from os import environ
from pathlib import Path

fp = Path("build_tag")
ref_name = environ.get("GITHUB_REF_NAME", "refs/tags/v0.0.0")
tag = ref_name.split("/")[-1]

print(f"Writing tag '{tag}' to {fp.name}")
Path("build_tag").write_text(tag)
