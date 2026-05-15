# BSV AI Fellowship — Conversation Log
**Date:** May 15, 2026

---

**User:** Starting company research. Can you help me quickly gather key signals on these 8 companies? Looking for: funding, positioning, traction indicators. I'll start with the ones I know least about.

---

**Claude:** Let's get into it. I'll run searches on all 8 simultaneously — prioritizing the ones you have less context on.

*[Ran web searches on: Tigris Data funding, Atuin funding, BAML traction, Parasail Series A, Primitive.dev, Mem0 funding, Entire.io, Rasa 2026]*

Good. I have everything I need. Let me synthesize all 8 companies before we start building the framework.

---

### Company Research Dump 🗂️

Here's the signal picture, organized by what I found:

---

#### 🔵 BSV Portfolio Companies

**One critical discovery first: You listed 3 BSV portfolio companies. It's actually 4.**

Parasail launched in April 2025 with $10M in seed funding — **led by Basis Set Ventures**. That round included Threshold, Buckley, and Black Opal Ventures. Then Parasail raised a $32M Series A in April 2026, led by Touring Capital and Kindred. BSV led the seed and presumably held through. This matters for your ranking framing.

**Mem0:**
- $24M raised ($3.9M seed + $20M Series A Oct 2025, led by Basis Set Ventures)
- 41,000+ GitHub stars, 13M Python downloads
- 186M API calls in Q3 2025 (up from 35M in Q1 — ~30% MoM growth)
- AWS selected them as exclusive memory provider for their new Agent SDK
- Over 80,000 developers on the cloud service
- April 2026: new token-efficient memory algorithm, biggest gains on temporal queries (+29.6 points) and multi-hop reasoning (+23.1 points) — directly relevant to your Firecast thesis

**Entire:**
- $60M seed at $300M valuation, Feb 2026, led by Felicis — largest-ever seed for a developer tools startup per Felicis
- Thomas Dohmke (ex-GitHub CEO, Aug 2025 departure)
- Three components: Git-compatible database, semantic reasoning layer, AI-native interface
- First product: Checkpoints, an open-source CLI that pairs every AI commit with the prompts and reasoning that produced it

**Rasa:**
- $83.8M raised total, Series C (Feb 2024, $30M co-led StepStone + PayPal Ventures, with a16z, Accel, and BSV)
- 180 employees
- Pivoting from chatbot framework to agent platform ("Hello Rasa")
- Enterprise: two of world's top 3 banks, American Express, Deutsche Telekom

---

#### Non-Portfolio Companies

**Parasail:**
- $42M total ($10M seed BSV-led, $32M Series A Touring Capital + Kindred)
- 500B tokens/day, 40 data centers, 15 countries
- Pay-per-token, no long-term GPU contracts
- Founded by Mike Henry, ex-Groq CPO and Mythic founder
- 30% month-over-month revenue growth since launching April 2025

**Tigris Data:**
- $25M Series A Oct 2025, led by Spark Capital with continued a16z
- S3-compatible, zero egress fees
- 4,000+ customers including fal.ai, KREA, Hedra, Fly.io
- 8x YoY growth
- Team built Uber's global storage platform
- Total raised: $39.2M

**BAML (BoundaryML):**
- No disclosed funding found publicly
- Open-source DSL for typed, schema-driven LLM outputs
- Created the SAP (schema-aligned parsing) algorithm
- Strong developer love: "game changer," "10x faster than LangChain"
- Appears pre-Series A / YC-stage

**Atuin:**
- Founded 2024, backed by Generationship + Preston-Werner Ventures (GitHub co-founder Tom Preston-Werner)
- Shell history sync — SQLite-backed, E2E encrypted, cross-device
- Pivoting toward "Atuin Desktop" — runbook execution engine that looks like a doc but runs like a terminal
- Very early commercial stage; beloved by developers but unclear business model

**Primitive (primitive.dev):**
- Email infrastructure for developers: managed webhooks, SDKs for Node.js, Python, Go
- No disclosed funding
- Minimal public footprint — appears to be solo/micro-team project at this point

---

#### Surprising Strategic Signals

1. **BSV is more concentrated in this list than you knew.** They led Parasail's seed + led Mem0's Series A + participated in Entire's seed + participated in Rasa's Series C. That's four of eight companies.

