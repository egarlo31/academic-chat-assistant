# Architecture Decisions

## 1. Purpose

This document defines how architectural decisions will be recorded during the development of the Academic Chat Assistant.

The purpose is to preserve the reasoning behind important technical decisions without creating a single large architecture document.

Each significant architecture decision will be documented independently inside the `decisions/` directory.

---

## 2. Decision Records

Architecture decisions will be stored using the following structure:

```text
architecture/
├── 01_architecture.md
├── 02_architecture_decisions.md
└── decisions/
    ├── AD-001_<decision_name>.md
    ├── AD-002_<decision_name>.md
    └── ...
```

Decision files should only be created when the development team makes a decision that materially affects the architecture or implementation of the system.

Examples include:

- LLM execution strategy;
- LLM or model selection;
- frontend technology;
- backend technology;
- persistence strategy;
- containerization strategy;
- conversation context management;
- evaluation infrastructure.

---

## 3. Decision Format

Each Architecture Decision Record should use the following minimum structure:

```markdown
# AD-XXX — Decision Name

**Status:** Accepted

## Decision

Description of the selected solution.

## Rationale

Explanation of why the team selected this solution.

## Consequences

Relevant technical implications of the decision.
```

Additional sections should only be added when they are necessary to understand the decision.

---

## 4. Architecture Dependency

From this point forward, implementation decisions that affect the system architecture should be supported by an accepted Architecture Decision Record when appropriate.

The architecture described in `01_architecture.md` represents the general system structure.

The files inside `decisions/` will progressively define the technologies and implementation strategies used to realize that architecture.

When an accepted decision changes the architecture, the corresponding sections or diagrams in `01_architecture.md` should be updated.

Therefore:

```text
Project Requirements
        ↓
01_architecture.md
        ↓
Architecture Decisions
        ↓
Implementation
```

Architecture decisions should be based on project requirements and constraints rather than on technology preference alone.

---

## 5. Decision Lifecycle

A decision may use one of the following states:

- **Proposed** — currently under discussion.
- **Accepted** — approved by the development team.
- **Replaced** — superseded by a newer decision.
- **Rejected** — evaluated but intentionally not selected.

If an accepted decision is later changed, the original decision record should remain available for traceability and reference the decision that replaces it.

---

## 6. Current State

No implementation-specific architecture decisions are considered final until they are discussed and accepted by the development team.

The current architecture therefore defines the system at a logical level while leaving technology-specific decisions open.