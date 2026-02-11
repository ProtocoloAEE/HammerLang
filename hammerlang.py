#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HammerLang v1.0 – Production Locked Validator

- Validación estructural de specs HammerLang
- Production Locked Mode con ruleset inmutable por checksum
- Whitelist de namespaces y símbolos
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

# ---------------------------------------------------------------------
# CONFIGURACIÓN BÁSICA
# ---------------------------------------------------------------------

IMMUTABLE_RULESET = True  # Production Locked Mode

ALLOWED_NAMESPACES = ["LLP", "BANK", "FSM", "DTL"]

# Regex CORRECTOS (sin corchetes escapados)
HEADER_RE = r'#([A-Z]+):([A-Z_]+):v\d+\.\d+'
CHECKSUM_RE = r'⊨[a-f0-9]{8}'

# Whitelist de caracteres permitidos
ALLOWED_CHARS = set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_:# v.\n\r\t"
    "+-*/<>=().,% "
    "≤≥⊨"
    "abcdefghijklmnopqrstuvwxyz"
    "[]!@⋈⊗⊢⦿"
)

# Defaults para entorno de desarrollo (se pueden sobreescribir por config/)
DEFAULT_ALLOWED_CHECKSUMS: Dict[str, str] = {
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
    m = re.search(CHECKSUM_RE, code)
    if not m:
        return ""
    return m.group(0).replace("⊨", "")


def strip_checksum_line(code: str) -> str:
    """Elimina la línea que contiene el checksum (para recomputar)."""
    return re.sub(CHECKSUM_RE + r'.*', '', code)


def load_allowed_checksums() -> Dict[str, str]:
    """Carga allowed checksums desde config/allowed_checksums.json si existe."""
    external = Path("config/allowed_checksums.json")
    if external.is_file():
        try:
            with external.open() as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except Exception:
            # Fallback silencioso a defaults
            pass
    return DEFAULT_ALLOWED_CHECKSUMS


# ---------------------------------------------------------------------
# VALIDACIONES
# ---------------------------------------------------------------------

def validate_symbols(code: str) -> List[str]:
    issues: List[str] = []
    for ch in code:
        if ch not in ALLOWED_CHARS:
            issues.append(f"❌ Unknown symbol: {repr(ch)}")
            break
    return issues


def validate_syntax(code: str) -> List[str]:
    """Validación sintáctica básica de HammerLang."""
    issues: List[str] = []

    if not re.search(HEADER_RE, code):
        issues.append("❌ No namespace header (#NAMESPACE:SPEC:vX.Y)")

    if not re.search(CHECKSUM_RE, code):
        issues.append("❌ Invalid checksum format (expected ⊨[a-f0-9]{8})")

    if code.count('[') != code.count(']'):
        issues.append("❌ Unbalanced brackets []")

    # EXTRAER NAMESPACE CORRECTAMENTE
    namespace_match = re.search(r'#([A-Z]+):', code)
    if namespace_match:
        namespace = namespace_match.group(1)
        if namespace not in ALLOWED_NAMESPACES:
            issues.append(f"❌ Namespace {namespace} not allowed in this build")
    else:
        issues.append("❌ Could not extract namespace")

    # Whitelist de símbolos
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
    print("HAMMERLANG PRODUCTION LOCKED MODE")
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
    m = re.search(CHECKSUM_RE, code)
    if not m:
        print("❌ No valid checksum found")
        return False

    checksum = m.group(0).replace("⊨", "")
    print(f"Found checksum: {checksum}")

    if not validate_checksum(code):
        print("❌ Checksum self-validation FAILED")
        return False

    allowed = load_allowed_checksums()
    print(f"ℹ️  Loaded {len(allowed)} checksums from config/allowed_checksums.json or defaults")

    if checksum not in allowed:
        print("❌ Checksum not allowed in Production Locked Mode")
        return False

    print(f"✅ Checksum APPROVED: {allowed[checksum]}\n")

    print("=" * 70)
    print("✅ VALIDATION PASSED - SPEC IS PRODUCTION-LOCKED")
    print("=" * 70)
    return True


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="HammerLang validator")
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
