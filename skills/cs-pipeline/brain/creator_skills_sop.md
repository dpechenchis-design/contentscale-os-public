# SOP — How To Write Short-Form Scripts Using Creator Skills

## 1. SOP Control Information

| Field | Your answer |
| --- | --- |
| **SOP title** | How To Write Short-Form Scripts Using Creator Skills |
| **SOP owner** | Head of Content — keeps the skill library and this SOP accurate |
| **Executor** | Scriptwriter / Content Manager |
| **Reviewer** | Head of Content (final QC before client sees the script) |
| **Repository** | https://github.com/dpechenchis-design/creator-skills |
| **Applies to** | All retainer clients producing short-form (Reels / TikTok / Shorts) and edu-carousels |

---

## 2. Purpose

**What this SOP controls**

> This SOP owns the two-stage process every script goes through: **first the executor loads the client's context, then the executor picks which creator they want the script modelled on.** It ends with a finished script that carries the creator's structure and the client's voice.

**How the skills actually work — read this before Step 1**

> Each skill is a reverse-engineered content engine of one specific creator — the hook skeletons, script structures and CTA patterns pulled out of that creator's real, high-performing posts.
>
> A skill does **not** know your client. It knows a shape. So the sequence is always the same, and it is not interchangeable:
>
> **1. Load the client** → DNA dossier, offer, audience pains, tone of voice, and the real facts for this topic.
> **2. Pick the creator** → choose whose script structure you want to reproduce for this topic.
> **3. Generate** → the skill drops the client's material into that creator's proven skeleton.
>
> The output is the client's content in the creator's structure. Never the creator's opinions, never the creator's voice.

**Why this task matters**

> A skeleton pulled from a creator with 95M proven views converts far better than a script written from a blank page — the structure is already validated, so the writer only has to supply the client's facts. It also removes writer-to-writer variance: two different scriptwriters using the same engine produce scripts of the same shape and quality.

---

## 3. Scope

**This SOP includes**

1. Installing and updating the creator skill library on the executor's machine.
2. Loading the client's DNA, facts and proof into the session before anything is generated.
3. Choosing which creator the script will be modelled on, for this specific topic and goal.
4. Generating the script through that creator's skill and iterating on the output.
5. QC-ing the script against the creator's own rules before handoff.

**This SOP does not include**

1. Choosing which topics get filmed this week — owned by the content-plan SOP (bucket-planner).
2. Building the client DNA dossier — owned by the client-DNA SOP (client-dna-v2).
3. Viral research and topic mining — owned by the research SOP (viral-content-research / content-research-analyzer).
4. Writing captions and CTA copy for the post — owned by the caption SOP (short-form-caption).
5. Filming, editing and publishing — owned by the production SOP.

---

## 4. Required Inputs

Everything the executor needs before starting. If it is not on this list, the executor should not have to hunt for it.

**What you need before starting**

- **Brief** — the approved topic + the content goal (views / comments / sales) + the bucket it belongs to.
- **Client information** — the client DNA dossier: tone of voice, offer, audience pains, forbidden claims.
- **Reference** — the routing table in Step 3, used to decide which creator this topic gets modelled on.
- **Source material** — real facts from the client: numbers, case studies, dates, client names, personal story. Without these the engine produces an empty shell.
- **Access** — the skill library installed locally (Step 1) and Claude Code running in the client's project folder.

---

## 5. Roles And Ownership

**Owner:** Head of Content — decides which creators enter the library, approves changes to any SKILL.md, keeps this SOP current.

**Executor:** Scriptwriter / Content Manager — performs Steps 1–6 and delivers the finished script.

**Reviewer:** Head of Content — runs Step 7 QC and either approves for production or returns with a named reason.

---

## 6. Execution Process

### Step 1 — install the skill library

**Action:** Clone the repo and copy the skills into your Claude Code skills folder.

```bash
git clone https://github.com/dpechenchis-design/creator-skills.git
cd creator-skills
for d in */; do [ -f "$d/SKILL.md" ] && cp -R "$d" ~/.claude/skills/; done
```

Restart Claude Code. Verify with `/` — the skills appear in the list.

**Rule:** Re-run `git pull` and the copy loop at the start of every month. The library is updated when a new creator is reverse-engineered; running an outdated skeleton is the same as running an outdated brief.

**Example:** To install a single engine instead of all eight: `cp -R creator-skills/dan-martell-shortform ~/.claude/skills/`

---

### Step 2 — load the client into the session

**Action:** Before you touch a creator skill, put the client in front of the agent. Open Claude Code in the client's project folder and load, in this order:

1. **The DNA dossier** — tone of voice, offer, audience, pains, forbidden claims.
2. **The approved brief** — the topic and the goal (views / comments / sales).
3. **The raw factual material for this specific topic** — numbers, the case study, dates, names, the personal story, the objection this script answers.

**Rule:** The skill supplies the *form*. The client supplies the *content*. A creator skill loaded into an empty session will happily invent a founder story and a revenue number — that is the single most common failure of this process. If you cannot name at least one concrete number, date or case for this topic, stop and go back to the brief.

