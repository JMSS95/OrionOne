#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpar ícones dos ficheiros de documentação
Garante encoding UTF-8 correto
"""

import os
import re

# Ficheiros para limpar ícones
files_to_clean = [
    'docs/requirements.md',
    'docs/architecture.md',
    'docs/database-schema.md',
    'docs/development-workflow.md',
    'docs/development-tools.md',
    'docs/docker-deep-dive.md',
    'docs/testing-strategy.md'
]

# Ícones para remover
icons_to_remove = [
    '✅ ',
    '❌ ',
    '⚠️ ',
    '🔧 ',
    '📋 ',
    '🚀 ',
    '💡 ',
    '⭐ ',
    '📊 ',
    '🎯 ',
    '🔄 ',
    '🛠️ ',
    '⏳ '
]

def clean_icons(content):
    """Remove ícones do conteúdo"""
    for icon in icons_to_remove:
        # Remove ícone no início de linha
        content = content.replace(f'-   {icon}', '-   ')
        content = content.replace(f'- {icon}', '- ')
        
        # Remove ícone em títulos
        content = content.replace(f'## {icon}', '## ')
        content = content.replace(f'### {icon}', '### ')
        content = content.replace(f'#### {icon}', '#### ')
        
        # Remove ícone em bold
        content = content.replace(f'**{icon}', '**')
    
    return content

def process_file(filepath):
    """Processa um ficheiro removendo ícones"""
    if not os.path.exists(filepath):
        print(f"❌ Ficheiro não existe: {filepath}")
        return False
    
    try:
        # Ler com UTF-8
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Limpar ícones
        cleaned_content = clean_icons(content)
        
        # Escrever com UTF-8
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(cleaned_content)
        
        print(f"✓ Limpo: {filepath}")
        return True
    
    except Exception as e:
        print(f"❌ Erro em {filepath}: {e}")
        return False

def main():
    print("🧹 Limpando ícones dos ficheiros de documentação...\n")
    
    success_count = 0
    for filepath in files_to_clean:
        if process_file(filepath):
            success_count += 1
    
    print(f"\n✓ Processados: {success_count}/{len(files_to_clean)} ficheiros")

if __name__ == '__main__':
    main()