2. **Entire is not a memory competitor to Mem0.** Different trust problems: Entire = *why* was this code written; Mem0 = *what* does this user need to know. The tension is more narrative than product.

3. **Mem0's April 2026 temporal reasoning gains (+29.6 points) are directly testable against your Firecast scenario.**

4. **BAML has no disclosed funding** — either YC/bootstrapped and we'd expect a raise soon, or it's a feature that gets absorbed.

5. **Primitive.dev appears pre-revenue/pre-seed** — no team page, no blog. Ranking it honestly probably means ranking it last on evidence weight alone.

---

Want to move into framework building now? I'd suggest we discuss your ranking criteria before committing to an order — the "why" matters as much as the list for BSV.

---

**User:** What is Entire actually building? $60M seed is massive but their website is vague. "Semantic reasoning layer for agents" - what does that mean in practice? And it's the ex-GitHub CEO which seems like a big deal?

---

**Claude:** *[Web searches: Entire.io Checkpoints product demo 2026, practitioner week-long review]*

Good, now I have a really clear picture. Let me break this down properly, because once you understand what Entire *actually is*, the investment framing shifts considerably.

---

### What Entire Is Actually Building

**The one-sentence version:** Entire is building Git-native audit trails for AI-generated code, starting with a CLI that attaches agent reasoning to every commit.

**What Checkpoints does concretely:**

Every agent commit creates a structured checkpoint object associated with that commit's SHA. Session data — prompts, responses, files modified, timestamps — lives on a separate `entire/checkpoints/v1` branch, keeping your main history clean.

So you commit code as normal. Checkpoints silently writes a parallel record: *why* that code exists. The code stays exactly the same — it just adds context as first-class metadata. Every change can be traced back not just to a diff, but to the reasoning that produced it.

**What the reasoning traces actually contain** (from a practitioner who tested it for a week):

- Prompts you gave the agent
- The agent's reasoning chain — what it considered, what it rejected
- Tool calls made (file reads/writes/shell commands)
- Before/after diffs
- Which model version was used, token usage

The real-world assessment was candid: the detail level is impressive — in a React refactor session, the checkpoint included reasoning about lifecycle method mappings, edge cases considered, why specific useEffect cleanup patterns were chosen. But after a week of normal usage, the checkpoint data was about 3x the size of the actual codebase, and there's no semantic search yet — you're scrolling through raw traces.

**The bigger vision:**

From Entire directly: "Checkpoints are our first step towards building a universal semantic reasoning layer for agents. Today, it gives you traceability and history. Tomorrow, it will become the shared memory that allows agents to coordinate, hand off context, and build together without collision or loss of understanding."

Checkpoints is the write path. The semantic reasoning layer is the read path — eventually letting multiple agents query *what was already tried, decided, or rejected* before starting work. That's the platform play.

---

### Is the ex-GitHub CEO Signal Real?

Yes, but it's nuanced.

**The bull case is legitimate:**

Dohmke isn't just a credentialed face. He was explicit: "We are not training models or building agents, we are integrating with them." Deliberate neutral infrastructure positioning. He watched the Copilot adoption curve from the inside and identified the real bottleneck: "The bottleneck in agentic coding is shifting from authoring to review. A pull request has the same problem — it shows changes to files I never wrote in the first place."

That's a real, observable problem. The review bottleneck is already here.

**The skeptical take:**

The $60M seed at $300M valuation is founder-fame pricing, full stop. The product launched is a CLI that writes JSON to a git branch. That's not $300M of product — it's $300M of: Dohmke + thesis + timing.

There's also a deeper risk: **Entire is betting that the SDLC needs to be rebuilt for agents.** That's a big, slow bet. It could take 5+ years to get there. Meanwhile GitHub itself, Atlassian, and Linear are not sitting still.

---

### The Key Clarification for Your Framework

**Entire is not a memory company. It's an auditability/governance company.**

So the Mem0 vs. Entire "portfolio tension" you identified? It's mostly not real. They're solving different trust problems:

- **Mem0:** Trust in what the AI *knows about you* persisting correctly across sessions
- **Entire:** Trust in *why the AI wrote this code* being auditable and reviewable

Where there IS real tension: both are pitching themselves as the "context layer for the agent era." The narrative positioning overlaps even if the products don't. BSV has a stake in both. Worth one honest sentence in your memo.

---

