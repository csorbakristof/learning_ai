# Using LLMs

Practice, prompting patterns and the transiton from asking to collaborating with the AI.

The standard components, Context-Task-Constraint model:

- Persona: Assigning a specific role (e.g., "You are a senior data scientist"). Did they define the "who"?
- Task: A clear, imperative verb describing the action. Is the objective unambiguous?
- Context: Background info, target audience, or relevant data. Is there enough "why" and "where"?
- Constraints: Limits on length, tone, or forbidden topics. Did they set boundaries?- Format:The desired structure (Table, JSON, Markdown, Bullet points).Is the output ready for use?

The "Zero-Shot to Chain-of-Thought" Scale

- Level 1: Standard Prompting (Simple question/instruction).
- Level 2: Few-Shot Prompting (Providing 2–3 examples within the prompt).
- Level 3: Chain-of-Thought (CoT) (Instructing the AI to "think step-by-step").
- Level 4: Iterative Refinement (Prompting the AI to critique its own previous answer).
- Level 5: Meta-Prompting (Asking the AI to write the best prompt for a specific task).

Plus one: ask the AI to evaluate your prompt, rate it on a 1-10 scale, and suggest improvements.

Patterns at a Glance

- Persona: "Who are you?, Tone, style, and specialized jargon
- Few-Shot: "Follow my lead.", Data formatting and classification.
- Chain of Thought: "Slow down and think.", Logic, math, and complex reasoning.
- Constraints: "Stay inside the lines.", Adhering to strict project requirements.
- Iterative Refinement: "Better, not more.", Summarization and professional editing.

Wise Usage Checklist for Students

- Role Play: Assign a persona to set the context.
- Fact-Check: Verify at least one claim using an external source.
- Ethics Check: Look for bias or excluded groups in the output.
- Attribution: Clearly label AI-generated sections in final work.

## Cross-Curricular Creative Tasks

Focus: AI Literacy, Fact-Checking, and Interdisciplinary Application.

### Historical Interview Task (History)

The Task: Prompt an LLM to act as a specific historical figure (e.g., Leonardo da Vinci).

CS Focus: Iterative Prompting. Students must refine the "system prompt" to include specific constraints like 16th-century vocabulary or references to specific inventions.

Critical Thinking: Compare AI responses against textbooks to identify hallucinations.

### Algorithmic Poet Task (Literature)

The Task: Generate a poem in a specific style (e.g., Romanticism) about a modern technical topic like cybersecurity.

CS Focus: Pattern Recognition. Analyze how changing stylistic keywords or "temperature" settings alters the output.

### Data Bias Detective (Social Studies & Math)

The Task: Ask for a list of "10 famous scientists" and analyze the results for demographic bias.

CS Focus: Training Data Awareness. Students must engineer a "Debiasing Prompt" to ensure a globally representative output.

### Scientific Hypothesis Generator

The Task: Input raw lab data and ask the LLM to suggest three variables that might have skewed the results.

CS Focus: Input/Output Boundaries. Understanding that the AI is a brainstorming partner predicting patterns, not an "oracle" with eyes on the experiment.

## Prompt Design Patterns

Focus: Structural Engineering of AI Interactions.

### Persona Pattern (Drama & Psychology)

Concept: Assigning a specific role, background, and tone.

Task: Create three distinct "tutors" for a difficult concept (e.g., Photosynthesis)—a Pirate, a Professor, and an "ELI5" (Explain Like I'm Five) specialist.

Insight: Observe how lexical choice changes based on the persona constraint.

### Few-Shot Pattern (Linguistics & Math)

Concept: Providing 2–5 examples of the desired format before the final request.

Task: Build a "Sentiment Analyzer." Provide three examples: [Quote] -> [Speaker] -> [Tone]. Then, test the AI's accuracy on a new quote with and without the examples.

Insight: Teaches that pattern matching often beats long descriptions.

### Chain of Thought Pattern (Physics & Logic)

Concept: Forcing the AI to "think step-by-step" before providing a final answer.

Task: Solve a multi-step Physics word problem. Compare a "direct answer" prompt vs. a prompt that requires stating formulas and intermediate steps first.

Insight: Demonstrates how "scratchpad" space improves LLM reasoning.

### Constraint/Negative Pattern (Art & Design)

Concept: Using strict boundaries (e.g., "Do not use...", "Max 50 words").

Task: Summarize a Shakespearean play without using the main characters' names or the word "tragedy."

Insight: Teaches how to delimit the output space for professional or safety-conscious applications.

### Chain of Density Pattern (Journalism)

Concept: Iteratively making text more information-dense without increasing length.

Task: Start with a 200-word summary. Repeatedly prompt the AI to rewrite it in 150 words while adding more specific facts and entities.

Insight: Demonstrates token efficiency and information synthesis.

# Image and music generation

Focus: Multimodal AI, Prompt Engineering for Visual/Audio Content, and Cross-Domain Application.

### Historical Scene Reconstruction (History & Art)

The Task: Use an image generation AI (e.g., DALL-E, Midjourney, Stable Diffusion) to recreate a specific historical event or period setting.

Prompt Challenge: Students describe a scene from World War II, Renaissance Florence, or Ancient Rome, including architectural details, clothing styles, and atmospheric elements.

CS Focus: Descriptive Precision. Students must iterate on their prompts to refine details (lighting, perspective, historical accuracy).

Critical Thinking: Compare generated images with historical photographs or paintings. Identify anachronisms or artistic liberties.

### Molecular Structure Visualizer (Chemistry)

The Task: Generate visual representations of chemical molecules or reactions using descriptive prompts.

Prompt Challenge: Describe a complex molecule (e.g., caffeine, DNA helix, glucose) or a chemical process (oxidation, crystallization) in natural language.

CS Focus: Translating Scientific Language. Students learn to bridge technical terminology with visual descriptors (shapes, colors, spatial relationships).

Extension: Compare AI-generated visuals with standard chemistry diagrams. Discuss limitations and strengths for educational purposes.

### Literary Cover Art Designer (Literature & Design)

The Task: Create book cover art based on a novel's themes, mood, and key symbols without directly illustrating characters.

Prompt Challenge: Design covers for classics like "1984", "Pride and Prejudice", or "The Metamorphosis" using only symbolic and atmospheric elements.

CS Focus: Abstract Representation. Students translate narrative themes into visual metaphors and mood descriptors.

Critical Analysis: Evaluate how different prompt styles (minimalist vs. detailed) affect the commercial appeal and thematic accuracy.

### Physics Concept Visualization (Physics & Science Communication)

The Task: Generate educational illustrations of abstract physics concepts that are difficult to photograph.

Prompt Challenge: Create visuals for quantum superposition, electromagnetic fields, entropy, or relativity effects using analogies and metaphors.

CS Focus: Concept-to-Visual Translation. Students must find creative ways to represent invisible forces and abstract principles.

Discussion Point: Assess whether AI-generated images help or hinder understanding compared to traditional diagrams or animations.

### Period-Appropriate Soundtrack Composer (Music & History)

The Task: Use AI music generation tools (e.g., Suno, MusicGen) to create short musical pieces fitting specific historical periods or literary moods.

Prompt Challenge: Generate a 30-second piece that sounds like Baroque court music, 1920s jazz, medieval folk, or film noir atmosphere.

CS Focus: Stylistic Constraint Engineering. Students specify instrumentation, tempo, mood, and cultural markers in their prompts.

Interdisciplinary Connection: Pair generated music with historical events or literary scenes. Discuss authenticity vs. creative interpretation.

Critical Reflection: Compare AI compositions with actual period recordings. Identify what the AI captures well and what it misses about cultural authenticity.

