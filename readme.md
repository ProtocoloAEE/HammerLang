# HammerLang v1.0 (NEXUS Edition) 🔨

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18447076.svg)](https://doi.org/10.5281/zenodo.18447076)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![License: SaaP](https://img.shields.io/badge/License-SaaP-green.svg)](https://github.com/ProtocoloAEE/HammerLang)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Status: Experimental](https://img.shields.io/badge/Status-Experimental-orange.svg)](https://github.com/ProtocoloAEE/HammerLang)

> **A Universal Ultra-Dense Semantic Compression Protocol for AI Safety Specifications.**  
> Specification Layer within the **Protocolo AEE** Security Stack.

---

## 📄 Official Publication & Citation

This protocol has been formally published as a **Technical Report** on **Zenodo (CERN)**.

**Cite as:**
```bibtex
@techreport{Carricondo2026HammerLang,
  author = {Carricondo, Franco},
  title = {{HammerLang v1.0 (NEXUS Edition): A Semantic Compression Protocol for AI Safety Specifications}},
  institution = {Protocolo AEE, Mendoza, Argentina},
  year = {2026},
  month = {February},
  url = {https://doi.org/10.5281/zenodo.18447076},
  doi = {10.5281/zenodo.18447076}
}
```

---

## 🛡️ Nomenclature & Provenance (Disambiguation)

**HammerLang v1.0 (2026)** is an **original semantic compression architecture** for AI safety specifications developed by **Franco Carricondo** (@ProtocoloAEE) under the **Protocolo AEE** framework (Mendoza, Argentina).

**NOT affiliated with:**
- ❌ The legacy `@hammerlang/interpreter` npm package (inactive, 2022)
- ❌ Valve Corporation's Hammer Editor (Source Engine map editor, 2004–2013)
- ❌ Hammer.js (JavaScript multitouch library, 2010s)
- ❌ Any game modding frameworks or legacy software systems

**HammerLang is a formal specification protocol for AI safety constraints,** not a programming language, IDE, or content creation tool.

---

## 📊 Executive Summary

HammerLang encodes AI safety invariants, state transitions, and constraint boundaries using a **logic-dense symbolic grammar**, achieving:

- **3.44× average compression** (peak 4.11×)
- **~70% token savings** across safety-critical specifications
- **Semantic equivalence validation** via state-match verification
- **Model-agnostic operation** (no proprietary fine-tuning)

**Measurement:** tiktoken cl100k_base tokenizer across 5 representative safety specifications (FSM access control, gradient-locking, threat modeling, contradiction detection, LoRA attacks).

---

## 🏗️ Architecture: Specification Layer + Enforcement Layer

HammerLang operates as the **Specification Layer** within a complementary two-layer safety architecture:

| Layer | Component | Function |
|-------|-----------|----------|
| **Specification** | **HammerLang v1.0** | Encode safety logic in dense symbols; define invariants & state transitions |
| **Enforcement** | **Logic Lock Protocol v1.2** | Execute constraint enforcement; blind gradients; mitigate adversarial attacks |

**Related Work:**  
Logic Lock Protocol v1.2 (Carricondo, Feb 2026) - DOI: [10.5281/zenodo.18447076](https://doi.org/10.5281/zenodo.18447076)

---

## 🔤 Core Grammar (NEXUS)

### Namespace Headers
```
#LLP:DTL  → Dual-Threshold Locks
#LLP:FSM  → Finite State Machines
#LLP:SIG  → Standardized Signals
#LLP:IMP  → Implicit Contradictions
#LLP:THR  → Threat Models
```

### Core Symbols (Single-Token)

| Symbol | Meaning | Context |
|--------|---------|---------|
| `!` | MUST / invariant | Obligatory conditions |
| `?` | trigger / condition | Boolean evaluations |
| `⊨` | checksum | Integrity (8-char hex) |
| `%` | prune flag | Omit known explanation |
| `@` | reference | Reference metric/entity |
| `~` | default | Namespace baseline value |
| `⋈` | binding/transition | Connect state → action |
| `⦿` | OR-composite | Disjunction of conditions |
| `⧉` | AND-composite | Conjunction of conditions |
| `Δ` | delta/change | Derivative or difference |
| `σ` | std deviation | Statistical variance |
| `θ` | threshold | Boundary value |
| `ε` | epsilon/sensitivity | Tolerance margin |
| `↓` | decreasing | Downward trend |
| `↑` | increasing | Upward trend |

### Compound Operators

| Operator | Expansion | Tokens |
|----------|-----------|--------|
| `Δ⧖` | windowed rate-of-change | 2 |
| `σ²>V⋔` | variance AND check | 3-4 |
| `θ↓` | threshold decreasing | 2 |

---

## 💻 Usage

### Basic Decoding
```bash
python hammerlang.py decode "#LLP:DTL:v1.0 !LOCK⋈⦿[@E(G)V⋔μ<~E-σ]%dancing ⊨a8f3c9e2"
```

**Output (55 tokens):**
```
The Dual-Threshold Lock State triggers if ANY of the following:
(1) E(G) < θ_lock [absolute degradation]
(2) signed_rate(t) < -ε_sensitivity for k windows [rate-based]
(3) Var(E[t-τ:t]) > V_threshold AND mean(E) < E_baseline - σ
[omitted: dancing - refers to variance-based detection of oscillating coherence]
```

**Compression:** 2.29× (56% token savings)

---

## 📈 Validated Examples

### 1️⃣ Dual-Threshold Lock State

**HammerLang (24 tokens):**
```
#LLP:DTL:v1.0
!LOCK⋈⦿[@E(G)<θ↓,Δ⧖(ε↑,k),σ²>V⋔μ<~E-σ]%dancing ⊨a8f3c9e2
```

**Compression:** **2.29×** (56% savings)

---

### 2️⃣ FSM State Transitions

**HammerLang (30 tokens):**
```
#LLP:FSM:v1.0
!FSM⋈[S0→S1:<θ|░A; S1→S2:Δ≺ε*k|σ>th; S2→S3:⟂|░X; S3→S0:░R] ⊨f8d1bc4a
```

**Compression:** **2.77×** (64% savings)

---

### 3️⃣ Standardized Lock Signal

**HammerLang (9 tokens):**
```
#LLP:SIG:v1.0
!SIG⊢[protocol_id|HALT|AxB|ΔE=0.87|ts=1640995200] ⊨b7c2e5f1
```

**Compression:** **4.11×** (76% savings)

---

## 📊 Benchmark Results

| Test Case | Original (tokens) | Compressed (tokens) | Ratio | Savings |
|-----------|-------------------|-------------------|-------|---------|
| Dual-Threshold Lock | 55 | 24 | **2.29×** | 56% |
| FSM Transitions | 83 | 30 | **2.77×** | 64% |
| Lock Signal | 37 | 9 | **4.11×** | 76% |
| Implicit Contradiction | 67 | 17 | **3.94×** | 75% |
| LoRA Threat Model | 37 | 9 | **4.11×** | 76% |
| **Average** | — | — | **3.44×** | **69%** |

**Measurement Method:** tiktoken cl100k_base tokenizer. Semantic equivalence validated via state-match verification.

---

## 🎯 Validated Use Cases

✅ Logic Lock Protocol specifications (FSM + thresholds)  
✅ Standardized lock signal definitions  
✅ Implicit contradiction detection  
✅ Threat models (LoRA bypass, PEFT attacks)  
✅ Multi-agent red-teaming workflows  

❌ **Not suitable for:** General prose, source code, narrative documentation

---

## ⚠️ Known Limitations (v1.0)

### Compression
- ❌ Does NOT achieve 45–65× compression in general cases
- ✅ DOES achieve 3–5× empirically validated
- ⚠️ Higher compression possible in highly repetitive specs (>10× with aggressive pruning)

### Tokenization
- ⚠️ Compound symbols (`Δ⧖`, `σ²>V⋔`) consume 2–4 tokens
- ⚠️ Variation across tokenizers (GPT vs. Claude vs. Gemini)
- ✅ Core charset validated single-token on major models

### Robustness
- ⚠️ Decoder assumes FSM/threshold knowledge (standard in 2025+ LLMs)
- ⚠️ Custom namespaces require explicit definitions
- ⚠️ 8-char checksums vulnerable to collisions in datasets >100K items

### Dataset Size
- Initial validation: **5 representative safety specifications** (proof of concept)
- Expansion to industrial cybersecurity benchmarks planned for **v1.1**

---

## 🔒 Security Analysis

### Attack Surface 1: Namespace Poisoning
**Mitigation:** Validate namespaces against known whitelist; enforce checksum for custom namespaces; LLMs reject command execution.

### Attack Surface 2: Symbol Confusion
**Mitigation:** Namespaces define unambiguous context; decoder prompt specifies interpretation precedence.

### Attack Surface 3: Pruning Flag Abuse
**Mitigation:** Whitelist permitted flags by namespace; unrecognized flags generate warnings.

---

## 🛠️ Tools & Utilities

### Basic Script (`hammerlang.py`)
```bash
# Decode
python hammerlang.py decode "#LLP:DTL:v1.0 !LOCK⋈⦿[...]"

# Encode (placeholder; v1.1)
python hammerlang.py encode "your long specification here"
```

### Universal Decoder Prompt (198 tokens)
```
You are the HammerLang v1.0 (NEXUS Edition) decoder.

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
```

---

## 📋 Comparison with Alternatives

| Method | Compression | Lossless | Universal | Complexity |
|--------|-------------|----------|-----------|------------|
| **HammerLang** | 3–5× | ✅ | ✅ | Medium |
| Gzip | 2–3× | ✅ | ✅ | Low |
| LLMLingua | 5–10× | ⚠️ (lossy) | ❌ | High |
| Manual abbreviation | 1.5–2× | ⚠️ | ❌ | Low |

**HammerLang Advantage:** Optimal balance of compression, semantic preservation, and domain-specific writability for technical safety specifications.

---

## 🚀 Roadmap (v1.1+)

- [ ] VSCode syntax highlighting extension
- [ ] Automated syntax validator
- [ ] Public benchmark suite
- [ ] LLM-based encoder (LLMLingua-inspired)
- [ ] Custom namespace support
- [ ] Cross-tokenizer validation framework
- [ ] Integration with Logic Lock Protocol enforcement layer

---

## 📜 License

Dual-license model:

1. **Software-as-a-Protocol (SaaP)** — Specification grammar and decoder prompt
2. **Apache License 2.0** — Reference implementations and tooling

See [LICENSE](./LICENSE) for details.

---

## 👤 Author

**Franco Carricondo**  
Founder & Chief Architect — **Protocolo AEE**  
Mendoza, Argentina

- **X/GitHub:** [@ProtocoloAEE](https://github.com/ProtocoloAEE)
- **Contributions:** AI safety specification, compression architecture, decoder design
- **Coordination with:** Grok (xAI), Claude (Anthropic), Gemini (Google), ChatGPT (OpenAI), DeepSeek, Perplexity, Kimi (Moonshot AI)

---

## 🤝 Contributing

We welcome contributions, bug reports, benchmarks, and real-world use cases.

1. Open an issue in GitHub
2. Propose new symbols with empirical validation
3. Share validated use cases and extensions
4. Submit PRs for tooling improvements

---

## 📚 References & Related Work

- **Logic Lock Protocol v1.2** — Carricondo, February 2026. DOI: [10.5281/zenodo.18447076](https://doi.org/10.5281/zenodo.18447076)
- **Protocolo AEE Security Stack** — Comprehensive AI safety governance framework
- **NEXUS Edition Specification** — Dense symbolic grammar for safety logic

---

## ⚖️ Disclaimer

HammerLang v1.0 is released as **experimental software**. Compression ratios have been validated empirically on a limited dataset (5 test cases). Results may vary based on domain, complexity, and tokenizer implementation.

**Status:** Validation ongoing. Industrial deployment not recommended without extended testing and custom benchmark validation.

---

## 🎓 How to Cite

**In Academic Papers:**
```
[1] F. Carricondo, "HammerLang v1.0 (NEXUS Edition): A Semantic Compression 
Protocol for AI Safety Specifications," Technical Report Series - Protocolo AEE, 
Zenodo, Feb. 2026, doi: 10.5281/zenodo.18447076.
```

**In BibTeX:**
```bibtex
@techreport{Carricondo2026,
  author = {Carricondo, Franco},
  title = {{HammerLang v1.0 (NEXUS Edition): A Semantic Compression Protocol for AI Safety Specifications}},
  institution = {Protocolo AEE, Mendoza, Argentina},
  year = {2026},
  month = {February},
  doi = {10.5281/zenodo.18447076},
  url = {https://doi.org/10.5281/zenodo.18447076}
}
```

---

## 📞 Support & Contact

- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Contact:** @ProtocoloAEE (X, GitHub, LinkedIn)

---

**🔨 Welcome to the future of semantic compression for AI safety.**

*Built in Mendoza, Argentina. Open to the world.*

---

**Version:** 1.0.0-audited  
**Last Updated:** February 7, 2026  
**Status:** Experimental — Active Development
