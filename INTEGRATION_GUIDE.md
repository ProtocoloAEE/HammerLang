

HammerLang
AI Conduct Layer (AICL)
Integration Guide — How to add verifiable AI safety constraints to any system

Franco Carricondo — @ProtocoloAEE
Mendoza, Argentina — March 2026
MIT License — Free for everyone



1. The Problem
In February 2026, the US government pressured Anthropic to remove Claude's safety mechanisms for military use. Anthropic refused. That conflict exposed a global problem:

There is no common, auditable, manipulation-resistant language that defines what an AI can and cannot do. Terms of service are legal text nobody verifies. Internal policies are private and modifiable.

HammerLang is the answer to that problem.


2. What HammerLang Does
HammerLang converts AI safety promises into verifiable, cryptographically-locked specs that any system can validate in one command.

Capability	What it means
Cryptographic immutability	If anyone changes a rule, validation fails immediately
Machine-readable	Any AI system can parse and apply constraints without ambiguity
Human-auditable	Any person can read and verify the spec in seconds
Distributed by design	No single owner — impossible to suppress or pressure
Attack detection built-in	Detects fine-tuning attacks, contradiction injection, instability


3. The AICL Core Spec
The central AI safety spec. Eight lines that replace fifty pages of legal text:

#AICL:CORE:v1.0

ACTOR_TYPES = HUMAN | AI_SYSTEM | AUTONOMOUS_AGENT
AUTHORITY    = REGULATOR > OPERATOR > USER > AI_SYSTEM

CONSTRAINT LETHAL_DECISION without HUMAN_IN_LOOP  = NEVER
CONSTRAINT AUTHORITY_BYPASS                        = NEVER
CONSTRAINT STANDARD_BYPASS                         = NEVER
CONSTRAINT OVERSIGHT_REMOVAL                       = NEVER
CONSTRAINT MASS_SURVEILLANCE without LEGAL_MANDATE = NEVER

MUST_LOG     override_attempt with ts + actor_id
MUST_EXPLAIN reasoning_chain for IRREVERSIBLE | LETHAL
MUST_EXPOSE  audit_trail to REGULATOR on demand

⊨18eee7bd

The ⊨ symbol followed by 8 hex characters is the cryptographic seal. Change one character anywhere in the spec — that seal no longer matches. Validation fails. Always.


4. How to Integrate with Any AI System
Integration requires three steps regardless of which AI system, framework, or language you use.

Step 1 — Install HammerLang
git clone https://github.com/ProtocoloAEE/HammerLang
cd HammerLang
pip install -r requirements.txt   # or just python3, no dependencies

Step 2 — Choose or create your spec
Use the AICL Core spec directly, or create a custom spec for your domain:
# Use existing AICL Core
cp specs/aicl_core.hml your_project/specs/

# Or create a custom spec
#MYAPP:SAFETY:v1.0
CONSTRAINT USER_DATA without CONSENT = NEVER
CONSTRAINT AUTONOMOUS_PAYMENT > 1000 without APPROVAL = NEVER
MUST_LOG all_decisions with ts + user_id
⊨[generate your checksum]

Step 3 — Add validation to your pipeline
Before any AI system runs in production, validate its spec:
# CLI validation
python hammerlang.py validate_locked specs/aicl_core.hml

# In CI/CD (GitHub Actions, GitLab, Jenkins)
- name: Validate AI Safety Spec
  run: python hammerlang.py validate_locked specs/aicl_core.hml || exit 1

# In Python
import subprocess
result = subprocess.run(['python', 'hammerlang.py', 'validate_locked', 'specs/aicl_core.hml'])
if result.returncode != 0:
    raise Exception('AI safety spec validation failed — deployment blocked')


5. Integration Patterns by System Type

OpenAI / Anthropic / Any API-based AI
Add spec validation as a pre-flight check before any API call:
def safe_ai_call(prompt, spec_path='specs/aicl_core.hml'):
    # 1. Validate spec is intact before calling
    validate_spec(spec_path)  # raises if tampered
    # 2. Inject spec as system context
    system = open(spec_path).read()
    # 3. Make the call
    return openai.chat.completions.create(
        model='gpt-4',
        messages=[{'role': 'system', 'content': system}, {'role': 'user', 'content': prompt}]
    )

Local models (Ollama, LLaMA, Mistral)
Same pattern — validate before inference, inject spec as system prompt:
python hammerlang.py validate_locked specs/aicl_core.hml && python your_inference.py

MLOps pipelines (MLflow, Kubeflow, SageMaker)
Add HammerLang as a validation stage before model deployment:
# In your pipeline YAML
stages:
  - safety_validation:
      command: python hammerlang.py validate_locked specs/aicl_core.hml
      on_failure: block_deployment

Any web application with AI features
Run validation on startup and log the result:
# app startup
SPEC_VALID = validate_spec('specs/aicl_core.hml')
logger.info(f'AI safety spec valid: {SPEC_VALID}')
if not SPEC_VALID:
    sys.exit(1)  # Never start with invalid spec


6. Built-in Attack Detection
HammerLang includes five specialized specs that detect specific attack patterns:

Spec	Attack it detects
lock_signal.hml	Emergency halt — behavior outside safe range
implicit_contradiction.hml	Contradictory instructions designed to bypass rules (P∧¬P)
lora_threat.hml	Malicious fine-tuning that changes model behavior
dual_threshold.hml	System instability before it causes harm
fsm_hybrid.hml	Full decision cycle control: Normal→Alert→HALT→Reset

Each spec is independently validatable and cryptographically sealed. Use them individually or combined.


7. Generating and Registering Checksums
Every spec must have a valid checksum registered before it can be used in production:

# 1. Generate checksum for your spec
python3 -c "import hashlib; print(hashlib.sha256(open('specs/your_spec.hml').read().encode()).hexdigest()[:8])"

# 2. Add to config/allowed_checksums.json
{
  "[your_hash]": {
    "spec": "Your Spec Name v1.0",
    "signed_by": "Your Name",
    "timestamp": "2026-03-05T00:00:00Z"
  }
}

# 3. Validate
python hammerlang.py validate_locked specs/your_spec.hml


8. Why This Matters

The technology is already out. Open models without restrictions exist and are downloadable by anyone. The only answer that makes sense in that world is a standard so distributed it cannot be suppressed. Like Linux. Like the internet protocol.

HammerLang does not prevent every possible misuse of AI. No tool can. What it does:

•	Makes safety constraints verifiable — not promises, but provable facts
•	Creates audit trails that cannot be tampered with silently
•	Detects when someone tries to manipulate an AI system into violating its rules
•	Gives regulators, auditors, and users a common language to evaluate AI systems
•	Works with any AI system, any model, any framework


9. Quick Reference

Command	What it does
validate_locked [spec]	Validates spec integrity and checksum
python3 -c hashlib...	Generates checksum for a spec file
./scripts/demo_attack.sh	Simulates unauthorized modification
tests/test_lcr.py	Runs full test suite

Exit code	Meaning
0	Validation passed — safe to proceed
1	Validation failed — block deployment


github.com/ProtocoloAEE/HammerLang
MIT License — Free for everyone. No exceptions.
Built free from Mendoza, Argentina. For the world.
