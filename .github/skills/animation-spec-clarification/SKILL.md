---
name: animation-spec-clarification
description: 'Clarify ambiguous SVG and SVG.js animation specs before implementation. Use when reading labeled SVG animation requirements, extracting missing decisions, asking focused clarification questions, resolving misunderstandings about motion, triggers, timing, labels, or visible styling, and updating the spec directly so implementation can proceed cleanly.'
argument-hint: 'Describe the animation spec or demo that needs clarification'
user-invocable: true
disable-model-invocation: false
---

# Animation Spec Clarification

Normalize ambiguous SVG and SVG.js animation requirements before implementation starts. Read the written spec and related SVG asset, identify only the missing decisions that materially affect code, ask focused questions, and update the spec directly so the implementation step is unambiguous.

## When to Use
- An SVG or SVG.js animation spec leaves out trigger, timing, phase order, movement semantics, or reset behavior
- The task references labeled SVG elements and the implementation depends on how those labels should behave
- The conversation has already surfaced misunderstandings and the spec needs to be tightened
- You want to convert a rough animation idea into an implementation-ready spec before writing code

## Outcomes
- A clarified spec with implementation-relevant decisions written down
- A short question set that avoids unnecessary back-and-forth
- Resolved wording for motion semantics, interaction rules, and visible styling expectations
- Fewer implementation mistakes caused by underspecified behavior

## Workflow
1. Start from the spec file and the target SVG asset.
Read the spec first, then inspect the SVG for actual labels, object types, and any visible style definitions that may affect implementation.
If no spec file or SVG asset is provided, ask the user to supply at least one before proceeding. Do not attempt to invent or assume spec content.

2. Extract concrete requirements.
Write down the parts that are already explicit:
- trigger type
- phase order
- movement targets
- duration
- easing
- visibility changes
- color/state changes
- reset behavior

3. Identify only implementation-critical ambiguities.
Do not ask broad or speculative questions. Ask only about missing decisions that would change the code. Common examples:
- page load vs click vs hover trigger
- one-shot vs loop vs phase progression
- center-to-center movement vs path-following vs boundary alignment
- whether clicks during animation are ignored, queued, or cancel motion
- whether color changes mean SVG attributes or visibly rendered CSS/style
- whether orientation/rotation changes are required
- whether the next click resets, advances, or restarts the sequence

4. Cross-check labels against the SVG.
If the spec refers to names like `marker_red` or `txt phase 1`, verify they actually exist in the SVG. If a name is missing or inconsistent, ask about the mismatch explicitly instead of guessing. If the user cannot resolve a label mismatch, document the assumed mapping explicitly in the spec and flag it with a TODO comment so the implementer is aware of the unresolved discrepancy.

5. Ask concise clarification questions.
Ask no more than 6 questions per clarification round. Prefer grouped, implementation-defining questions over many micro-questions. If there are natural defaults, offer them as options.

6. Reflect the clarified answers back into the spec.
Once answers are available, update the spec so the chosen behavior is written down explicitly. Do not rely on the chat transcript as the only source of truth.

7. Tighten wording where misunderstandings are likely.
If a phrase can be interpreted multiple ways, rewrite it in implementation terms. Example: replace "moves to home_red" with "moves from its original center to the center of `home_red`" when that is the intended behavior.

8. Stop when the spec becomes implementation-ready.
The goal is not exhaustive documentation. Stop when one reasonable implementation path is clearly defined.

## Decision Rules
- Prefer exact behavioral wording over shorthand phrases
- Treat the SVG labels and visible rendering as ground truth to verify against the text spec
- If the spec says to use a library such as SVG.js, make that implementation constraint explicit when omissions previously caused confusion
- If a behavior can be interpreted in multiple technically valid ways, ask rather than choose silently
- If an answer affects future maintenance, write it into the spec immediately

## Quality Checks
- Every animation phase has a clear trigger and effect
- Movement semantics are explicit
- Timing and easing are explicit where relevant
- Interaction rules during animation are explicit
- Label names in the spec match the actual SVG labels
- Visual state changes describe the actually visible styling behavior
- The updated spec is sufficient to implement without guessing

## Example Prompt Ideas
- Clarify this animation spec before implementation and ask only the necessary questions.
- Read this SVG animation spec and update it to remove ambiguous movement wording.
- Compare this spec to the labeled SVG asset and identify missing decisions.
- Turn this rough animation description into an implementation-ready spec for an SVG.js demo.
