#!/usr/bin/env python3
"""
UEFN Digest File Finder and Copier

This script helps locate and copy Verse digest files from UEFN installation
to the project VerseDigests/ directory.

Usage:
    python find_and_copy_digests.py [--search-path PATH] [--dry-run]

Options:
    --search-path PATH    Custom UEFN installation path to search
    --dry-run            Show what would be copied without actually copying
    --verbose           Show detailed output
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
from typing import List, Tuple


# Default UEFN installation paths by platform
DEFAULT_SEARCH_PATHS = {
    'win32': [
        os.path.expanduser('~/AppData/Local/UnrealEditorFortnite/Saved/VerseProject'),  # UEFN Project digests (primary)
        'C:/Program Files/Epic Games/UEFN',
        'C:/Program Files (x86)/Epic Games/UEFN',
        'D:/Epic Games/UEFN',
    ],
    'darwin': [
        '/Users/Shared/Epic Games/UEFN',
        os.path.expanduser('~/Library/Application Support/Epic/UEFN'),
    ],
    'linux': [
        '/mnt/c/Users/*/AppData/Local/UnrealEditorFortnite/Saved/VerseProject',  # WSL - UEFN Project digests
        '/mnt/c/Program Files/Epic Games/UEFN',  # WSL - Standalone UEFN (if installed)
        os.path.expanduser('~/.local/share/Epic/UEFN'),
        os.path.expanduser('~/.wine/drive_c/Program Files/Epic Games/UEFN'),
    ],
}


def find_digest_files(search_path: Path, verbose: bool = False) -> List[Path]:
    """
    Recursively search for .digest.verse files in the given path.

    Args:
        search_path: Root directory to search
        verbose: Print detailed search progress

    Returns:
        List of paths to digest files found
    """
    digest_files = []

    if not search_path.exists():
        if verbose:
            print(f"⚠️  Path does not exist: {search_path}")
        return []

    if verbose:
        print(f"🔍 Searching in: {search_path}")

    try:
        for root, dirs, files in os.walk(search_path):
            for file in files:
                if file.endswith('.digest.verse'):
                    full_path = Path(root) / file
                    digest_files.append(full_path)
                    if verbose:
                        print(f"   ✅ Found: {file}")
    except PermissionError as e:
        if verbose:
            print(f"⚠️  Permission denied: {e}")

    return digest_files


def get_project_root() -> Path:
    """Get the project root directory."""
    script_dir = Path(__file__).parent
    return script_dir.parent  # Go up from Python/ to project root


def copy_digest_files(
    source_files: List[Path],
    dest_dir: Path,
    dry_run: bool = False,
    verbose: bool = False
) -> Tuple[int, int]:
    """
    Copy digest files to destination directory.

    Args:
        source_files: List of source file paths
        dest_dir: Destination directory
        dry_run: If True, don't actually copy files
        verbose: Print detailed output

    Returns:
        Tuple of (success_count, failure_count)
    """
    if not dest_dir.exists():
        if dry_run:
            print(f"📁 Would create directory: {dest_dir}")
        else:
            dest_dir.mkdir(parents=True, exist_ok=True)
            if verbose:
                print(f"📁 Created directory: {dest_dir}")

    success = 0
    failed = 0

    for source in source_files:
        dest = dest_dir / source.name

        try:
            if dry_run:
                print(f"📋 Would copy: {source.name}")
                if verbose:
                    print(f"   From: {source}")
                    print(f"   To: {dest}")
            else:
                shutil.copy2(source, dest)
                print(f"✅ Copied: {source.name}")
                if verbose:
                    print(f"   Size: {source.stat().st_size:,} bytes")
            success += 1
        except Exception as e:
            print(f"❌ Failed to copy {source.name}: {e}")
            failed += 1

    return success, failed


def main():
    parser = argparse.ArgumentParser(
        description='Find and copy UEFN Verse digest files to project'
    )
    parser.add_argument(
        '--search-path',
        type=str,
        help='Custom UEFN installation path to search'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without actually copying'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("UEFN Digest File Finder")
    print("=" * 60)
    print()

    # Determine search paths
    search_paths = []

    if args.search_path:
        search_paths.append(Path(args.search_path))
    else:
        # Use default paths for current platform
        platform = sys.platform
        if platform in DEFAULT_SEARCH_PATHS:
            search_paths = [Path(p) for p in DEFAULT_SEARCH_PATHS[platform]]
        else:
            print(f"⚠️  Unknown platform: {platform}")
            print("Please specify --search-path manually")
            return 1

    # Search for digest files
    all_digest_files = []

    print(f"🔍 Searching {len(search_paths)} potential UEFN location(s)...\n")

    for search_path in search_paths:
        files = find_digest_files(search_path, verbose=args.verbose)
        all_digest_files.extend(files)

    if not all_digest_files:
        print("\n❌ No digest files found!")
        print("\nTroubleshooting:")
        print("1. Verify UEFN is installed")
        print("2. Check UEFN installation path in Epic Games Launcher")
        print("3. Run with --search-path to specify custom location")
        print("4. Try running with elevated permissions (admin/sudo)")
        return 1

    # Remove duplicates (in case files found in multiple searches)
    all_digest_files = list(set(all_digest_files))

    print(f"\n✅ Found {len(all_digest_files)} digest file(s):\n")

    # Critical files check
    critical_files = ['Fortnite.digest.verse', 'Verse.digest.verse']
    found_critical = []

    for digest in all_digest_files:
        is_critical = digest.name in critical_files
        marker = "🔥" if is_critical else "  "
        print(f"{marker} {digest.name}")
        if is_critical:
            found_critical.append(digest.name)
        if args.verbose:
            print(f"     {digest.parent}")

    # Verify critical files
    print()
    if len(found_critical) == len(critical_files):
        print("✅ All critical files found!")
    else:
        missing = set(critical_files) - set(found_critical)
        print(f"⚠️  Missing critical files: {', '.join(missing)}")

    # Determine destination directory
    project_root = get_project_root()
    dest_dir = project_root / 'VerseDigests'

    print(f"\n📁 Destination: {dest_dir}")

    # Copy files
    print(f"\n{'📋 DRY RUN - No files will be copied' if args.dry_run else '📦 Copying files...'}")
    print()

    success, failed = copy_digest_files(
        all_digest_files,
        dest_dir,
        dry_run=args.dry_run,
        verbose=args.verbose
    )

    # Summary
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Files found:    {len(all_digest_files)}")
    print(f"Files copied:   {success}")
    if failed > 0:
        print(f"Files failed:   {failed}")

    if args.dry_run:
        print("\n💡 Run without --dry-run to actually copy files")
    else:
        if success > 0 and failed == 0:
            print("\n✅ All files copied successfully!")
            print("\n📝 Next steps:")
            print("   1. Verify files in VerseDigests/ directory")
            print("   2. Proceed to Phase 2: Verse parser implementation")
        elif failed > 0:
            print(f"\n⚠️  Some files failed to copy ({failed}/{len(all_digest_files)})")
            print("   Check permissions and try again")

    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
