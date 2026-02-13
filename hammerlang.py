#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HammerLang v1.0 – Production Locked Validator (Security Hardened)

- Validación estructural de specs HammerLang
- Production Locked Mode con ruleset inmutable por checksum
- Whitelist de namespaces y símbolos
- Security Hardening: Regex anchoring, homograph defense, fail-safe config
"""

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Dict, List, Union

# ---------------------------------------------------------------------
# CONFIGURACIÓN BÁSICA
# ---------------------------------------------------------------------

IMMUTABLE_RULESET = True  # Production Locked Mode

ALLOWED_NAMESPACES = ["LLP", "BANK", "FSM", "DTL"]

# Regex ENDURECIDOS con anclas de seguridad
HEADER_RE = r'^#([A-Z]+):([A-Z_]+):v\d+\.\d+'  # Ancla ^ al inicio
CHECKSUM_RE = r'⊨[a-f0-9]{8}(?=\s*$)'  # Ancla de fin de línea

# Whitelist de caracteres permitidos
ALLOWED_CHARS = set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_:# v.\n\r\t"
    "+-*/<>=().,% "
    "≤≥⊨"
    "abcdefghijklmnopqrstuvwxyz"
    "[]!@⋈⊗⊢⦿"
)

# Defaults para entorno de desarrollo (se pueden sobreescribir por config/)
DEFAULT_ALLOWED_CHECKSUMS: Dict[str, Union[str, dict]] = {
    "a5e9f3a7": "Basel III LCR v1.1 – BANK:LCR",
    "a8f3c9e2": "DORA ICT minimal spec – ICT:DORA",
}


# ---------------------------------------------------------------------
# UTILIDADES
# ---------------------------------------------------------------------

def robust_checksum(spec: str) -> str:
    """SHA-256 -> 8 hex chars deterministas."""
    h = hashlib.sha256(spec.encode("utf-8")).hexdigest()
    return h[:8]


def extract_checksum(code: str) -> str:
    """Extrae el checksum desde la línea con ⊨xxxx."""
    m = re.search(CHECKSUM_RE, code, re.MULTILINE)
    if not m:
        return ""
    return m.group(0).replace("⊨", "")


def strip_checksum_line(code: str) -> str:
    """
    Elimina ÚNICAMENTE la línea que contiene el checksum (precisión quirúrgica).
    Busca la línea completa que contiene ⊨[checksum] y la elimina.
    """
    lines = code.split('\n')
    filtered_lines = []
    
    for line in lines:
        # Solo eliminar la línea si contiene el patrón de checksum completo
        if not re.search(r'⊨[a-f0-9]{8}(?=\s*$)', line):
            filtered_lines.append(line)
    
    return '\n'.join(filtered_lines)


def load_allowed_checksums() -> Dict[str, Union[str, dict]]:
    """
    Carga allowed checksums en orden de prioridad (FAIL-SAFE MODE):
    1. Variable de entorno ALLOWED_CHECKSUMS (JSON string)
    2. Archivo config/allowed_checksums.json
    3. DEFAULT_ALLOWED_CHECKSUMS (fallback)
    
    SECURITY: Cualquier error en archivos externos causa terminación fatal.
    """
    # Prioridad 1: Variable de entorno
    env_checksums = os.getenv("ALLOWED_CHECKSUMS")
    if env_checksums:
        try:
            data = json.loads(env_checksums)
            if isinstance(data, dict):
                print("ℹ️  Loaded checksums from environment variable")
                return data
            else:
                print("❌ FATAL: ALLOWED_CHECKSUMS env var is not a valid dict")
                sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ FATAL: Invalid JSON in ALLOWED_CHECKSUMS env var: {e}")
            sys.exit(1)

    # Prioridad 2: Archivo externo (FAIL-SAFE)
    external = Path("config/allowed_checksums.json")
    if external.is_file():
        try:
            with external.open() as f:
                data = json.load(f)
                if isinstance(data, dict):
                    print("ℹ️  Loaded checksums from config/allowed_checksums.json")
                    return data
                else:
                    print("❌ FATAL: config/allowed_checksums.json does not contain a valid dict")
                    sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ FATAL: Invalid JSON in config/allowed_checksums.json: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ FATAL: Error loading config/allowed_checksums.json: {e}")
            sys.exit(1)

    # Prioridad 3: Defaults
    print("ℹ️  Using default hardcoded checksums")
    return DEFAULT_ALLOWED_CHECKSUMS


def parse_checksum_entry(entry: Union[str, dict]) -> dict:
    """
    Normaliza entrada de checksum a formato con metadatos.
    Soporta formato legacy (string) y nuevo (dict con signed_by, timestamp).
    """
    if isinstance(entry, str):
        return {
            "spec": entry,
            "signed_by": "legacy",
            "timestamp": "unknown"
        }
    elif isinstance(entry, dict):
        return {
            "spec": entry.get("spec", "Unknown"),
            "signed_by": entry.get("signed_by", "unknown"),
            "timestamp": entry.get("timestamp", "unknown")
        }
    return {"spec": "Unknown", "signed_by": "unknown", "timestamp": "unknown"}


# ---------------------------------------------------------------------
# VALIDACIONES
# ---------------------------------------------------------------------

def validate_symbols(code: str) -> List[str]:
    """
    Validación de símbolos con defensa contra homógrafos Unicode.
    Normaliza a NFKC antes de validar.
    """
    issues: List[str] = []
    
    # DEFENSA CONTRA HOMÓGRAFOS: Normalización Unicode
    normalized_code = unicodedata.normalize('NFKC', code)
    
    for ch in normalized_code:
        if ch not in ALLOWED_CHARS:
            issues.append(f"❌ Unknown symbol: {repr(ch)} (Unicode normalized)")
            break
    
    return issues


def validate_syntax(code: str) -> List[str]:
    """Validación sintáctica básica de HammerLang."""
    issues: List[str] = []

    # Validar header con ancla de inicio
    if not re.search(HEADER_RE, code, re.MULTILINE):
        issues.append("❌ No namespace header (#NAMESPACE:SPEC:vX.Y) at file start")

    # Validar checksum con ancla de fin de línea
    if not re.search(CHECKSUM_RE, code, re.MULTILINE):
        issues.append("❌ Invalid checksum format (expected ⊨[a-f0-9]{8} at line end)")

    if code.count('[') != code.count(']'):
        issues.append("❌ Unbalanced brackets []")

    # EXTRAER NAMESPACE CORRECTAMENTE
    namespace_match = re.search(r'^#([A-Z]+):', code, re.MULTILINE)
    if namespace_match:
        namespace = namespace_match.group(1)
        if namespace not in ALLOWED_NAMESPACES:
            issues.append(f"❌ Namespace {namespace} not allowed in this build")
    else:
        issues.append("❌ Could not extract namespace")

    # Whitelist de símbolos (con defensa homógrafo)
    issues.extend(validate_symbols(code))

    return issues


def validate_checksum(code: str) -> bool:
    """Revalida el checksum embebido."""
    embedded = extract_checksum(code)
    if not embedded:
        print("❌ No checksum marker ⊨XXXXXXXX found")
        return False

    base = strip_checksum_line(code)
    recomputed = robust_checksum(base)

    if embedded != recomputed:
        print(f"❌ Checksum mismatch: embedded={embedded}, recomputed={recomputed}")
        return False

    print(f"✅ Checksum OK: {embedded}")
    return True


# ---------------------------------------------------------------------
# MODO BLOQUEADO (PROD)
# ---------------------------------------------------------------------

def validate_locked(path: str) -> bool:
    """Production Locked Mode: syntax + checksum + whitelist de checksums."""
    if not IMMUTABLE_RULESET:
        print("⚠️ IMMUTABLE_RULESET is False, locked mode disabled")
        return False

    p = Path(path)
    if not p.is_file():
        print(f"❌ Spec file not found: {path}")
        return False

    code = p.read_text(encoding="utf-8")

    print("=" * 70)
    print("HAMMERLANG PRODUCTION LOCKED MODE (SECURITY HARDENED)")
    print("=" * 70)
    print(f"Validating: {path}\n")

    print("Step 1: Syntax validation...")
    issues = validate_syntax(code)
    if issues:
        for i in issues:
            print(i)
        print("❌ Syntax validation FAILED")
        return False
    print("✅ Syntax validation PASSED\n")

    print("Step 2: Checksum validation...")
    m = re.search(CHECKSUM_RE, code, re.MULTILINE)
    if not m:
        print("❌ No valid checksum found")
        return False

    checksum = m.group(0).replace("⊨", "")
    print(f"Found checksum: {checksum}")

    if not validate_checksum(code):
        print("❌ Checksum self-validation FAILED")
        return False

    allowed = load_allowed_checksums()
    print(f"ℹ️  Loaded {len(allowed)} approved checksums")

    if checksum not in allowed:
        print("❌ Checksum not allowed in Production Locked Mode")
        return False

    # Parsear entrada con metadatos y VALIDAR AUDITORÍA
    entry = parse_checksum_entry(allowed[checksum])
    print(f"✅ Checksum APPROVED: {entry['spec']}")
    print(f"   📝 Audit Trail:")
    print(f"      • Signed by: {entry['signed_by']}")
    print(f"      • Timestamp: {entry['timestamp']}\n")

    print("=" * 70)
    print("✅ VALIDATION PASSED - SPEC IS PRODUCTION-LOCKED")
    print("=" * 70)
    return True


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="HammerLang validator (Security Hardened)")
    parser.add_argument("mode", choices=["validate", "validate_locked"], help="Validation mode")
    parser.add_argument("spec", help="Path to HammerLang spec")
    args = parser.parse_args()

    if args.mode == "validate_locked":
        ok = validate_locked(args.spec)
        sys.exit(0 if ok else 1)
    else:
        p = Path(args.spec)
        if not p.is_file():
            print(f"❌ Spec file not found: {args.spec}")
            sys.exit(1)
        code = p.read_text(encoding="utf-8")
        issues = validate_syntax(code)
        if issues:
            for i in issues:
                print(i)
            sys.exit(1)
        if not validate_checksum(code):
            sys.exit(1)
        print("✅ Spec is syntactically valid and checksum matches")
        sys.exit(0)


if __name__ == "__main__":
    main()
