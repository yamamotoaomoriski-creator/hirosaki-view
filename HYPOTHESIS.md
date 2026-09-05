# Hypothesis: Problem Exploration in AI Dialogue

## 1. Background and Framing

Current AI evaluations primarily focus on optimizing task-performance within a given, fixed problem set. We refer to this optimization axis provisionally as the **"X-axis"**. 

However, real-world tasks often require a different movement:
- Questioning underlying assumptions
- Searching for missing variables
- Reframing the core problem
- Generating new sub-problems or hypotheses not present in the initial prompt
- Altering the scope of exploration

We provisionally call this movement the **"Y-axis"**. 

## 2. Clarification of Terms

This project does not assume that the X-axis and Y-axis are strictly independent, nor does it claim to have discovered a novel cognitive law. The terms are used to separate two different types of conversational outcomes:
1. **Optimization (X-axis):** Solving a given problem deeper, faster, or with higher accuracy.
2. **Reformulation (Y-axis):** Changing what problem is being solved.

### Existing Related Concepts
This work relates to, and builds upon, existing concepts in AI and human-computer interaction, including:
- Problem formulation and reframing
- Iterative prompting and self-refinement
- Interactive machine learning
- Human-AI co-creation and co-adaptation
- Open-endedness in problem-solving
- Scientific discovery support systems

## 3. Core Question

Instead of asking, *"What are the capability limits of the AI model?"*, this framework asks:
> *Are we measuring the actual limits of the AI, or simply the boundaries of the problem definitions provided by the initial human prompt?*

## 4. Falsifiability & Limitations

- The hypothesis that iterative dialogues yield meaningful problem reformulation may be falsified if structured feedback only results in superficial verbose expansions rather than structural shifts in problem space.
- ITERATIVE conditions involve higher turn counts and direct human interventions, meaning any observed differences cannot be solely attributed to the model's autonomous behavior.