**User:** Just saw Parasail raised $32M Series A in April 2026 and generates 500B tokens/day. That's huge volume. Is this just commodity GPU brokerage or is there real defensibility here?

---

**Claude:** *[Web searches: Parasail defensibility vs Fireworks Baseten Together AI, Parasail kernel tuning technical differentiation, inference commoditization race to bottom 2026]*

Good question to push on. This is actually the hardest call in your whole portfolio ranking. Let me lay it out straight.

---

### What Parasail Actually Does (Under the Hood)

The positioning is "AI Supercloud" but the mechanics matter more than the branding. Three distinct layers:

**Layer 1: Multi-provider GPU aggregation.**
Parasail operates an inference-optimized cloud where some GPUs run internally, others are hosted by partners — access to GPUs in 40 data centers across 15+ countries. They buy on spot/liquidity markets and route behind the scenes. This is brokerage. Not inherently defensible.

**Layer 2: Automated kernel optimization.**
The part that's easy to miss in press releases: "Parasail replaces manual kernel tuning and performance engineering with automated systems." The claim: kernel configuration tuning across the fleet, so customers don't need dedicated performance engineering teams. If true and proprietary, this is a data-flywheel argument — more workloads → better optimization data → better performance → lower cost → more customers.

**Layer 3: No-contract, startup-accessible pricing.**
Pay-per-token, no long-term commitments. Henry argues this sets it apart from larger cloud companies and even better-funded competitors like Fireworks and Baseten. He's targeting the generation of AI-native startups who scale from zero to enterprise without rewriting infrastructure.

---

### The Honest Defensibility Analysis

**Definitely commodity:** The GPU aggregation / brokerage layer. Most serverless providers expose drop-in OpenAI-compatible endpoints — switching means changing the base URL and API key, nothing more. Parasail lives in this same world.

**Speed benchmarks — real but not decisive:** On Together AI's own throughput comparison page, Parasail appears alongside Fireworks, Baseten, Deepinfra, and Novita. Fast, but one of several fast options, not uniquely fast. Mid-pack on DeepSeek V3.1 throughput.

**The macro headwind is serious:** Cloud compute costs projected to compress 25–35% in 2026 due to overcapacity. AWS has a $20B custom silicon program. Hyperscaler bundling is the terminal threat.

**The potential moat:** Automated optimization at scale is the only genuinely interesting claim. But there's limited public evidence they've actually built this vs. described building it. Groq has real custom silicon. Fireworks has ex-PyTorch core team. Parasail's claimed routing intelligence is harder to verify.

**The most interesting signal — BSV's early conviction:** BSV led the seed before the 500B tokens/day headline. That's a revealed preference worth noting. Now they've held through a $32M Series A led by outsiders. Validation, not just loyalty.

---

### The Actual Investment Question

Not "is inference commoditizing?" (it is). The question is: **what does the market structure look like at scale?**

**Bear case:** Hyperscalers drop inference prices, bundle it into existing cloud relationships, and the startup inference cloud market collapses the same way PaaS startups got squeezed in 2015–2018.

**Bull case:** As agent workloads fragment across models (cheap for classification, expensive for reasoning, fine-tuned for domain), the multi-provider orchestration + cost optimization layer gets genuinely complex. A specialist that routes intelligently, auto-tunes, requires no contracts becomes the default for AI-native startups — like Stripe became default payments even though banks exist. The 30% MoM revenue growth is evidence the wedge is working right now.

---

### Bottom Line

**Parasail is a well-timed bet on the routing/optimization layer being a durable wedge, backed by a founder with the right pedigree (Groq CPO, Mythic founder) and real traction — but with a commoditization clock ticking from above.**

For your ranking: "strong traction, real risk" bucket. Not #1, but not dismissible. Note it as a BSV portfolio company regardless of where you rank it.

---

**User:** BAML does structured LLM outputs. But doesn't Pydantic + Instructor already solve this? And OpenAI has structured outputs built in now. What's the moat if foundation models just add this feature?

---

**Claude:** *[Web searches: BAML vs Instructor vs OpenAI structured outputs SAP algorithm, BAML BoundaryML business model funding 2026, OpenAI structured outputs accuracy degradation reasoning research 2025]*

Good question, and it's exactly the right one to ask before ranking BAML. Let me be direct about what I found.

---

### The Short Answer

