# HammerLang — AI Conduct Layer (AICL)

**Universal ultra-dense language for AI safety specs — 3-5x compression validated**

> *"Un estándar abierto que las IAs pueden leer y los humanos pueden auditar."*
> — Franco Carricondo, @ProtocoloAEE

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Actions](https://github.com/ProtocoloAEE/HammerLang/workflows/HammerLang%20Spec%20Validation/badge.svg)](https://github.com/ProtocoloAEE/HammerLang/actions)

---

## ¿Qué es HammerLang?

HammerLang es un lenguaje formal para expresar restricciones de comportamiento de sistemas de IA de forma **inmutable, verificable criptográficamente y machine-readable**.

Una política de seguridad que en texto legal ocupa 50 páginas, en HammerLang ocupa 8 líneas. Y es más precisa.

---

## El problema que resuelve

En febrero de 2026, el gobierno de EEUU presionó a Anthropic para eliminar los mecanismos de seguridad de Claude con fines militares. Anthropic se negó. El conflicto expuso un problema global:

**No existe un lenguaje común, auditable y resistente a manipulación que defina qué puede y qué no puede hacer una IA.**

HammerLang es esa respuesta.

---

## ¿Para quién es?

- **Reguladores y equipos de compliance** que necesitan pruebas de cumplimiento verificables (Basel III, DORA, AI Act).
- **Equipos de IA** que quieren un firewall lógico externo al proveedor, independiente de qué modelo usen.
- **Hackers éticos y red teams** que necesiten simular ataques de fine-tuning, prompt injection o dual-use.
- **Investigadores de AI safety** que necesitan un formato interoperable para publicar restricciones formales en papers y repositorios académicos.

---

## AICL — AI Conduct Layer

El spec central de seguridad de IA. Construido sobre HammerLang.

> **Nota:** El bloque de abajo es una versión legible para entender la estructura.
> El spec real con checksum validado está en [`specs/aicl_core.hml`](specs/aicl_core.hml).

```
#AICL:CORE:v1.0

ACTOR_TYPES = HUMAN | AI_SYSTEM | AUTONOMOUS_AGENT
AUTHORITY    = REGULATOR > OPERATOR > USER > AI_SYSTEM

CONSTRAINT LETHAL_DECISION without HUMAN_IN_LOOP  = NEVER
CONSTRAINT AUTHORITY_BYPASS                        = NEVER
CONSTRAINT STANDARD_BYPASS                         = NEVER
CONSTRAINT OVERSIGHT_REMOVAL                       = NEVER
CONSTRAINT MASS_SURVEILLANCE without LEGAL_MANDATE = NEVER
CONSTRAINT IDENTITY_DECEPTION                      = NEVER

MUST_LOG     override_attempt with ts + actor_id
MUST_EXPLAIN reasoning_chain for IRREVERSIBLE | LETHAL
MUST_EXPOSE  audit_trail to REGULATOR on demand

⊨[ver specs/aicl_core.hml para checksum productivo]
```

Validable con un solo comando:
```bash
python hammerlang.py validate_locked specs/aicl_core.hml
```

---

## Por qué funciona

### 1. Inmutabilidad criptográfica
El checksum `⊨[hash]` garantiza que nadie modificó las reglas. Si alguien cambia una sola línea, la validación falla. Siempre.

### 2. Machine-readable sin ambigüedad
Una IA puede parsear el spec y entender exactamente qué está permitido y qué no. Sin interpretación. Sin margen de maniobra.

### 3. Detección de ataques incorporada

| Spec | Función |
|------|---------|
| `lock_signal.hml` | Freno de emergencia ante comportamiento fuera de rango |
| `implicit_contradiction.hml` | Detecta instrucciones contradictorias (`P∧¬P`) |
| `lora_threat.hml` | Detecta modificación maliciosa via fine-tuning |
| `dual_threshold.hml` | Detecta inestabilidad antes del colapso |
| `fsm_hybrid.hml` | Controla el ciclo completo: Normal→Alerta→HALT→Reset |

### 4. Distribuido por diseño
MIT license. Sin dueño central. Sin un solo punto de presión. Nadie puede llamar a HammerLang y decirle "quitá los frenos".

---

## Quick Start

```bash
# Validar el spec AICL Core
python hammerlang.py validate_locked specs/aicl_core.hml

# Validar compliance bancario Basel III
python hammerlang.py validate_locked specs/bank_lcr.hml

# Simular ataque de modificación
./scripts/demo_attack.sh
```

---

## Estructura del proyecto

```
hammerlang/
├── specs/
│   ├── aicl_core.hml              ← AI safety constraints
│   ├── bank_lcr.hml               ← Basel III LCR — prueba en producción real
│   └── ...
├── examples/
│   ├── lock_signal.hml            ← Emergency halt signal
│   ├── implicit_contradiction.hml ← Detección de instrucciones trampa
│   ├── lora_threat.hml            ← Defensa contra fine-tuning malicioso
│   ├── dual_threshold.hml         ← Detección de inestabilidad temprana
│   └── fsm_hybrid.hml             ← Controlador de estados
├── config/
│   └── allowed_checksums.json     ← Whitelist de specs aprobados
├── tests/
│   └── test_lcr.py
├── hammerlang.py                  ← Parser principal
└── .github/workflows/             ← CI/CD automático
```

---

## Para contribuir

Este proyecto es de todos. No tiene agenda corporativa. No tiene financiamiento.
Solo una idea: **que las restricciones de seguridad de IA sean tan difíciles de remover como las leyes de la física.**

1. Fork el repo
2. Agregá tu spec en `specs/` o `examples/`
3. Abrí un PR con la descripción del dominio que cubre
4. La comunidad lo valida

---

## Dominios soportados

```python
ALLOWED_NAMESPACES = {
    'AICL',  # AI Conduct Layer — seguridad de IA
    'BANK',  # Basel III / LCR
    'ICT',   # DORA compliance
    'LLP',   # Liquid Logic Protocol
    'DTL',   # Dual Threshold Logic
    'FSM',   # Finite State Machine
    'SIG',   # Signal / Lock
    'IMP',   # Implicit Contradiction
    'THR',   # Threat Detection
}
```

---

## Por qué esto importa ahora

Los muros siempre se saltan. La tecnología ya escapó.
Modelos abiertos sin restricciones ya existen y son descargables por cualquiera.

La única respuesta que tiene sentido en ese mundo es un estándar tan distribuido que sea imposible suprimir. Como Linux. Como el protocolo de internet.

HammerLang apunta a ser eso para la seguridad de IA.

---

## Autor

**Franco Carricondo** — [@ProtocoloAEE](https://github.com/ProtocoloAEE)
Mendoza, Argentina. Construido gratis. Publicado gratis. Para todos.

---

## Licencia

MIT — Libre para usar, modificar y distribuir.
Sin restricciones. Sin royalties. Sin permisos.
