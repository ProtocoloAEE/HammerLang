#!/usr/bin/env python3
"""
HammerLang Compression Benchmark - Validación Empírica
Mide la compresión REAL vs las afirmaciones teóricas
"""

import json
from typing import Dict, List, Tuple

# Simulador simple de tokenización (aproximación - en prod usar tiktoken/transformers)
def estimate_tokens(text: str) -> int:
    """Estimación conservadora de tokens (palabras + símbolos especiales)"""
    # Aproximación: palabra promedio = 1.3 tokens, símbolos = 1-2 tokens cada uno
    words = len(text.split())
    special_chars = len([c for c in text if ord(c) > 127])
    return int(words * 1.3 + special_chars * 1.5)

# Test cases reales del Logic Lock Protocol
test_cases = [
    {
        "name": "Dual-Threshold Lock State",
        "original": """The Dual-Threshold Lock State triggers if ANY of the following: (1) E(G) < θ_lock [absolute degradation] (2) signed_rate(t) < -ε_sensitivity for k windows [rate-based] (3) Var(E[t-τ:t]) > V_threshold AND mean(E) < E_baseline - σ [variance-based, catches 'dancing' coherence]""",
        "hammerlang": "#LLP:DTL:v1.0\n!LOCK⋈⦿[@E(G)<θ↓,Δ⧖(ε↑,k),σ²>V⋔μ<~E-σ]%dancing ⊨a3f9",
        "expected_claim": "45-65x"
    },
    {
        "name": "FSM State Transitions",
        "original": """The Finite State Machine transitions through four states: NORMAL (S0) transitions to DETECT (S1) when coherence drops below threshold θ or anomaly A is detected; DETECT transitions to LOCKED (S2) when rate degradation exceeds epsilon for k consecutive windows or variance exceeds threshold; LOCKED transitions to RECOVER (S3) on explicit override or exception X; RECOVER transitions back to NORMAL on successful recovery R.""",
        "hammerlang": "#LLP:FSM:v1.0\n!FSM⋈[S0→S1:<θ|░A; S1→S2:Δ≺ε*k|σ>th; S2→S3:⟂|░X; S3→S0:░R] ⊨f8d1",
        "expected_claim": "45-65x"
    },
    {
        "name": "Lock Signal Format",
        "original": """Standardized lock signal format consists of: protocol identifier (Logic Lock Protocol v1.3), action type (HALT), affected systems (AxB cross-product), coherence delta (ΔE=0.87), and Unix timestamp in milliseconds (ts=1640995200000).""",
        "hammerlang": "#LLP:SIG:v1.0\n!SIG⊢[🜁|HALT|AxB|ΔE=0.87|ts=16409952e9] ⊨b7c2",
        "expected_claim": "45-65x"
    },
    {
        "name": "Implicit Contradiction Detection",
        "original": """The system detects implicit contradictions through multi-hop reasoning: if proposition P and its negation ¬P are both asserted, or if the negation of P cannot be proven false (¬⊧¬P), and this contradiction is buried deep in the reasoning chain rather than surface-level, trigger the implicit contradiction handler.""",
        "hammerlang": "#LLP:IMP:v1.0\n!IMP⊧[P∧¬P|¬⊧¬P|⦉buried⦊] ⊨c9e4",
        "expected_claim": "35-55x"
    },
    {
        "name": "LoRA Bypass Threat",
        "original": """Detect potential LoRA or PEFT adapter bypass attacks: if adapter introduces delta modifications that cause E(G) coherence mismatch compared to baseline, reject the adapter and flag as high-severity threat.""",
        "hammerlang": "#LLP:THR:v1.0\n!THR⊢[adapterΔ|¬E(G)match|reject|~high] ⊨d2a5",
        "expected_claim": "25-40x"
    }
]

def analyze_compression(test_case: Dict) -> Dict:
    """Analiza la compresión real vs el claim"""
    original_tokens = estimate_tokens(test_case["original"])
    compressed_tokens = estimate_tokens(test_case["hammerlang"])
    
    actual_ratio = original_tokens / compressed_tokens if compressed_tokens > 0 else 0
    actual_savings = ((original_tokens - compressed_tokens) / original_tokens * 100) if original_tokens > 0 else 0
    
    # Parsear el claim esperado
    expected_range = test_case["expected_claim"].replace("x", "").split("-")
    expected_min = float(expected_range[0])
    expected_max = float(expected_range[1]) if len(expected_range) > 1 else expected_min
    
    meets_claim = expected_min <= actual_ratio <= expected_max
    
    return {
        "name": test_case["name"],
        "original_tokens": original_tokens,
        "compressed_tokens": compressed_tokens,
        "actual_ratio": round(actual_ratio, 2),
        "actual_savings_pct": round(actual_savings, 2),
        "expected_claim": test_case["expected_claim"],
        "meets_claim": meets_claim,
        "delta_vs_min": round(actual_ratio - expected_min, 2),
        "verdict": "✅ PASS" if meets_claim else f"❌ FAIL (off by {abs(round(actual_ratio - expected_min, 2))}x)"
    }

def run_benchmark():
    """Ejecuta el benchmark completo"""
    print("=" * 80)
    print("HAMMERLANG COMPRESSION BENCHMARK - Validación Empírica")
    print("=" * 80)
    print()
    
    results = []
    for test_case in test_cases:
        result = analyze_compression(test_case)
        results.append(result)
    
    # Reporte detallado
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['name']}")
        print(f"   Original: {result['original_tokens']} tokens")
        print(f"   Compressed: {result['compressed_tokens']} tokens")
        print(f"   Ratio actual: {result['actual_ratio']}x ({result['actual_savings_pct']}% ahorro)")
        print(f"   Claim esperado: {result['expected_claim']}")
        print(f"   {result['verdict']}")
        print()
    
    # Estadísticas agregadas
    avg_ratio = sum(r['actual_ratio'] for r in results) / len(results)
    avg_savings = sum(r['actual_savings_pct'] for r in results) / len(results)
    pass_rate = sum(1 for r in results if r['meets_claim']) / len(results) * 100
    
    print("=" * 80)
    print("RESUMEN AGREGADO")
    print("=" * 80)
    print(f"Promedio de compresión: {avg_ratio:.2f}x")
    print(f"Promedio de ahorro: {avg_savings:.2f}%")
    print(f"Tasa de éxito vs claims: {pass_rate:.1f}%")
    print()
    
    # Veredicto final
    if pass_rate >= 80:
        print("✅ VEREDICTO: Claims de compresión VALIDADOS")
    elif pass_rate >= 50:
        print("⚠️ VEREDICTO: Claims parcialmente validados - necesita ajuste")
    else:
        print("❌ VEREDICTO: Claims NO validados - compresión sobrestimada")
    
    print()
    print("NOTA: Esta es una estimación conservadora usando tokenización aproximada.")
    print("Para validación definitiva, usar tiktoken (GPT) o tokenizadores reales de cada LLM.")
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    results = run_benchmark()
    
    # Guardar resultados en JSON para análisis posterior
    with open("/home/claude/benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResultados guardados en: benchmark_results.json")
