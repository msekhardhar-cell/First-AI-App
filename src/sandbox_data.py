"""OmniChat AI - Rich Sandbox Demonstrations for Judge Evaluation without API Keys."""

SANDBOX_RESPONSES = {
    "default": """### Welcome to OmniChat AI (Sandbox Mode) ⚡

I am operating in **Judge Sandbox Mode**, designed so you can explore all features—including token streaming, persona switching, interactive quiz generation, and artifact canvas rendering—without needing your own API key.

Here is what you can try:
1. **Explore Personas:** Switch to *Senior Code Architect* or *Academic Study Partner* in the sidebar.
2. **⚔️ Model Battle Mode:** Pit two AI models side-by-side to compare reasoning and latency!
3. **Interactive Quiz:** Click the **"🎯 Launch Quiz"** button above to launch an interactive quiz!
4. **Artifact Canvas:** Notice the right panel showing live rendered diagrams and structured code.

```mermaid
flowchart LR
    A[User Request] --> B[OmniChat Engine]
    B --> C{Battle Mode?}
    C -->|Yes| D[Dual Streaming Arena]
    C -->|No| E[Single Model Stream]
    D --> F[Artifact Canvas & Quiz Engine]
    E --> F
```

Feel free to click any of the starter prompt chips or ask any question!""",

    "code_architecture": """### Senior Code Architect Analysis: Microservices vs Modular Monolith

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
""",

    "study_physics": """### Academic Study Partner: Understanding Quantum Entanglement 🎓

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
Even though the correlation is instantaneous, **entanglement cannot transmit classical information or Morse code faster than light**. Because the outcome at Earth is fundamentally random, Earth's observer cannot *force* the particle to land in a specific state to send a deliberate message.
""",

    "summarizer_brief": """### Executive Brief: AI System Readiness & ROI Matrix ⚡

**Subject:** Deployment Strategy for First-AI-App  
**Target:** Devpost Challenge Evaluation  
**Status:** Green (Production Prototype Verified)

| Metric | Target | Verified Performance | Status |
| :--- | :--- | :--- | :--- |
| **Response Latency** | < 1.5s | ~0.4s (Streaming active) | ✅ Optimal |
| **UX Accessibility** | High Contrast | WCAG AA Compliant Obsidian Dark | ✅ Complete |
| **Judge Usability** | 100% Pass | Zero-Key Sandbox Active | ✅ Verified |
| **Interactive Modality** | Multi-Feature | Artifact Canvas + Live Quiz Widget | ✅ Complete |

#### Top 3 Executive Takeaways:
1. **Zero Barrier to Entry:** Evaluators can thoroughly stress-test every feature without signing up for third-party API keys.
2. **High Visual Fidelity:** Design tokens match modern developer tools (Vercel, Linear).
3. **Clear Next Milestones:** Cloud hosting deployment to Streamlit Community Cloud.
""",

    "nous_battle_response": """### Nous Hermes 3 Evaluation: Chain-of-Thought Synthesis 🏛️

<thinking>
Analyzing the architectural trade-offs between distributed microservices and a cohesive modular monolith.
Key parameters: network boundary latency, operational complexity overhead, database transactions, cognitive load on developers.
</thinking>

Here is my structured comparative assessment:

1. **Cognitive Load & Developer Velocity:**
   - *Modular Monolith:* Low. Single refactoring step across modules, compile-time type verification, zero RPC serialization overhead.
   - *Microservices:* High. Requires dedicated API contracts (Protobuf/gRPC), versioning discipline, and independent CI/CD pipelines per service.

2. **Data Consistency & Transactions:**
   - *Modular Monolith:* ACID guarantees via standard relational database transactions.
   - *Microservices:* Eventual consistency requiring the Saga Pattern or Outbox Pattern to prevent silent state divergence.

```mermaid
graph TD
    A[Monolith Single Transaction] -->|ACID Guaranteed| B[(Unified Database)]
    C[Microservice A] -->|Network Call / Outbox| D[Message Broker]
    D -->|Eventual Consistency| E[Microservice B]
```

**Verdict:** The majority of scaling problems prior to Series B are organizational, not computational. Choose a Modular Monolith first, enforce domain boundaries strictly, and decouple only when distinct scaling vectors demand independent deployment.
"""
}

def get_sandbox_response(query: str, persona_id: str, model_hint: str = "") -> str:
    """Returns a matching rich sandbox response based on query keywords, persona, or model."""
    if "nous" in model_hint.lower() or "hermes" in model_hint.lower():
        return SANDBOX_RESPONSES["nous_battle_response"]

    q = query.lower()
    if any(k in q for k in ["code", "architect", "microservice", "monolith", "bug", "python", "diagram"]):
        return SANDBOX_RESPONSES["code_architecture"]
    elif any(k in q for k in ["quantum", "physics", "study", "explain", "learn", "tutor", "entangle"]):
        return SANDBOX_RESPONSES["study_physics"]
    elif any(k in q for k in ["summary", "brief", "exec", "matrix", "roi", "takeaway"]):
        return SANDBOX_RESPONSES["summarizer_brief"]
    elif persona_id == "architect":
        return SANDBOX_RESPONSES["code_architecture"]
    elif persona_id == "tutor":
        return SANDBOX_RESPONSES["study_physics"]
    elif persona_id == "summarizer":
        return SANDBOX_RESPONSES["summarizer_brief"]
    else:
        return SANDBOX_RESPONSES["default"]
