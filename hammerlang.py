#!/usr/bin/env python3
"""
hammerlang.py - Encoder/Decoder básico + validador para HammerLang v1.0

Uso: 
  python hammerlang.py decode "tu código HammerLang"
  python hammerlang.py encode "tu texto largo" (placeholder - en desarrollo)
  python hammerlang.py validate "código HammerLang" (verifica sintaxis)

Autor: Proyecto HammerLang (colectivo multi-LLM)
Versión: 1.0.0-audited
"""

import sys
import re
import hashlib

DECODER_PROMPT = """You are the HammerLang v1.0 (NEXUS Edition) decoder.

Context: You will receive compressed specifications using namespace priors and dense symbols.

Namespace loading:
- #LLP:ID:v → Logic Lock Protocol namespace with ID-specific defaults
- All undefined symbols resolve to namespace defaults

Symbol definitions:
- ! = MUST (invariant) | ? = trigger | ~ = default baseline | @ = reference
- % = prune flag (omit known explanation, add [omitted: flag] comment)
- ⊨ = checksum (integrity validation)
- ⋈ = binding/transition | ⦿ = OR-composite | ⧉ = AND-composite
- Δ = delta/change | σ = std deviation | θ = threshold | ε = sensitivity
- ↓ = decreasing | ↑ = increasing

Compound operators:
- Δ⧖ = windowed rate-of-change over k windows
- σ²>V⋔ = variance exceeds threshold AND (conjunction)
- A(B)C = A operates on B in context C

Expansion rules:
1. Resolve namespace defaults first
2. Expand symbols to full technical English
3. Respect pruning flags: add [omitted: flag] where %flag appears
4. Verify checksum if provided
5. Output ONLY the expanded specification in audit-ready format

Input:
"""

def robust_checksum(text):
    """
    Checksum robusto de 8 caracteres (anti-poisoning mejorado)
    
    Args:
        text: Contenido a hashear (sin el checksum mismo)
    
    Returns:
        8 caracteres hex del SHA256
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:8]

def validate_checksum(code):
    """
    Valida el checksum del código HammerLang
    
    Returns:
        tuple: (is_valid, expected_checksum, found_checksum)
    """
    # Buscar checksum en el código (formato: ⊨XXXXXXXX)
    checksum_pattern = r'⊨([a-f0-9]{8})'
    match = re.search(checksum_pattern, code)
    
    if not match:
        return (None, None, "No checksum found")
    
    found_checksum = match.group(1)
    
    # Remover el checksum del código para calcular el esperado
    code_without_checksum = re.sub(checksum_pattern, '', code)
    expected_checksum = robust_checksum(code_without_checksum.strip())
    
    is_valid = (found_checksum == expected_checksum)
    
    return (is_valid, expected_checksum, found_checksum)

def validate_syntax(code):
    """
    Validación básica de sintaxis HammerLang
    
    Returns:
        list: Lista de warnings/errores encontrados
    """
    issues = []
    
    # Check 1: Header namespace presente
    if not re.search(r'#[A-Z]+:[A-Z]+:v\d+\.\d+', code):
        issues.append("⚠️  No namespace header found (expected: #LLP:ID:vX.X)")
    
    # Check 2: Checksum presente y formato correcto
    if not re.search(r'⊨[a-f0-9]{8}', code):
        issues.append("⚠️  No valid checksum found (expected: ⊨XXXXXXXX with 8 hex chars)")
    
    # Check 3: Balanced brackets
    if code.count('[') != code.count(']'):
        issues.append("❌ Unbalanced brackets [ ]")
    
    if code.count('(') != code.count(')'):
        issues.append("❌ Unbalanced parentheses ( )")
    
    # Check 4: Namespace permitidos (whitelist básica)
    allowed_namespaces = ['LLP', 'FSM', 'DTL', 'SIG', 'IMP', 'THR']
    namespace_match = re.search(r'#([A-Z]+):', code)
    if namespace_match and namespace_match.group(1) not in allowed_namespaces:
        issues.append(f"⚠️  Namespace '{namespace_match.group(1)}' not in whitelist: {allowed_namespaces}")
    
    return issues

def decode(code):
    """
    Genera el prompt completo para decodificar en cualquier LLM
    """
    print("=" * 80)
    print("HAMMERLANG DECODER - Copia y pega esto en cualquier LLM")
    print("=" * 80)
    print()
    
    # Validar checksum
    is_valid, expected, found = validate_checksum(code)
    
    if is_valid is not None:
        if is_valid:
            print("✅ Checksum válido")
        else:
            print(f"❌ Checksum INVÁLIDO")
            print(f"   Esperado: {expected}")
            print(f"   Encontrado: {found}")
            print()
            response = input("¿Continuar de todos modos? (y/n): ")
            if response.lower() != 'y':
                print("Decodificación cancelada.")
                return
    else:
        print(f"⚠️  {found}")
    
    print()
    print("-" * 80)
    print()
    
    # Imprimir el prompt completo
    print(DECODER_PROMPT + code)
    
    print()
    print("-" * 80)
    print()
    print("Copia el bloque de arriba completo y pégalo en:")
    print("  • Claude (claude.ai)")
    print("  • ChatGPT (chat.openai.com)")
    print("  • Gemini (gemini.google.com)")
    print("  • Grok (grok.x.ai)")
    print("  • Cualquier otro LLM")
    print()
    print("Obtendrás la expansión completa en inglés técnico.")
    print("=" * 80)

def encode_stub(text):
    """
    Placeholder para encoder automático (v1.1)
    
    Por ahora genera una estructura básica y el checksum correcto
    """
    print("=" * 80)
    print("HAMMERLANG ENCODER (Versión básica - manual)")
    print("=" * 80)
    print()
    print("⚠️  El encoder automático está en desarrollo para v1.1")
    print()
    print("Por ahora, usa esta plantilla manual:")
    print()
    
    # Generar estructura básica
    snippet = text[:50] + "..." if len(text) > 50 else text
    basic_structure = f"#LLP:TEXT:v1.0\n!SPEC⋈[{snippet}]"
    checksum = robust_checksum(basic_structure)
    
    print(f"{basic_structure} ⊨{checksum}")
    print()
    print("Refina manualmente según tu caso de uso:")
    print("  • Define el namespace correcto (#LLP:DTL, #LLP:FSM, etc.)")
    print("  • Usa símbolos apropiados (⋈, ⦿, Δ, σ, θ, ε)")
    print("  • Agrega flags de pruning (%flag) donde aplique")
    print("  • Regenera el checksum con: python hammerlang.py checksum \"tu código\"")
    print()
    print("=" * 80)

def generate_checksum(code):
    """
    Genera el checksum para código HammerLang sin checksum
    """
    # Remover cualquier checksum existente
    code_clean = re.sub(r'⊨[a-f0-9]{8}', '', code).strip()
    checksum = robust_checksum(code_clean)
    
    print("=" * 80)
    print("CHECKSUM GENERATOR")
    print("=" * 80)
    print()
    print(f"Código sin checksum:")
    print(code_clean)
    print()
    print(f"Checksum: ⊨{checksum}")
    print()
    print(f"Código completo:")
    print(f"{code_clean} ⊨{checksum}")
    print("=" * 80)

def validate(code):
    """
    Valida sintaxis y checksum de código HammerLang
    """
    print("=" * 80)
    print("HAMMERLANG VALIDATOR")
    print("=" * 80)
    print()
    
    # Validar sintaxis
    syntax_issues = validate_syntax(code)
    
    if not syntax_issues:
        print("✅ Sintaxis OK")
    else:
        print("Problemas encontrados:")
        for issue in syntax_issues:
            print(f"  {issue}")
    
    print()
    
    # Validar checksum
    is_valid, expected, found = validate_checksum(code)
    
    if is_valid is None:
        print(f"⚠️  {found}")
    elif is_valid:
        print(f"✅ Checksum válido: {found}")
    else:
        print(f"❌ Checksum INVÁLIDO")
        print(f"   Esperado: {expected}")
        print(f"   Encontrado: {found}")
    
    print()
    print("=" * 80)

def show_help():
    """
    Muestra ayuda de uso
    """
    print("""
