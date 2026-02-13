# HammerLang - Production Parser

Formal validation for Basel III LCR and regulatory specs with locked mode enforcement.

## 🚀 Quick Start

### Validate LCR Spec

```bash
python hammerlang.py validate_locked specs/bank_lcr.hml
Generate LCR Spec (if needed)
bash
Copy
bash tools/gen_bank_lcr.sh
Run Tests
bash
Copy
python tests/test_lcr.py
🎯 Pilot Demo (4 semanas)
Demo autocontenida para prospectos Basel III/DORA:
bash
Copy
# 1. Validar spec aprobada (PASARÁ)
python hammerlang.py validate_locked specs/bank_lcr.hml

# 2. Simular cambio no autorizado (ej: 30d → 20d)
./scripts/demo_attack.sh

# 3. Validar nuevamente (FALLARÁ - checksum mismatch)
python hammerlang.py validate_locked specs/bank_lcr.hml
Threat model: Previene modificaciones no autorizadas a specs regulatorias aprobadas (insider edits, CI tampering, spec drift).
CI/CD: Cada PR corre automáticamente validate_locked via GitHub Actions.
❌ What HammerLang is NOT
Not a general-purpose programming language
Not a policy suggestion engine
Not runtime decision logic (OPA/Cedar hacen eso)
✅ Sí es: Immutable spec validator, execution gate, compliance invariant enforcer
📋 Features
✅ Production Locked Mode
Checksum enforcement: Only approved specs can run
Syntax validation: Formal grammar checking
Symbol whitelist: Prevents injection attacks
Namespace control: Restricts to approved domains
✅ Security Hardening
Unknown symbol rejection
Bracket balance validation
Regex injection prevention
External config support for prod deployment
🔒 Production Deployment
Dev Environment
Uses hardcoded checksums in hammerlang.py:
Python
Copy
ALLOWED_CHECKSUMS = {
    "m5e9f3a7": "Basel III LCR v1.1 – BANK:LCR",
    "a8f3c9e2": "DORA ICT minimal spec – ICT:DORA"
}
Production Environment
Mount config/allowed_checksums.json from secure source:
JSON
Copy
{
  "m5e9f3a7": "Basel III LCR v1.1 – BANK:LCR",
  "a8f3c9e2": "DORA ICT minimal spec – ICT:DORA"
}
The parser automatically loads external config if present.
📁 Project Structure
plain
Copy
hammerlang/
├── hammerlang.py              # Main parser (FIXED regex, validation)
├── specs/
│   └── bank_lcr.hml          # Clean spec (no shell script)
├── tools/
│   └── gen_bank_lcr.sh       # Generator script (separated)
├── config/
│   └── allowed_checksums.json # External checksum config (prod)
├── tests/
│   └── test_lcr.py           # Test suite
└── README.md
🔬 Validation Rules
1. Namespace Header
plain
Copy
✅ #BANK:LCR:v1.1
❌ #bank:lcr:v1.1  (lowercase)
❌ BANK:LCR:v1.1   (missing #)
2. Checksum Format
plain
Copy
✅ ⊨m5e9f3a7  (8 hex chars)
❌ ⊨M5E9F3A7  (uppercase)
❌ ⊨m5e9f3a   (too short)
3. Allowed Symbols
Whitelist includes:
A-Z, a-z, 0-9, _ (identifiers)
+-*/<>=().,%  (operators)
≤≥⊨ (Unicode operators)
[]!@⋈⊗⊢⦿ (HammerLang syntax)
Any other symbol → REJECTED
4. Namespace Allowlist
Python
Copy
ALLOWED_NAMESPACES = {
    'BANK', 'ICT', 'DORA', 
    'LLP', 'DTL', 'FSM', 'SIG', 'IMP'
}
🧪 Test Coverage
Run tests:
bash
Copy
python tests/test_lcr.py
Tests include:
✅ Canonical LCR spec passes
✅ Tampered checksum rejected
✅ Unknown symbol rejected
✅ Missing header rejected
✅ Unbalanced brackets rejected
Expected output:
plain
Copy
======================================================================
HAMMERLANG TEST SUITE
======================================================================
Test 1: Canonical LCR spec validation...
✅ PASSED: Canonical LCR spec is valid

Test 2: Tampered checksum rejection...
✅ PASSED: Tampered checksum rejected

Test 3: Unknown symbol rejection...
✅ PASSED: Unknown symbol rejected

Test 4: Missing namespace header...
✅ PASSED: Missing header rejected

Test 5: Unbalanced brackets...
✅ PASSED: Unbalanced brackets rejected

======================================================================
TEST RESULTS
======================================================================
Passed: 5/5
Failed: 0/5

✅ ALL TESTS PASSED
🔧 Extending
Add New Namespace
Edit hammerlang.py:
Python
Copy
ALLOWED_NAMESPACES = {'BANK', 'ICT', 'DORA', 'MYNEWNS'}
Add New Checksum
Dev:
Python
Copy
ALLOWED_CHECKSUMS["abc12345"] = "My new spec"
Prod:
JSON
Copy
{
  "m5e9f3a7": "Basel III LCR v1.1",
  "abc12345": "My new spec"
}
Add Allowed Symbol
Python
Copy
ALLOWED_CHARS = set(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ..."
    "⊕"  # Add new operator
)
📊 Fixes Applied
✅ Fix #1: Clean Specs
Moved shell script to tools/gen_bank_lcr.sh
specs/bank_lcr.hml is now pure HML
✅ Fix #2: Regex Corrections
Fixed: r'#([A-Z]+):([A-Z_]+):v\d+\.\d+'
Fixed: r'⊨[a-f0-9]{8}'
No more escaped brackets \[ → [
✅ Fix #3: Symbol Whitelist
ALLOWED_CHARS set enforced
Unknown symbols rejected with Unicode info
✅ Fix #4: Dev/Prod Separation
load_allowed_checksums() function
External config/allowed_checksums.json support
✅ Fix #5: Test Suite
5 comprehensive tests
Edge cases covered
Regression prevention
🚨 Exit Codes
bash
Copy
python hammerlang.py validate_locked specs/bank_lcr.hml
echo $?
0: Validation passed
1: Validation failed
📄 License
MIT
🤝 Author
Franco Carricondo (@ProtocoloAEE)
