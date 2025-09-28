"""Utility helpers for generating and verifying SHA-256 manifests."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Iterable, Tuple


def iter_files(root: Path) -> Iterable[Path]:
    """Yield all files contained in *root* (non-recursive on symlinks)."""

    for path in sorted(root.rglob("*")):
        if path.is_file() and not path.name.startswith("."):
            yield path


def sha256_file(path: Path) -> str:
    """Compute the SHA-256 hash for *path*."""

    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def write_manifest(root: Path, outfile: Path | None = None) -> Path:
    """Generate a sha256sum.txt manifest for files under *root*."""

    if outfile is None:
        outfile = root / "sha256sum.txt"
    lines = []
    for file_path in iter_files(root):
        if file_path == outfile:
            continue
        digest = sha256_file(file_path)
        rel = file_path.relative_to(root)
        lines.append(f"{digest}  {rel.as_posix()}\n")
    outfile.write_text("".join(lines), encoding="utf-8")
    return outfile


def read_manifest(manifest: Path) -> Iterable[Tuple[str, Path]]:
    """Parse a checksum manifest into (digest, relative_path) entries."""

    for line in manifest.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split()
        if len(parts) != 2:
            continue
        digest, rel = parts
        yield digest, manifest.parent / Path(rel)


def verify_manifest(manifest: Path) -> bool:
    """Verify the checksum manifest. Returns *True* when all entries match."""

    for digest, path in read_manifest(manifest):
        if not path.exists():
            return False
        if sha256_file(path) != digest:
            return False
    return True


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SHA-256 manifest helper")
    sub = parser.add_subparsers(dest="command", required=True)

    write_p = sub.add_parser("write", help="Create sha256sum.txt for a directory")
    write_p.add_argument("directory", type=Path, help="Target directory")
    write_p.add_argument("--output", type=Path, help="Optional output file path")

    verify_p = sub.add_parser("verify", help="Verify an existing manifest")
    verify_p.add_argument("manifest", type=Path, help="Path to sha256sum.txt")

    return parser


def main() -> int:
    args = _build_parser().parse_args()

    if args.command == "write":
        directory: Path = args.directory
        directory.mkdir(parents=True, exist_ok=True)
        manifest = write_manifest(directory, args.output)
        print(manifest)
        return 0

    if args.command == "verify":
        manifest: Path = args.manifest
        ok = verify_manifest(manifest)
        if not ok:
            return 1
        print("ok")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
