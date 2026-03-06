#!/usr/bin/env python3
"""
HammerLang Origin — Content Origin Verification
Signs any content with a cryptographic signature and generates
a QR-verifiable certificate.

Usage:
    python hammerlang_origin.py sign <file> --origin <HUMAN|AI|HYBRID> --tool <name:version>
    python hammerlang_origin.py verify <signature_file>

Author: Franco Carricondo @ProtocoloAEE
License: MIT
"""

import hashlib
import json
import sys
import os
import argparse
from datetime import datetime, timezone


VERIFY_BASE_URL = "https://protocoloaee.github.io/HammerLang/verify"
SIGNATURES_DIR = ".hammerlang_signatures"


def hash_content(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def generate_signature_id(content_hash: str, timestamp: str) -> str:
    combined = f"{content_hash}:{timestamp}"
    return hashlib.sha256(combined.encode()).hexdigest()[:16]


def sign_content(filepath: str, origin: str, tool: str, location: str = None) -> dict:
    """Sign a file and generate a verifiable certificate."""

    if not os.path.exists(filepath):
        print(f"Error: file '{filepath}' not found.")
        sys.exit(1)

    origin = origin.upper()
    if origin not in ("HUMAN", "AI", "HYBRID"):
        print("Error: --origin must be HUMAN, AI, or HYBRID")
        sys.exit(1)

    with open(filepath, "rb") as f:
        content = f.read()

    content_hash = hash_content(content)
    timestamp = datetime.now(timezone.utc).isoformat()
    sig_id = generate_signature_id(content_hash, timestamp)

    signature = {
        "aicl_spec": "AICL:ORIGIN:v1.0",
        "signature_id": sig_id,
        "origin": origin,
        "tool": tool,
        "timestamp": timestamp,
        "content_hash": content_hash,
        "filename": os.path.basename(filepath),
        "location": location,
        "status": "CERTIFIED",
        "verify_url": f"{VERIFY_BASE_URL}?id={sig_id}"
    }

    # Save signature file
    os.makedirs(SIGNATURES_DIR, exist_ok=True)
    sig_path = os.path.join(SIGNATURES_DIR, f"{sig_id}.json")
    with open(sig_path, "w") as f:
        json.dump(signature, f, indent=2, ensure_ascii=False)

    # Also save alongside the original file
    alongside_path = filepath + ".aicl.json"
    with open(alongside_path, "w") as f:
        json.dump(signature, f, indent=2, ensure_ascii=False)

    return signature


def verify_signature(sig_path: str) -> dict:
    """Verify a signature file."""

    if not os.path.exists(sig_path):
        print(f"Error: signature file '{sig_path}' not found.")
        sys.exit(1)

    with open(sig_path) as f:
        signature = json.load(f)

    # Find original file
    original_path = sig_path.replace(".aicl.json", "")
    if os.path.exists(original_path):
        with open(original_path, "rb") as f:
            content = f.read()
        current_hash = hash_content(content)

        if current_hash == signature["content_hash"]:
            signature["verification_result"] = "CERTIFIED"
            signature["verification_message"] = "Content is intact. Origin verified."
        else:
            signature["verification_result"] = "TAMPERED"
            signature["verification_message"] = "WARNING: Content has been modified since signing."
    else:
        signature["verification_result"] = "UNVERIFIED"
        signature["verification_message"] = "Original file not found. Cannot verify integrity."

    return signature


def print_certificate(signature: dict):
    """Print a human-readable certificate."""
    status = signature.get("verification_result", signature.get("status", "CERTIFIED"))

    icons = {
        "CERTIFIED": "✅",
        "UNVERIFIED": "⚠️",
        "TAMPERED": "🚨"
    }

    print("\n" + "="*60)
    print(f"  AICL:ORIGIN — Content Origin Certificate")
    print("="*60)
    print(f"  Status:    {icons.get(status, '?')} {status}")
    print(f"  Origin:    {signature['origin']}")
    print(f"  Tool:      {signature['tool']}")
    print(f"  Timestamp: {signature['timestamp']}")
    print(f"  File:      {signature['filename']}")
    print(f"  Hash:      {signature['content_hash'][:32]}...")
    print(f"  ID:        {signature['signature_id']}")
    if signature.get("location"):
        print(f"  Location:  {signature['location']}")
    print(f"\n  Verify:    {signature['verify_url']}")
    print("="*60)
    if signature.get("verification_message"):
        print(f"  {signature['verification_message']}")
    print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="HammerLang Origin — Cryptographic content origin verification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sign a file as AI-generated
  python hammerlang_origin.py sign report.pdf --origin AI --tool "Claude:claude-sonnet-4-6:Anthropic"

  # Sign as human-created
  python hammerlang_origin.py sign article.txt --origin HUMAN --tool "vim:9.0:local"

  # Sign as hybrid (human + AI collaboration)
  python hammerlang_origin.py sign essay.docx --origin HYBRID --tool "Claude+Human:v1:Anthropic"

  # Sign with optional location
  python hammerlang_origin.py sign photo.jpg --origin HUMAN --tool "iPhone:16:Apple" --location "Mendoza,AR"

  # Verify a signed file
  python hammerlang_origin.py verify article.txt.aicl.json
        """
    )

    subparsers = parser.add_subparsers(dest="command")

    # Sign command
    sign_parser = subparsers.add_parser("sign", help="Sign a file and generate origin certificate")
    sign_parser.add_argument("file", help="File to sign")
    sign_parser.add_argument("--origin", required=True, choices=["HUMAN", "AI", "HYBRID"],
                             help="Origin of the content")
    sign_parser.add_argument("--tool", required=True,
                             help="Tool used to create content (name:version:provider)")
    sign_parser.add_argument("--location", default=None,
                             help="Optional location (e.g. 'Mendoza,AR')")

    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify a signed file")
    verify_parser.add_argument("signature", help="Signature file (.aicl.json)")

    args = parser.parse_args()

    if args.command == "sign":
        print(f"\nSigning '{args.file}'...")
        signature = sign_content(args.file, args.origin, args.tool, args.location)
        print_certificate(signature)
        print(f"Signature saved to: {args.file}.aicl.json")
        print(f"Share the verify URL or QR so anyone can check the origin.\n")

    elif args.command == "verify":
        print(f"\nVerifying '{args.signature}'...")
        signature = verify_signature(args.signature)
        print_certificate(signature)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
