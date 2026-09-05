# Experimental Protocol (v0.1)

## 1. Objective
To compare how a model behaves under standard single-turn prompting versus an iterative, challenge-based dialogue protocol, focusing specifically on changes in problem definition and variable expansion.

## 2. Conditions

### Condition A: PLAIN (Baseline)
1. Input the initial question.
2. Record the AI's direct response.
3. End session.

### Condition B: ITERATIVE (Exploratory)
1. Input the initial question.
2. Receive the initial response.
3. Issue subsequent turns addressing:
   - Challenges to assumptions
   - Identification of missing variables
   - Reconsideration of the core problem statement
4. Record the final response and the sequence of state changes.

## 3. Metrics & Observations
Rather than grading "correctness," runs are evaluated based on structural shifts:
1. Initial problem definition
2. Newly emerged variables
3. Newly generated hypotheses
4. Newly generated sub-problems
5. Modified assumptions
6. Final problem formulation

## 4. Known Limitations & Caveats
- **Intervention Bias:** The ITERATIVE condition includes more user input and turns, introducing confounding variables. 
- **Non-Causal Proof:** This protocol does not prove causality between a specific question type and problem restructuring; it merely records observable shifts for third-party re-analysis.
