#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove ALL emojis from documentation files.
Preserves UTF-8 encoding and clean markdown formatting.
"""

import os
import re
from pathlib import Path

# Enhanced emoji pattern - catches ALL Unicode emojis
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "\u2640-\u2642"
    "\u2600-\u2B55"
    "\u200d"
    "\u23cf"
    "\u23e9"
    "\u231a"
    "\ufe0f"  # dingbats
    "\u3030"
    "\u2139"  # info icon
    "\u2194-\u2199"  # arrows
    "\u21a9-\u21aa"  # arrows
    "\u231b"
    "\u2328"
    "\u23cf"
    "\u23e9-\u23fa"
    "\u25aa-\u25ab"
    "\u25b6"
    "\u25c0"
    "\u25fb-\u25fe"
    "\u2600-\u2604"
    "\u260e"
    "\u2611"
    "\u2614-\u2615"
    "\u2618"
    "\u261d"
    "\u2620"
    "\u2622-\u2623"
    "\u2626"
    "\u262a"
    "\u262e-\u262f"
    "\u2638-\u263a"
    "\u2640"
    "\u2642"
    "\u2648-\u2653"
    "\u265f-\u2660"
    "\u2663"
    "\u2665-\u2666"
    "\u2668"
    "\u267b"
    "\u267e-\u267f"
    "\u2692-\u2697"
    "\u2699"
    "\u269b-\u269c"
    "\u26a0-\u26a1"
    "\u26a7"
    "\u26aa-\u26ab"
    "\u26b0-\u26b1"
    "\u26bd-\u26be"
    "\u26c4-\u26c5"
    "\u26c8"
    "\u26ce-\u26cf"
    "\u26d1"
    "\u26d3-\u26d4"
    "\u26e9-\u26ea"
    "\u26f0-\u26f5"
    "\u26f7-\u26fa"
    "\u26fd"
    "\u2702"
    "\u2705"
    "\u2708-\u270d"
    "\u270f"
    "\u2712"
    "\u2714"
    "\u2716"
    "\u271d"
    "\u2721"
    "\u2728"
    "\u2733-\u2734"
    "\u2744"
    "\u2747"
    "\u274c"
    "\u274e"
    "\u2753-\u2755"
    "\u2757"
    "\u2763-\u2764"
    "\u2795-\u2797"
    "\u27a1"
    "\u27b0"
    "\u27bf"
    "\u2934-\u2935"
    "\u2b05-\u2b07"
    "\u2b1b-\u2b1c"
    "\u2b50"
    "\u2b55"
    "\u3030"
    "\u303d"
    "\u3297"
    "\u3299"
    "]+",
    flags=re.UNICODE
)

def clean_file(filepath: Path) -> tuple[bool, int]:
    """
    Clean emojis from a single file.

    Returns:
        (changed: bool, replacements: int)
    """
    try:
        # Read file with UTF-8 encoding
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Count emojis before removal
        emojis_found = EMOJI_PATTERN.findall(content)
        replacements = len(emojis_found)

        if replacements > 0:
            # Show sample of emojis found
            unique_emojis = set(emojis_found)
            print(f"  - Found {replacements} emojis: {' '.join(list(unique_emojis)[:10])}")

        # Remove ALL emojis
        content = EMOJI_PATTERN.sub('', content)

        # Clean up multiple spaces that might result from emoji removal
        content = re.sub(r'  +', ' ', content)

        # Clean up empty lines with just spaces
        content = re.sub(r'^\s+$', '', content, flags=re.MULTILINE)

        # Write back only if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
            return True, replacements

        return False, 0

    except Exception as e:
        print(f"  Error processing {filepath}: {e}")
        return False, 0

def main():
    """Main function to process all documentation files."""

    # Define paths to clean
    base_dir = Path(__file__).parent.parent

    files_to_clean = [
        base_dir / 'README.md',
        base_dir / 'SETUP.md',
        base_dir / 'DEPLOYMENT.md',
        base_dir / 'CONTRIBUTING.md',
        base_dir / 'TECH-STACK.md',
        base_dir / '.github' / 'GITHUB_SETUP.md',
        base_dir / 'docs' / 'DEVELOPMENT-PLAN.md',
        base_dir / 'docs' / 'COMMANDS-REFERENCE.md',
        base_dir / 'docs' / 'implementation-checklist.md',
        base_dir / 'docs' / 'MVP.md',
        base_dir / 'docs' / 'development-guide.md',
        base_dir / 'docs' / 'TECH-DEEP-DIVE-BACKEND.md',
        base_dir / 'docs' / 'TECH-DEEP-DIVE-FRONTEND.md',
        base_dir / 'docs' / 'TECH-DEEP-DIVE-DATABASE.md',
        base_dir / 'docs' / 'TECH-DEEP-DIVE-DEVOPS.md',
        base_dir / 'docs' / 'ITSM-STACK-ANALYSIS.md',
        base_dir / 'docs' / 'COMPONENTS-GUIDE.md',
        base_dir / 'docs' / 'database-schema.md',
        base_dir / 'docs' / 'architecture.md',
        base_dir / 'docs' / 'requirements.md',
        base_dir / 'docs' / 'tech-stack.md',
        base_dir / 'docs' / 'business-model.md',
        base_dir / 'docs' / 'guides' / 'Development-Guide.md',
        base_dir / 'docs' / 'guides' / 'DOCKER-GUIDE.md',
        base_dir / 'docs' / 'guides' / 'SPRINT-0-SETUP.md',
        base_dir / 'docs' / 'guides' / 'Sprint-1-guide.md',
        base_dir / 'docs' / 'guides' / 'Sprint-2-guide.md',
        base_dir / 'docs' / 'guides' / 'Sprint-3-guide.md',
    ]

    print("Removing ALL emojis from documentation...")
    print(f"Base directory: {base_dir}")
    print(f"Using Unicode emoji pattern matcher")
    print()

    total_files_changed = 0
    total_replacements = 0

    for filepath in files_to_clean:
        if not filepath.exists():
            print(f"Skipping {filepath.name} (not found)")
            continue

        print(f"Processing {filepath.name}...")
        changed, replacements = clean_file(filepath)

        if changed:
            total_files_changed += 1
            total_replacements += replacements
            print(f"  Cleaned {filepath.name} ({replacements} emojis removed)")
        else:
            print(f"  {filepath.name} - no emojis found")
        print()

    print("=" * 60)
    print(f"Done!")
    print(f"Files changed: {total_files_changed}")
    print(f"Total emojis removed: {total_replacements}")
    print()
    print("Next steps:")
    print("   1. Review changes with: git diff")
    print("   2. Test files are not corrupted")
    print("   3. Commit: git add . && git commit -m 'docs: remove all emojis'")
    print("   4. Push: git push origin feat/add-api-observers-events-docs")

if __name__ == '__main__':
    main()
