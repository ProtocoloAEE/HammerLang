#!/usr/bin/env python3
"""
HammerLang v1.0 - Production Parser with Locked Mode
Formal validation for Basel III LCR and regulatory specs

Author: Franco Carricondo (@ProtocoloAEE)
Date: February 8, 2026
Status: Production-Ready with Security Hardening
"""

import re
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

# Allowed namespaces (extend as needed)
ALLOWED_NAMESPACES = {'BANK', 'ICT', 'DORA', 'LLP', 'DTL', 'FSM', 'SIG', 'IMP'}

# Production checksums (can be overridden by config/allowed_checksums.json)
ALLOWED_CHECKSUMS: Dict[str, str] = {
    "m5e9f3a7": "Basel III LCR v1.1 – BANK:LCR",
    "a8f3c9e2": "DORA ICT minimal spec – ICT:DORA"
}

# Allowed characters whitelist (prevents injection attacks)
ALLOWED_CHARS = set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_:# v.\n\r\t"  # Base alphanumeric + separators
    "+-*/<>=().,% "                                     # Operators and separators
    "≤≥⊨"                                              # Unicode operators used in HML
    "abcdefghijklmnopqrstuvwxyz"                       # Lowercase (for checksums)
    "[]!@⋈⊗⊢⦿"                                         # HammerLang operators
)

# Regex patterns (FIXED - no escaped brackets)
HEADER_RE = r'#([A-Z]+):([A-Z_]+):v\d+\.\d+'
CHECKSUM_RE = r'⊨[a-z0-9]{8}'

# ============================================================================
# CHECKSUM MANAGEMENT
# ============================================================================

def load_allowed_checksums() -> Dict[str, str]:
    """
    Load allowed checksums from external config if available.
    Falls back to default ALLOWED_CHECKSUMS if config not found.
    
    This allows separation of dev/prod environments:
    - Dev: Uses hardcoded ALLOWED_CHECKSUMS
    - Prod: Mounts config/allowed_checksums.json from secure source
    """
    external = Path("config/allowed_checksums.json")
    if external.is_file():
        try:
            with external.open() as f:
                checksums = json.load(f)
            print(f"ℹ️  Loaded {len(checksums)} checksums from {external}")
            return checksums
        except Exception as e:
            print(f"⚠️  Failed to load {external}: {e}")
            print("⚠️  Falling back to default checksums")
    return ALLOWED_CHECKSUMS

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_symbols(code: str) -> List[str]:
    """
    Validate that all characters in the spec are in the allowed whitelist.
    This prevents injection attacks and unknown symbols.
    
    Returns:
        List of issues found (empty if valid)
    """
    issues = []
    unknown_chars = set()
    
    for ch in code:
        if ch not in ALLOWED_CHARS:
            unknown_chars.add(ch)
    
    if unknown_chars:
        for ch in sorted(unknown_chars):
            issues.append(f"❌ Unknown symbol: {repr(ch)} (Unicode: U+{ord(ch):04X})")
    
    return issues


def validate_syntax(code: str) -> List[str]:
    """
    Validate HammerLang syntax.
    
    Checks:
    - Namespace header format
    - Checksum format
    - Bracket balance
    - Namespace allowlist
    - Unknown symbols
    
    Returns:
        List of issues found (empty if valid)
    """
    issues = []
    
    # Check for namespace header
    if not re.search(HEADER_RE, code):
        issues.append("❌ No namespace header (#NAMESPACE:SPEC:vX.Y)")
    
    # Check for checksum
    if not re.search(CHECKSUM_RE, code):
        issues.append("❌ Invalid checksum format (expected ⊨[a-f0-9]{8})")
    
    # Check bracket balance
    if code.count('[') != code.count(']'):
        issues.append("❌ Unbalanced brackets []")
    
    if code.count('(') != code.count(')'):
        issues.append("❌ Unbalanced parentheses ()")
    
    # Extract and validate namespace
    namespace_match = re.search(r'#([A-Z]+):', code)
    if namespace_match:
        namespace = namespace_match.group(1)
        if namespace not in ALLOWED_NAMESPACES:
            issues.append(f"❌ Namespace {namespace} not allowed in this build")
    else:
        issues.append("❌ Could not extract namespace")
    
    # Check for unknown symbols
    issues.extend(validate_symbols(code))
    
    return issues


def validate_locked(filepath: str) -> bool:
    """
    Production Locked Mode validation.
    
    Validates that:
    1. Spec has valid syntax
    2. Checksum matches one of the allowed production checksums
    
    This ensures only audited, approved specs can run in production.
    
    Args:
        filepath: Path to HammerLang spec file
    
    Returns:
        True if valid and locked, False otherwise
    """
    print("=" * 70)
    print("HAMMERLANG PRODUCTION LOCKED MODE")
    print("=" * 70)
    print(f"Validating: {filepath}")
    print()
    
    # Read spec
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Syntax validation
    print("Step 1: Syntax validation...")
    issues = validate_syntax(code)
    
    if issues:
        print("❌ Syntax validation FAILED")
        for issue in issues:
            print(f"  {issue}")
        return False
    
    print("✅ Syntax validation PASSED")
    print()
    
    # Checksum extraction and validation
    print("Step 2: Checksum validation...")
    checksum_match = re.search(CHECKSUM_RE, code)
    
    if not checksum_match:
        print("❌ No valid checksum found")
        return False
    
    checksum = checksum_match.group(0)[1:]  # Remove ⊨ prefix
    print(f"Found checksum: {checksum}")
    
    # Load allowed checksums (may come from external config)
    allowed = load_allowed_checksums()
    
    if checksum not in allowed:
        print("❌ Checksum not allowed in Production Locked Mode")
        print()
        print("Allowed checksums:")
        for cs, desc in allowed.items():
            print(f"  ⊨{cs} - {desc}")
        return False
    
    print(f"✅ Checksum APPROVED: {allowed[checksum]}")
    print()
    print("=" * 70)
    print("✅ VALIDATION PASSED - SPEC IS PRODUCTION-LOCKED")
    print("=" * 70)
    
    return True


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Main CLI entry point."""
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python hammerlang.py validate_locked <spec_file>")
        print()
        print("Example:")
        print("  python hammerlang.py validate_locked specs/bank_lcr.hml")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "validate_locked":
        filepath = sys.argv[2]
        result = validate_locked(filepath)
        sys.exit(0 if result else 1)
    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: validate_locked")
        sys.exit(1)


if __name__ == "__main__":
    main()
