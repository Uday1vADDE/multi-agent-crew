# AI Content Creation Crew 🤖

A multi-agent content creation system built with CrewAI where three 
specialized AI agents work together to produce polished articles on any topic.

---

## What it Does

Give it any topic → three specialized agents collaborate → 
you get a well researched, written and edited article.

---

## How the Agents Work Together
Topic enters
↓
Researcher Agent → researches the topic → produces detailed notes
↓
Writer Agent → takes research notes → writes engaging article
↓
Editor Agent → takes article → polishes and perfects it
↓
Final polished article
Output of each agent automatically becomes input for the next one.

---

## CrewAI Core Concepts

**Agent** — a specialist with:
- `role` — job title
- `goal` — what they want to achieve  
- `backstory` — their background and expertise

**Task** — an assignment with:
- `description` — exactly what to do
- `expected_output` — what the result should look like
- `agent` — who performs this task

**Crew** — combines agents and tasks in order and runs them sequentially

---

## Why Multi-Agent Instead of One Agent with Many Tools?

You could give one agent all three jobs — research, write and edit.
But the more tools you give one agent, the more confused it gets.
It tries to do everything at once and quality drops.

Multi-agent approach:
- Researcher focuses ONLY on research
- Writer focuses ONLY on writing
- Editor focuses ONLY on editing

Each specialist produces better output in their domain.
Combined result is significantly higher quality.

---

## The Bug That Taught Me Prompt Caching

I got this error when running with Groq:
property 'cache_breakpoint' is unsupported

CrewAI recently added **prompt caching** — a feature that saves money 
by caching the fixed parts of agent prompts (role, goal, backstory) 
so they don't get resent on every API call.

Problem: Groq doesn't support this feature yet — only OpenAI and Anthropic do.

Fix:
```python
os.environ["CREWAI_DISABLE_PROMPT_CACHING"] = "true"
```

This taught me an important concept — in multi-agent systems, the same 
system prompt gets sent multiple times per agent run. Caching the fixed 
parts saves significant API costs at scale.

---

## Tech Stack
- **CrewAI** — multi-agent framework
- **Groq (Llama 3.3-70b)** — LLM brain for all agents
- **Streamlit** — web interface
- **python-dotenv** — API key management

---

## Run Locally

**Step 1 — Clone:**
```bash
git clone https://github.com/Uday1vADDE/multi-agent-crew.git
cd multi-agent-crew
```

**Step 2 — Install:**
```bash
pip install -r requirements.txt
```

**Step 3 — Create .env:**
GROQ_API_KEY=your-groq-key-here
**Step 4 — Run:**
```bash
streamlit run crew_agent.py
```

---

## What I Learned
- How CrewAI orchestrates multiple specialized agents
- Why specialized agents produce better output than one generalist agent
- What prompt caching is and why it matters for cost optimization
- How output flows automatically between agents in a crew
- Debugging compatibility issues between frameworks
