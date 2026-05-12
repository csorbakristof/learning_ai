1. Custom Instructions (.github/copilot-instructions.md)

This is a global ruleset for your repository.

Copilot automatically reads this file and injects its contents into the "background" of every chat and code completion request.  How to use it: Create a file at .github/copilot-instructions.md.Best for:Coding Standards: "Always use functional components over class components."Libraries: "Prefer Tailwind CSS for styling; do not use Bootstrap."  Architecture: "Follow the Atomic Design pattern for the src/components folder."Effect: You don't need to repeat these rules; Copilot will "just know" them.

2. Custom Agents (.github/agents/)

Custom agents allow you to define personas with specific "skills" or specialized knowledge. You trigger these in chat using the @ symbol (e.g., @backend-expert).

How to use it:Create a folder: .github/agents/.Add a Markdown file, e.g., reviewer.agent.md.Use YAML Frontmatter at the top to define the agent's name and description.

3. Reusable Prompts (.github/prompts/)

Prompt files are slash commands (/) that act as templates for complex or repetitive tasks.

Instead of typing a long prompt, you just call the file.  How to use it:Create a folder: .github/prompts/.Add a Markdown file, e.g., scaffold-api.prompt.md

### Comparison of Customization Levels

| Feature | Location | Trigger | Use Case |
| :--- | :--- | :--- | :--- |
| **Custom Instructions** | `.github/copilot-instructions.md` | Automatic | Project-wide style/rules. |
| **Custom Agents** | `.github/agents/*.agent.md` | `@agentname` | Specialized roles (DBA, Reviewer). |
| **Reusable Prompts**| `.github/prompts/*.prompt.md` | `/command` | Complex, repetitive tasks. |

### Pro-Tip: The `/init` Command
If you are unsure where to start, you can type `/init` or `/create-instructions` in the Copilot Chat. In newer versions of VS Code (2026), this will analyze your project structure and offer to generate a starter `.github/copilot-instructions.md` file tailored to your tech stack.

Would you like help drafting a specific set of instructions for a particular framework or language you're using?
  