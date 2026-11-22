# Demo Video Script: OmniChat

Target length: roughly 2 minutes.
Walkthrough for hackathon evaluators.
Local application: http://localhost:8505

---

## Walkthrough Steps

### 1. Introduction (0:00 - 0:25)
- Open the application at http://localhost:8505.
- Voiceover:
  "Hi everyone. This is OmniChat, a chat workspace built for the Build Your First AI App hackathon. Instead of a single text window, OmniChat provides a split workspace with a dedicated artifact canvas, dual-model comparison, and an interactive study quiz engine."

### 2. Starter Prompts & Artifact Canvas (0:25 - 0:50)
- Click the prompt chip: "Architect: Monolith vs Microservices".
- Show the answer streaming on the left.
- Point to the right canvas showing the rendered Mermaid diagram and download button.
- Voiceover:
  "When you ask an architectural or coding question, OmniChat separates the explanation from the deliverables. On the right, the Artifact Canvas automatically parses and renders the Mermaid system diagram. You can copy the code or download the diagram directly."

### 3. Model Battle & Free Model Scanner (0:50 - 1:15)
- In the sidebar, switch from "Standard Chat" to "Model Battle / Compare".
- Click "View / Rescan Free Models".
- Show the cards displaying discovered free models (Qwen, Solar Mini, Tencent Hy4, LongCat).
- Type a short question (e.g. "Explain the trade-offs of using Redis for caching") and send it.
- Show both Model A and Model B streaming side-by-side.
- Voiceover:
  "In Battle Mode, you can compare two models at the same time. OmniChat queries open inference endpoints to detect currently available zero-cost models. Both models answer side-by-side, displaying latency metrics and voting buttons."

### 4. Interactive Quiz Engine (1:15 - 1:40)
- Click "Launch Quiz" in the top bar.
- Click a radio option on Question 1 (get green feedback) and Question 2 (show explanation).
- Voiceover:
  "For study workflows, the app includes a self-grading quiz module. You select answers to get instant explanations and track your score."

### 5. Wrap-up (1:40 - 2:00)
- Show the sidebar sandbox notice.
- Voiceover:
  "Evaluators can test everything immediately in sandbox mode without entering an API key. The codebase is fully modular, documented, and available on GitHub. Thank you."

---

## Recommended Screenshots for Devpost

1. Split Canvas View: Chat message on the left, rendered Mermaid architecture diagram on the right.
2. Model Battle View: Side-by-side response streams with response times and voting buttons.
3. Free Model Scanner: Discovered model cards with context lengths and provider names.
4. Interactive Quiz View: Active quiz card showing correct answer confirmation and score banner.