HammerLang v1.0 - Ultra-dense language for AI safety specs

USAGE:
  python hammerlang.py decode "código HammerLang"
      Genera prompt para decodificar en cualquier LLM
  
  python hammerlang.py encode "texto largo a comprimir"
      Genera estructura básica (manual refinement needed)
  
  python hammerlang.py validate "código HammerLang"
      Valida sintaxis y checksum
  
  python hammerlang.py checksum "código sin checksum"
      Genera checksum para tu código
  
  python hammerlang.py help
      Muestra esta ayuda

EXAMPLES:
  Decodificar:
    python hammerlang.py decode "#LLP:DTL:v1.0
!LOCK⋈⦿[@E(G)<θ↓,Δ⧖(ε↑,k)] ⊨a8f3c9e2"
  
  Validar:
    python hammerlang.py validate "$(cat examples/dual_threshold.hml)"
  
  Generar checksum:
    python hammerlang.py checksum "#LLP:DTL:v1.0
!LOCK⋈⦿[@E(G)<θ↓]"

DOCUMENTATION:
  https://github.com/YOUR_USERNAME/HammerLang
    """)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == "help" or mode == "-h" or mode == "--help":
        show_help()
        sys.exit(0)
    
    if mode in ["decode", "encode", "validate", "checksum"] and len(sys.argv) < 3:
        print(f"Error: '{mode}' requiere un argumento")
        print("Usa: python hammerlang.py help")
        sys.exit(1)
    
    content = " ".join(sys.argv[2:])
    
    if mode == "decode":
        decode(content)
    elif mode == "encode":
        encode_stub(content)
    elif mode == "validate":
        validate(content)
    elif mode == "checksum":
        generate_checksum(content)
    else:
        print(f"Modo desconocido: '{mode}'")
        print("Usa: python hammerlang.py help")
        sys.exit(1)
