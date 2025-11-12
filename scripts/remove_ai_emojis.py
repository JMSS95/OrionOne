#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove AI/decorative emojis from documentation files.
Preserves functional emojis (checkmarks, warnings) and UTF-8 encoding.
"""

import os
import re
from pathlib import Path

# Emojis to remove (decorative/AI only)
EMOJIS_TO_REMOVE = {
    '🤖': '',  # Robot
    '🧠': '',  # Brain
    '🚀': '',  # Rocket
    '⚡': '',  # Lightning
    '✨': '',  # Sparkles
    '💡': '',  # Light bulb
    '🔧': '',  # Wrench
    '📊': '',  # Chart
    '🎨': '',  # Art palette
    '🎯': '',  # Dart
    '🔥': '',  # Fire
    '💪': '',  # Muscle
    '👍': '',  # Thumbs up
    '👎': '',  # Thumbs down
    '🎉': '',  # Party
    '🎊': '',  # Confetti
    '🌟': '',  # Star
    '💰': '',  # Money bag
    '🐳': '',  # Whale (Docker)
    '🐋': '',  # Whale
    '🐘': '',  # Elephant (PostgreSQL)
    '🗄️': '',  # File cabinet
    '🏗️': '',  # Building construction
    '🌐': '',  # Globe
    '🛠️': '',  # Hammer and wrench
    '🔐': '',  # Locked with key
    '📝': '',  # Memo
    '🧪': '',  # Test tube
    '📧': '',  # Email
    '📚': '',  # Books
    '😱': '',  # Screaming face
}

# Emojis to KEEP (functional)
EMOJIS_TO_KEEP = [
    '✅',  # Check mark (used in task lists)
    '❌',  # Cross mark (used in task lists)
    '⚠️',  # Warning sign (important warnings)
    '❗',  # Exclamation mark (alerts)
    '☑️',  # Ballot box with check
    '✓',   # Check mark (text)
    '✗',   # Cross mark (text)
]

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
        replacements = 0
        
        # Remove each emoji
        for emoji, replacement in EMOJIS_TO_REMOVE.items():
            count = content.count(emoji)
            if count > 0:
                content = content.replace(emoji, replacement)
                replacements += count
                print(f"  - Removed {count}x '{emoji}' from {filepath.name}")
        
        # Clean up double spaces that might result from emoji removal
        content = re.sub(r'  +', ' ', content)
        
        # Write back only if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
            return True, replacements
        
        return False, 0
        
    except Exception as e:
        print(f"  ⚠️  Error processing {filepath}: {e}")
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
    
    print("🧹 Removing AI/decorative emojis from documentation...")
    print(f"📁 Base directory: {base_dir}")
    print(f"🎯 Emojis to remove: {len(EMOJIS_TO_REMOVE)}")
    print(f"✅ Emojis to keep: {len(EMOJIS_TO_KEEP)}")
    print()
    
    total_files_changed = 0
    total_replacements = 0
    
    for filepath in files_to_clean:
        if not filepath.exists():
            print(f"⏭️  Skipping {filepath.name} (not found)")
            continue
        
        print(f"🔍 Processing {filepath.name}...")
        changed, replacements = clean_file(filepath)
        
        if changed:
            total_files_changed += 1
            total_replacements += replacements
            print(f"✅ {filepath.name} cleaned ({replacements} replacements)")
        else:
            print(f"⏭️  {filepath.name} - no changes needed")
        print()
    
    print("=" * 60)
    print(f"✅ Done!")
    print(f"📊 Files changed: {total_files_changed}")
    print(f"🔄 Total replacements: {total_replacements}")
    print()
    print("⚠️  Remember to:")
    print("   1. Review changes with: git diff")
    print("   2. Test files are not corrupted")
    print("   3. Commit if satisfied: git add . && git commit")

if __name__ == '__main__':
    main()