Your instinct is correct as stated — but it's aimed at the wrong target. OpenAI's structured outputs *does* threaten part of BAML's value. But BAML's actual moat isn't where most people think it is, and neither is the risk.

---

### Why "OpenAI Has Structured Outputs" Isn't a Full Refutation

The core technical issue is real and documented by peer-reviewed research (UC San Diego, 2025, "The Format Tax"): requiring structured output substantially degrades reasoning and writing performance across open-weight models. The dominant cost enters at the prompt level — format-requesting instructions alone cause most of the accuracy loss, before any decoder constraint is applied.

This is the problem BAML's SAP algorithm directly attacks. Schema-Aligned Parsing takes a different approach: rather than requiring the model output to be valid JSON before interpretation begins, BAML's parser extracts structured data from whatever the model actually returns, using the declared schema as a guide.

What SAP handles in practice:
- Model wraps JSON in markdown code fence → SAP strips the fences
- Model emits trailing commas or unquoted values → SAP corrects them
- Reasoning model outputs chain-of-thought before the structured object → SAP identifies where structured content begins and parses from there
- String "123" where integer expected → SAP coerces rather than rejects

The benchmark: "BAML is more accurate and 2–4× faster than OpenAI FC-strict JSON tools across every model we tested." An independent benchmark (Instill AI) threw a reasoning-plus-structuring task at GPT-4o through multiple frameworks: OpenAI Structured, Instructor, Marvin, TypeChat, LangChain, and BAML. Only BAML and a few others produced valid JSON on every call; OpenAI's own structured mode failed correctness on the reasoning field despite perfect schema adherence.

---

### The Actual Threat Model — Three Layers

**Layer 1: SAP / parsing correctness.**
This is what OpenAI structured outputs directly competes with. OpenAI has improved here — recent closed-weight models appear to have closed the reasoning-degradation gap. Real pressure. But it only covers OpenAI. The moment you route to Anthropic, a local model, DeepSeek, or any open-source model, you're back to needing model-agnostic parsing. SAP is explicitly model-agnostic by design.

**Layer 2: BAML as a DSL / developer experience.**
The harder-to-copy part. VSCode playground (first LLM playground in an IDE), type-generated SDKs across Python/TS/Ruby/Go/Rust/Java/C#, CI/CD test primitives, prompt versioning as code. These are workflow tools, not a parsing library. OpenAI doesn't ship this — it's not their business.

**Layer 3: Provider-agnostic routing + fallbacks.**
"When OpenAI went down, BAML customers didn't, because BAML makes fallbacks easy." Retry policies, fallbacks, model rotation — statically declared in BAML. This *requires* being model-agnostic. OpenAI structurally cannot offer this.

---

### The Real Strategic Risk (Not OpenAI)

The honest threat is subtler: **models getting good enough that the format tax disappears entirely.** If future foundation models handle format constraints with zero degradation natively and across all providers, SAP's core value erodes. The DSL/tooling layer remains, but the defensibility weakens.

The other real risk: if you only use OpenAI and your schemas are flat, the native SDK is genuinely enough today. BAML's moat is strongest in messy multi-model, complex-schema, open-source environments. Simple single-provider setups may never need it.

---

### The Investment Problem with BAML

YC-backed. No Series A announced. No public revenue signal.

The strategic question: is BAML a **product** (standalone company) or a **feature** (acquired by Langfuse, absorbed into a framework, becomes a standard)?

The "React for AI" bull case is compelling — React won because it solved a real DX problem at the right abstraction layer and couldn't easily be displaced once embedded. If `.baml` files sit alongside application code with CI/CD tests as table stakes, switching costs accrue and it becomes infrastructure.

But React had Facebook distribution. BAML has developer love, MIT license, and a competitive environment where LangChain, LlamaIndex, Pydantic, and every inference provider is iterating on DX simultaneously.

---

### For Your Ranking

**High conviction on the problem. Uncertain on the business model. No funding signal to anchor a valuation thesis.** Worth watching closely at seed if they ever raise — but hard to rank #1 without knowing whether they're building a company or a library.

---

**User:** I'm seeing a pattern - most of these could get commoditized:
- BAML: feature not product
- Mem0: OpenAI has memory now
- Parasail: competes on price
- Tigris: storage always compresses margins
Only Entire feels like it might escape this. Am I being too bearish?

---

