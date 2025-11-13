#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove ALL emojis from documentation files.
Preserves UTF-8 encoding and clean markdown formatting.
"""

import os
import re
from pathlib import Path

# Remove ALL emojis using Unicode ranges
# This regex matches all emoji characters
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
        base_dir / '.github' / 'GITHUB_SETUP.md',
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
