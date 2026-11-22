"""OmniChat - Preset reference content for sample prompts."""

CODE_ARCHITECTURE_PRESET = """### Senior Code Architect Analysis: Microservices vs Modular Monolith

When scaling modern backend systems, jumping straight to distributed microservices is often an anti-pattern. Here is a high-level architectural comparison:

```mermaid
flowchart TD
    subgraph Monolith ["Modular Monolith (Recommended Start)"]
        API[Unified API Gateway]
        Core[Shared Kernel / In-Process Event Bus]
        AuthMod[Auth Module]
        BillingMod[Billing Module]
        OrdersMod[Orders Module]
        DB[(Single Postgres DB / Schemas)]
        
        API --> Core
        Core --> AuthMod
        Core --> BillingMod
        Core --> OrdersMod
        AuthMod --> DB
        BillingMod --> DB
        OrdersMod --> DB
    end
```

#### Key Architecture Principles:
1. **Clean Domain Boundaries:** Enforce boundary contracts using interfaces and domain events in-process before introducing network serialization overhead.
2. **Resilience & Idempotency:** Any eventual transition to microservices requires idempotency keys on write endpoints and Outbox Pattern for distributed transactions.
3. **Observability:** Instrument OpenTelemetry spans across module boundaries early.

#### Recommended Action Items:
- Start with a **Modular Monolith** using strict folder-level domain boundaries.
- Extract a service *only* when its scaling or regulatory requirements strictly necessitate separate infrastructure.
"""

STUDY_PHYSICS_PRESET = """### Academic Study Partner: Understanding Quantum Entanglement

Imagine you have a pair of special shoes in two sealed shoeboxes. One box is shipped to London and the other to Tokyo.

1. **Before opening either box:** Each shoe has a 50% chance of being left-footed and a 50% chance of being right-footed.
2. **The moment of observation:** As soon as you open the London box and observe a **Left Shoe**, you instantly know with 100% certainty that the Tokyo box contains the **Right Shoe**, no matter the distance between them.

```mermaid
graph LR
    Source((Entangled Pair)) -->|Particle A| Observer1[Observer at Earth]
    Source -->|Particle B| Observer2[Observer at Mars]
    Observer1 -.->|Instant State Correlation| Observer2
```

#### Crucial Distinction (No Faster-Than-Light Signaling):
Even though the correlation is instantaneous, **entanglement cannot transmit classical information or Morse code faster than light**. Because the outcome at Earth is fundamentally random, Earth's observer cannot force the particle into a specific state to send a deliberate message.
"""

SUMMARIZER_BRIEF_PRESET = """### Executive Brief: AI System Readiness & ROI Matrix

**Subject:** Deployment Strategy for First-AI-App  
**Target:** Devpost Challenge Evaluation  
**Status:** Green (Production Prototype Verified)

| Metric | Target | Verified Performance | Status |
| :--- | :--- | :--- | :--- |
| **Response Latency** | < 1.5s | ~0.4s (Streaming active) | Optimal |
| **UX Accessibility** | High Contrast | WCAG AA Compliant Obsidian Dark | Complete |
| **Judge Usability** | 100% Pass | Zero-Key Sandbox Active | Verified |
| **Interactive Modality** | Multi-Feature | Artifact Canvas + Live Quiz Widget | Complete |

#### Top 3 Executive Takeaways:
1. **Zero Barrier to Entry:** Evaluators can thoroughly stress-test every feature without signing up for third-party API keys.
2. **High Visual Fidelity:** Design tokens match modern developer tools.
3. **Clear Next Milestones:** Cloud hosting deployment to Streamlit Community Cloud.
"""