**Example:** "$40K/mo agency, 3 editors, churn was 40% before we changed onboarding, dropped to 8% in 6 weeks" — that is loadable. "The client grew a lot" — that is not.

---

### Step 3 — pick the creator you want to reproduce

**Action:** With the client already loaded, decide **whose script structure this topic should be built on.** You are not picking a favourite creator — you are matching the shape of the topic to the creator whose engine handles that shape. One topic = one creator.

| The topic is shaped like | Reproduce | The engine you get |
| --- | --- | --- |
| A B2B / SaaS / coaching lesson, "here is how the system works" | **Dan Martell** | Question→Hook→Explain→Illustrate→Lesson→Hook2 |
| A how-to for SMM / personal brand, teaching a tactic | **Ava** (@personalbrandlaunch) | 6 Pillars + 5X rule + structural skeletons |
| Money, numbers, ratings, "is this good or bad" | **James Conole** | X/10 Scorecard, Uncomfortable Flip, Dollar Amount Hook |
| A take, an opinion, an insider position — not a how-to | **Joao** (name.is.joao) | Skeletons S1–S7, command hook + open loop |
| Storytelling, creator life, BTS, escalating lists | **Jun Yuh** | 12 frameworks, "Name It to Claim It" rule |
| AI, funnels, lead magnets, keyword-comment CTA | **Ronin** (@roninxsocials) | ABT skeleton + 8 hook templates |
| An edu-carousel, story-first, named frameworks | **Sharran Srivatsaa** | 4 narrative arcs A–D |
| Lead-gen *strategy*, not a script at all | **Alex Hormozi** ($100M Leads) | Core Four, Lead Magnets, Rule of 100 |

**Rule:** Never blend two creators in one script. The skeletons carry different emotional logic — Joao takes a position, James Conole scores a number, Ava teaches a step. Mixing them produces a script that does none of the three. If a topic seems to need two, it is two topics.

**Rule:** Match the shape of the topic, not the industry of the creator. James Conole's engine is a scoring engine — it works for any topic that puts a number on something, not only for finance.

**Example:** Topic "most founders hire their first manager too early", client is a B2B coach. The obvious pick is Dan Martell — wrong. This is a *position*, not a system walkthrough. Reproduce **Joao**.

---

### Step 4 — invoke the creator's skill

**Action:** Write a prompt that names three things: **the creator**, **the topic**, and **the goal**. The skill activates on the creator's name, or you call it explicitly with `/skill-name`.

**Rule:** Name the creator in the prompt. Do not rely on the agent guessing — if the creator is not mentioned, the skill may not trigger at all and you get a generic script that looks fine and performs like nothing.

**Rule:** Do not re-paste the client facts here if you loaded them in Step 2 — point at them instead ("use the churn case from the DNA doc"). Re-pasting invites the model to treat them as the only facts that exist.

**Example:**

```
Take the Dan Martell short-form engine. Topic: hiring your first manager
too early breaks the founder. Goal — comments. Facts are in the DNA doc,
use the churn 40%→8% case.
```

```
Skeleton S4 from Joao, hot take: content managers optimise for the wrong
metric. Position — insider, I've seen it from the agency side.
```

```
Sharran carousel, arc A, topic: the first deal that nearly killed the business.
```

---

### Step 5 — iterate on the output

**Action:** Read the generated script against that creator's own reference file (`references/` inside the skill). Push back on the specific slot that is weak — hook, build-up, payoff, CTA — not on the whole script.

**Rule:** Fix one slot at a time and name it. "Rewrite the hook, the open loop closes too early" gets a fix. "Make it better" gets a different-but-equally-weak script.

**Example:** "The hook is a statement, not a command — S4 needs a command hook. Redo just the hook, keep everything below."

---

### Step 6 — self-QC before handoff

**Action:** Run the script through this checklist. Fix anything that fails before it reaches the reviewer.

- [ ] The skeleton is intact 1:1 — every slot of the chosen framework is present and in order.
- [ ] The hook works with the sound off and stands alone as the first line.
- [ ] Every claim is backed by a real client fact — no invented numbers.
- [ ] Tone of voice matches the client DNA, not the creator's voice.
- [ ] Length fits the format (short-form: spoken in 30–60s; carousel: slide count matches the arc).
- [ ] The CTA matches the goal set in the brief (views / comments / sales).

**Rule:** A script that breaks the skeleton "because it reads better" is a rewrite, not a script — send it back to Step 5.

---

### Step 7 — hand off for review

**Action:** Deliver the script into the client's content doc with the creator and framework named at the top, e.g. `Creator: Joao (nameisjoao-shortform) / Skeleton S4`.

**Rule:** Always record which creator was reproduced. When a script performs, the team needs to know which skeleton produced it — that is how the library gets better, and how you learn which creator fits which client.

**Example:** Reviewer approves → moves to production. Reviewer returns → names the failing slot and the executor goes back to Step 5.
