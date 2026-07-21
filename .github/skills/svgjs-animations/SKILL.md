---
name: svgjs-animations
description: 'Create or update concise HTML demo files that animate external SVG assets with SVG.js. Use when implementing click-driven or timed SVG animations from labeled SVG files, selecting elements by label, animating between object centers, updating visible SVG styling, and avoiding manual DOM or requestAnimationFrame logic when SVG.js already provides the feature.'
argument-hint: 'Describe the SVG animation demo or spec to implement'
user-invocable: true
disable-model-invocation: false
---

# SVG.js Animations

Create concise, readable HTML demo files that load external SVG assets and use SVG.js directly for SVG selection, styling, events, positioning, and animation.

## When to Use
- Implement a new HTML demo around an existing SVG asset
- Translate a written animation spec into an HTML + SVG.js demo
- Add click-driven phases or scripted animation sequences
- Fix an SVG animation that currently uses manual DOM traversal or custom interpolation logic
- Resolve SVG styling issues where visible colors come from inline style or CSS rather than plain SVG attributes

## Outcomes
- A minimal HTML demo that loads an external SVG asset
- SVG.js-based element lookup and manipulation
- Behavior aligned with the spec, including triggers, phases, timing, easing, and reset behavior
- Basic validation after edits

## Workflow
1. Start from the concrete anchor.
Read the spec and the target SVG file first. Extract the exact labels, trigger conditions, timing, easing, phase order, and any visibility or styling requirements.

2. Clarify missing behavior before implementation.
Ask only the questions that materially affect implementation, such as:
- What triggers the animation: page load, click, hover, or control button?
- Is the animation one-shot, looping, or phase-based?
- Is movement center-to-center, along a path, or to a bounding-box position?
- Should clicks during animation be ignored, queued, or cancel the current motion?
- Does a color change mean SVG attribute color or the visibly rendered style?

3. Inspect the SVG asset for actual labels and shape types.
Confirm that the labels referenced in the spec exist in the SVG. Verify whether targets are rects, circles, text, paths, or groups so positioning and styling use the correct SVG.js APIs.

4. Prefer SVG.js over manual implementation.
Use SVG.js where it already supports the task:
- Selection: `findOne(...)`
- Events: `on(...)`
- Styling: `css(...)`, `stroke(...)`, `fill(...)`, `addClass(...)`
- Positioning: `center(...)`, `cx()`, `cy()`, `move(...)`
- Animation: `animate(...).ease(...)`
- Lightweight state: `remember(...)`
Only use tiny non-SVG.js helpers for loading the SVG file or surfacing setup errors. Do not write custom `requestAnimationFrame` interpolation or low-level DOM selection if SVG.js already provides the behavior.

5. Build the smallest behavior slice first.
Implement the first phase or the first motion path first, using the fewest moving parts needed to prove the behavior. Then add the remaining phases without widening scope unnecessarily.

6. Encode motion from the spec literally.
When the spec says move between object centers, animate between centers. Do not reinterpret that as following a path perimeter unless the spec explicitly requires path following.

7. Handle visible styling, not just nominal attributes.
If text or shapes are styled through the SVG `style` attribute or CSS, update the visible style with SVG.js `css(...)` rather than only setting a plain SVG attribute. Preserve and restore original values when phases require resetting visual state.

8. Keep runtime behavior deterministic.
For phase-based interaction:
- Advance exactly one phase per trigger
- Ignore clicks during active animation when the spec says so
- Store original positions or styles once and reuse them for reset phases

9. Validate immediately after the first substantive edit.
Prefer a focused validation step right away:
- editor diagnostics for the touched file
- a narrow runtime check if available
- then continue only if the first slice works

10. Finish with concise code.
Remove redundant bookkeeping, duplicate lookup code, and obsolete manual logic once the SVG.js version is in place.

## Decision Rules
- If the spec names labels, treat labels as the source of truth and verify them in the SVG.
- If the spec and the visible behavior conflict, update the implementation to match the spec and then tighten the spec wording if needed.
- If a visible style change does not appear, inspect whether the source SVG defines color via `style`, `stroke`, or `fill`, then update the property that actually controls rendering.
- If SVG.js can express the behavior directly, prefer that over custom helper code.
- If a library-free helper remains necessary, keep it tiny and local.

## Quality Checks
- SVG.js is used for the main interaction and animation behavior
- Labels referenced by the spec exist and are targeted correctly
- Motion semantics match the spec exactly
- Phase transitions and click-lock behavior match the spec
- Visible colors and resets behave correctly on the actual SVG elements
- The result is short, readable, and free of unnecessary state or manual animation code

## Example Prompt Ideas
- Create an SVG.js demo from this spec and SVG file.
- Refactor this SVG animation to use SVG.js instead of manual DOM code.
- Implement a three-phase click animation using SVG.js and these labeled SVG elements.
- Fix this SVG.js demo so text color changes affect the visible SVG styling.
