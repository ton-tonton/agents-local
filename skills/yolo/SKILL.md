---
name: yolo
description: "Orchestrate a complete feature workflow: PO defines requirements in plan.md, Lead Dev adds technical planning, and Dev executes the plan."
---

# YOLO Workflow: Plan -> Architect -> Execute

This workflow orchestrates a sequential development process involving three specialized agents (Product Owner, Lead Developer, Senior Developer) to transform a high-level request into working code.

[Extended thinking: This workflow chains three distinct personas. First, the Product Owner (PO) crystalizes the vague user request into concrete requirements and user stories stored in `plan.md`. Second, the Lead Developer analyzes these requirements to produce a technical design and task list, appending it to the same plan. Finally, the Developer executes this plan, implementing features and running tests. This separation of concerns ensures we built the *right* thing, build it the *right way*, and build it *correctly*.]

## Use this skill when

- You want to implement a feature from end-to-end starting with just a high-level description
- You need a structured plan (`plan.md`) before writing code
- You want to simulate a full team workflow (PO -> Lead -> Dev)

## Instructions

1.  **Analyze**: Understand the user's high-level request ($ARGUMENTS).
2.  **Define**: Have the PO agent create the product requirements.
3.  **Plan**: Have the Lead Dev agent add technical specifications.
4.  **Execute**: Have the Dev agent implement the code.
5.  **Deliver**: Use push-pr skill to open a Pull Request.

## Phase 1: Product Definition (PO)

### 1. Requirements Gathering & Story Creation
- Use Task tool with subagent @po
- Prompt: "You are the Product Owner. Create a file named `plan.md`. Analyze the user's request: '$ARGUMENTS'. Write a comprehensive product plan in `plan.md` including: 1) A clear content summary, 2) detailed User Stories with Acceptance Criteria, 3) Business Value/Rationale. Ensure specifications are clear enough for a technical lead to pick up."
- Expected output: A `plan.md` file containing structured product requirements.

## Phase 2: Technical Planning (Lead Dev)

### 1. Architecture & Implementation Planning
- Use Task tool with subagent @lead-dev
- Prompt: "You are the Lead Developer. Read the existing `plan.md` created by the PO. Update `plan.md` by appending a 'Technical Implementation Plan' section. Do NOT overwrite the PO's work. Add: 1) Architecture Overview, 2) Technical Stack confirmation, 3) A step-by-step Implementation Task list (Phase 1, Phase 2, etc.), 4) Testing Strategy. Ensure the tasks are atomic and actionable for the Developer."
- Context from previous: `plan.md` now contains both product and technical requirements.
- Expected output: `plan.md` updated with technical architecture and tasks.

## Phase 3: Execution (Dev)

### 1. Code Implementation & Testing
- Use Task tool with subagent @dev
- Prompt: "You are the Senior Developer. Read the complete `plan.md`. Execute the technical plan step-by-step. For each task defined by the Lead Dev: 1) Write the necessary code, 2) Create and run tests to verify the Acceptance Criteria, 3) Check off the items in `plan.md` as you go. If you encounter ambiguity, make a reasonable technical decision and document it."
- Context from previous: Completed `plan.md` guiding the implementation.
- Expected output: Fully implemented feature with passing tests and updated `plan.md` showing progress.

## Phase 4: Delivery

### 1. Create Pull Request
- Use the /push-pr skill to generate a description and open a pull request for the changes implemented in this workflow.

## Success Criteria

- [x] `plan.md` exists and contains User Stories, Architecture, and Task List
- [x] Code implementation matches the technical plan
- [x] Tests are written and passing
- [x] User stories' acceptance criteria are met
