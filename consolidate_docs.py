#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para fundir ficheiros de documentação
Garante encoding UTF-8 correto
"""

import os

def read_file(filepath):
    """Lê ficheiro com UTF-8"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """Escreve ficheiro com UTF-8"""
    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

def create_development_guide():
    """Cria development-guide.md fundindo workflow + testing"""
    
    print("📝 Criando development-guide.md...")
    
    # Ler ficheiros
    workflow = read_file('docs/development-workflow.md')
    testing = read_file('docs/testing-strategy.md')
    
    # Remover título do testing (para não duplicar)
    testing = testing.replace('# Estratégia de Testes - OrionOne\n\n', '')
    
    # Fundir
    content = f"""{workflow}

---

# Estratégia de Testes

{testing}
"""
    
    # Escrever
    write_file('docs/development-guide.md', content)
    print("✓ Criado: docs/development-guide.md")

def delete_files():
    """Deleta ficheiros redundantes"""
    files_to_delete = [
        'docs/scripts.md',
        'docs/development-workflow.md',
        'docs/development-tools.md',
        'docs/docker-deep-dive.md',
        'docs/testing-strategy.md'
    ]
    
    print("\n🗑️  Deletando ficheiros redundantes...")
    
    for filepath in files_to_delete:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"✓ Deletado: {filepath}")
        else:
            print(f"⚠ Não existe: {filepath}")

def main():
    print("🔧 Consolidando documentação...\n")
    
    # Criar development-guide.md
    create_development_guide()
    
    # Deletar ficheiros redundantes
    delete_files()
    
    print("\n✅ Consolidação completa!")
    print("\nFicheiros restantes em docs/:")
    print("  - requirements.md")
    print("  - architecture.md")
    print("  - database-schema.md")
    print("  - development-guide.md")

if __name__ == '__main__':
    main()
