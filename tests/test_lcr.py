#!/usr/bin/env python3
"""
Test suite for HammerLang LCR validation
Tests syntax validation, checksum enforcement, and symbol rejection
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hammerlang import validate_locked, validate_syntax

def test_bank_lcr_ok():
    """Test that canonical LCR spec passes validation."""
    print("Test 1: Canonical LCR spec validation...")
    result = validate_locked("specs/bank_lcr.hml")
    assert result is True, "❌ Canonical LCR spec should pass"
    print("✅ PASSED: Canonical LCR spec is valid\n")


def test_tampered_checksum():
    """Test that tampering with checksum fails validation."""
    print("Test 2: Tampered checksum rejection...")
    
    # Read canonical spec
    with open("specs/bank_lcr.hml") as f:
        code = f.read()
    
    # Tamper with checksum
    tampered = code.replace("⊨m5e9f3a7", "⊨aaaaaaaa")
    
    # Write to temp file
    Path("specs/tmp_bad.hml").write_text(tampered)
    
    # Should fail validation
    result = validate_locked("specs/tmp_bad.hml")
    assert result is False, "❌ Tampered checksum should be rejected"
    
    # Cleanup
    Path("specs/tmp_bad.hml").unlink()
    
    print("✅ PASSED: Tampered checksum rejected\n")


def test_unknown_symbol():
    """Test that unknown symbols are rejected."""
    print("Test 3: Unknown symbol rejection...")
    
    # Read canonical spec
    with open("specs/bank_lcr.hml") as f:
        code = f.read()
    
    # Insert unknown Unicode symbol
    tampered = code.replace("CONSTRAINT LCR ≥ 1.0", "CONSTRAINT LCR ⧞ 1.0")  # ⧞ not in whitelist
    
    # Write to temp file
    Path("specs/tmp_unknown.hml").write_text(tampered)
    
    # Should fail validation
    result = validate_locked("specs/tmp_unknown.hml")
    assert result is False, "❌ Unknown symbol should be rejected"
    
    # Cleanup
    Path("specs/tmp_unknown.hml").unlink()
    
    print("✅ PASSED: Unknown symbol rejected\n")


def test_missing_header():
    """Test that missing namespace header fails validation."""
    print("Test 4: Missing namespace header...")
    
    # Create spec without header
    bad_spec = """
STOCK_HQLA = LEVEL1 + LEVEL2A + LEVEL2B
LCR = STOCK_HQLA / OUTFLOWS_30D
⊨m5e9f3a7
"""
    
    # Validate syntax (doesn't require file)
    issues = validate_syntax(bad_spec)
    assert len(issues) > 0, "❌ Missing header should fail validation"
    assert any("namespace header" in issue.lower() for issue in issues)
    
    print("✅ PASSED: Missing header rejected\n")


def test_unbalanced_brackets():
    """Test that unbalanced brackets fail validation."""
    print("Test 5: Unbalanced brackets...")
    
    # Create spec with unbalanced brackets
    bad_spec = """
#BANK:LCR:v1.1
CONSTRAINT [LEVEL2B ≤ 0.15 * STOCK_HQLA
⊨m5e9f3a7
"""
    
    # Validate syntax
    issues = validate_syntax(bad_spec)
    assert len(issues) > 0, "❌ Unbalanced brackets should fail"
    assert any("bracket" in issue.lower() for issue in issues)
    
    print("✅ PASSED: Unbalanced brackets rejected\n")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("HAMMERLANG TEST SUITE")
    print("=" * 70)
    print()
    
    tests = [
        test_bank_lcr_ok,
        test_tampered_checksum,
        test_unknown_symbol,
        test_missing_header,
        test_unbalanced_brackets,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {e}")
            failed += 1
    
    print("=" * 70)
    print("TEST RESULTS")
    print("=" * 70)
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n✅ ALL TESTS PASSED")
        return 0
    else:
        print(f"\n❌ {failed} TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
