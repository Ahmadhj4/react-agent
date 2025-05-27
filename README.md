#   React Agent – Enhanced Gemini-Powered AI (Based on Albanna Tutorials)

This project is based on a tutorial from **Albanna Tutorials**, which was then i enhanced to create a more dynamic AI agent using **Google’s Gemini API**.

##   Enhancements Added

- Structured agent loop with `Thought → Action → PAUSE → Observation → Answer`
- Dynamic function execution system (e.g., `calculate`, `average_dog_weight`)
- Action parser using Python regular expressions
- Modular design allowing easy extension with more actions
- Improved prompts and example use case for clarity and testing

##   Features

- **Gemini API Integration** for generative AI capabilities
- **Agent Memory and Dialogue Management** with role-based messages
- **Executable Actions** with dynamic observation and response
- Clean and modular code structure for learning or further development

##   Agent Logic Flow

1. **Thought** – Describes internal reasoning.
2. **Action** – Executes an available function.
3. **PAUSE** – Temporarily halts to await observation.
4. **Observation** – Receives and processes result from action.
5. **Answer** – Final response based on accumulated context.

## Setup
1. Clone repo:
   ```bash
   git clone https://github.com/your-username/repo-name.git
   ```
2. Add your Gemini API key to `.env`:
   ```
   GEMINI_API_KEY=your_key_here
   ```
3. Run:
   ```bash
   python react_agent.py