**Claude:** This is worth slowing down on. You're pattern-matching correctly in some places and overcorrecting in others. Let me push back specifically rather than generally.

---

### Where You're Right

**BAML as feature-not-product** — valid concern, strongest of the four. No disclosed funding, unclear monetization path, core parsing moat erodes if models improve. The risk is real.

**Parasail competing on price** — partially right. The GPU aggregation layer is commodity. Whether the optimization layer is defensible is genuinely uncertain. You're not wrong to flag it.

---

### Where You're Overcorrecting

**"OpenAI has memory now" doesn't threaten Mem0.**

This is the weakest of your four concerns. OpenAI's memory is walled-garden, siloed within ChatGPT, non-portable, and closed. It doesn't help a developer building a healthcare agent on Claude, a customer service bot on Llama, or a coding assistant that needs to remember preferences across five different tools.

The pitch isn't "memory for AI." The pitch is portable, cross-platform, model-agnostic memory infrastructure — like Plaid for memory. When OpenAI builds memory, it *validates the category*. Enterprises that see ChatGPT remembering things will immediately ask: "why doesn't our custom agent remember things?" That's a demand signal for Mem0, not a competitive threat.

The actual evidence: AWS named Mem0 the exclusive memory provider for their new Agent SDK *after* OpenAI shipped their memory feature. If "OpenAI has memory" killed the market, AWS wouldn't have done that. The 186M API calls in Q3 2025 vs 35M in Q1 is 30% MoM growth *after* OpenAI's memory release.

**Tigris isn't just storage margin compression.**

The zero-egress-fee structure isn't cosmetic pricing — it's a structural attack on AWS's business model. Amazon cannot match zero egress without cannibalizing billions in existing egress revenue. That's not a feature gap, it's an architectural hostage situation. The Fal.ai testimony — egress fees used to be the *majority* of their cloud spending — shows this lands in real P&Ls.

The AI-native features (bucket forking, point-in-time snapshots, per-agent credential scoping) don't exist on S3 at all. Purpose-built for agent workflows where you want ten parallel experiments sharing a dataset without copying it. A wedge that gets stickier as agentic architectures mature.

---

### The Part You're Missing: Entire Has Its Own Commoditization Risk

You said Entire "might escape this" — I'd actually flip the analysis. Entire is arguably *more* exposed than Mem0 or Tigris, not less.

- Product shipped: CLI writing JSON to a hidden git branch
- Moat: entirely in the roadmap — the "universal semantic reasoning layer" doesn't exist yet
- $300M valuation at ~15 employees is almost entirely founder premium
- Commoditization vector is obvious and well-resourced: **GitHub itself.** They own the git layer, have Copilot data about how agents write code, have enterprise distribution. They could ship Checkpoints in a quarter. The reason they haven't is probably that it's not a priority yet, not that it's hard.
- Terminal risk: what if models get good enough that agents write obviously-reasoned code, eliminating the need for an audit trail before the platform matures?

---

### The More Useful Frame

Commoditization isn't binary. The question isn't "will margins compress?" — they will for everything on this list. The question is: **do you become the default before margins compress?**

S3 compresses margins. AWS still prints money on S3. Stripe competes on price. Stripe still has 40%+ gross margins. The companies that survive commoditization are the ones with distribution moats, not technical moats.

Run each company through that lens:

| Company | Distribution Signal |
|---|---|
| **Mem0** | 80K developers, AWS SDK exclusive, 21 framework integrations, ECAI academic credibility. Real and growing. |
| **Tigris** | 4K+ customers, 8x annual growth, fal.ai + Fly.io reference customers with public testimonials. |
| **Parasail** | 30% MoM revenue growth. Right side of agent infrastructure wave. |
| **BAML** | Beloved but not yet embedded. Highest execution risk. |
| **Entire** | Best narrative, least product. Distribution depends on habits forming before GitHub wakes up. |

---

### Bottom Line

You're not too bearish — you're **selectively bearish** in ways that accidentally favor the most speculative company (Entire) and penalize the one with the clearest distribution moat (Mem0).

The commoditization risk is real across the board. But "eventually competes on price" and "doesn't deserve investment" are different claims. The former is probably true for all eight. The latter depends entirely on whether they capture distribution before the compression hits.

**For your ranking:** Mem0 deserves more credit than your current framing gives it. Entire deserves more scrutiny.
