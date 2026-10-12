# Architecture Decisions

## 1. Purpose

This document defines how architectural decisions will be recorded and managed during the development of the Academic Chat Assistant.

The purpose is to preserve the reasoning behind important technical decisions without creating a single large architecture document.

The project will use Architecture Decision Records (ADRs) to document decisions that materially affect the system architecture, implementation, maintainability, or extensibility.

The current architectural direction includes:

- a modular layered monolith;
- Retrieval-Augmented Generation (RAG) as a required MVP component;
- a curated technical knowledge base;
- independent document indexing and retrieval components;
- a common interface for interchangeable LLM providers;
- GPT-OSS-120B through the Groq API as the initial inference configuration.

Architecture decisions must remain consistent with the project scope, system requirements, and architecture overview.

---

## 2. Decision Records

Architecture decisions will be stored using the following structure:

```text
architecture/
├── 01_architecture_overview.md
├── 02_architecture_decisions.md
└── decisions/
    ├── AD-001_rag_integration.md
    ├── AD-002_knowledge_storage_retrieval.md
    ├── AD-003_llm_provider_abstraction.md
    ├── AD-004_initial_llm_selection.md
    └── ...
```

Decision files should only be created when a decision materially affects the architecture or implementation.

Examples include:

- RAG integration strategy;
- knowledge base storage and retrieval strategy;
- LLM provider abstraction;
- initial LLM provider and model selection;
- embedding model selection;
- frontend and backend technologies;
- conversation context management;
- persistence strategy;
- containerization strategy;
- evaluation infrastructure.

Minor implementation details that do not materially affect the architecture do not require individual ADRs.

---

## 3. Decision Format

Each Architecture Decision Record should use the following minimum structure:

```markdown
# AD-XXX — Decision Name

**Status:** Proposed

## Decision

Description of the proposed or selected solution.

## Rationale

Explanation of why the team considers or selected this solution.

## Consequences

Relevant technical implications, limitations, and trade-offs.
```

Additional sections should only be added when necessary to understand the decision.

The status must reflect the actual decision lifecycle.

A proposed decision must not be documented as accepted until it has been approved by the development team.

---

## 4. Current Architecture Decisions

The following decisions define the current architectural direction.

The decisions are initially recorded as **Proposed** until formally reviewed and accepted by the development team.

| ID | Decision | Proposed Direction | Status |
|---|---|---|---|
| AD-001 | RAG Integration | Incorporate a minimal RAG workflow as a required MVP component. | Proposed |
| AD-002 | Knowledge Storage and Retrieval | Use a curated knowledge base with local vector storage, semantic retrieval, and metadata filtering. | Proposed |
| AD-003 | LLM Provider Abstraction | Define a common `LLMProvider` interface with interchangeable provider adapters. | Proposed |
| AD-004 | Initial LLM Selection | Use GPT-OSS-120B through the Groq API for initial inference. | Proposed |

These entries document the intended architectural direction and do not replace the corresponding ADR files.

### 4.1 AD-001 — RAG Integration

**Status:** Proposed

**Proposed Decision:**

Integrate Retrieval-Augmented Generation (RAG) into the Academic Chat Assistant as a required MVP component, consistent with the updated project scope.

The implementation will include:

- ingestion of reviewed technical documentation;
- document preprocessing and fragmentation;
- embedding generation;
- document indexing;
- retrieval of relevant technical information;
- integration of retrieved evidence into the LLM context;
- preservation of source references and applicable version metadata.

The RAG implementation will remain logically separated from the application and LLM integration components.

**Rationale:**

RAG is intended to improve technical grounding, reduce unsupported claims, and provide access to version-specific programming documentation.

**Consequences:**

- the architecture requires indexing and retrieval components;
- a searchable technical knowledge base becomes necessary;
- documentation quality and coverage directly affect retrieval performance;
- retrieval quality must be evaluated independently from response generation;
- advanced RAG capabilities remain outside the MVP.

### 4.2 AD-002 — Knowledge Storage and Retrieval

**Status:** Proposed

**Proposed Decision:**

Use a controlled technical knowledge base containing reviewed documentation for C, C++, Python, and the selected compiler and interpreter versions.

The initial retrieval strategy will prioritize:

- local vector storage;
- semantic similarity search;
- filtering using language and version metadata;
- preservation of document identifiers and source references.

The knowledge base will contain document fragments, embeddings, and relevant metadata.

The indexing workflow will operate separately from user interactions.

**Rationale:**

A local retrieval system provides a manageable foundation for the MVP without requiring distributed infrastructure or unrestricted external information retrieval.

**Consequences:**

- technical documentation must be reviewed before indexing;
- the system requires an embedding model;
- document and query embeddings must remain compatible;
- changing the embedding model may require rebuilding the index;
- metadata quality affects version-aware retrieval;
- the specific vector storage technology and embedding model remain pending.

Advanced retrieval strategies may be evaluated later if the initial implementation does not meet the established evaluation criteria.

### 4.3 AD-003 — LLM Provider Abstraction

**Status:** Proposed

**Proposed Decision:**

Define a common `LLMProvider` interface to separate application logic from provider-specific inference implementations.

Each provider will implement the same interface through an independent adapter.

The architecture will support:

- externally hosted LLM APIs;
- locally executed language models.

Provider selection will be managed through application configuration.

The initial implementation will require only the adapter for the selected external provider.

**Rationale:**

A common interface reduces coupling and allows the language model or inference provider to be replaced without modifying the main application workflow.

**Consequences:**

- application components will depend on the common interface;
- provider-specific code will remain inside adapters;
- switching providers may require implementing a new adapter;
- RAG indexing and retrieval will remain independent from the generative LLM;
- multiple simultaneous provider implementations are not required for the MVP.

The implementation may use the Strategy pattern and a simple provider selection mechanism.

### 4.4 AD-004 — Initial LLM Selection

**Status:** Proposed

**Proposed Decision:**

Use GPT-OSS-120B through the Groq API as the initial language model and inference provider.

The initial configuration will be:

| Property | Configuration |
|---|---|
| Provider | Groq |
| Model | GPT-OSS-120B |
| Model identifier | `openai/gpt-oss-120b` |
| Inference strategy | External API |
| Integration | `GroqProvider` adapter |
| Provider interface | `LLMProvider` |

**Rationale:**

The selected configuration provides an initial inference strategy without requiring the development team to deploy and maintain a large language model locally.

It allows the team to prioritize application functionality, RAG integration, and evaluation.

**Consequences:**

- inference depends on an external API;
- availability, rate limits, and usage restrictions depend on the provider;
- credentials must be managed securely;
- provider-specific integration must remain isolated;
- local inference remains a supported architectural extension but is not required initially.

The final selection must be reviewed against available resources, provider conditions, and evaluation requirements before acceptance.

---

## 5. Pending Architecture Decisions

The following decisions require additional analysis before implementation details can be finalized.

| Decision | Current Direction | Status |
|---|---|---|
| Embedding model | Lightweight model compatible with the documentation and query languages. | Proposed |
| Vector storage technology | Local vector database or equivalent searchable index. | Proposed |
| Document processing | Controlled ingestion of reviewed technical documentation. | Proposed |
| Chunking strategy | Preserve technical meaning and relevant documentation structure. | Proposed |
| Retrieval configuration | Semantic retrieval with language and version metadata filtering. | Proposed |
| Metadata schema | Preserve sources, document identifiers, languages, standards, and version information. | Proposed |
| Frontend technology | Web-based interface. | Proposed |
| Backend technology | Python-based API, with FastAPI as the current candidate. | Proposed |
| Conversation context | Maintain relevant history during active interactions. | Proposed |
| Evaluation storage | Structured local files for initial experiments. | Proposed |
| Containerization | Minimal reproducible deployment without distributed orchestration. | Proposed |

These decisions must be evaluated according to project requirements and constraints.

A separate ADR should only be created when the decision materially affects the architecture or introduces a significant technical trade-off.

Implementation details that can be changed without affecting the architectural structure do not require additional documentation.

---

## 6. Architecture Dependency

Implementation decisions must be supported by accepted Architecture Decision Records when appropriate.

The architecture described in `01_architecture_overview.md` represents the general system structure.

The files inside `decisions/` will progressively define the technologies and implementation strategies used to realize that architecture.

When an accepted decision changes the architecture, the corresponding sections or diagrams in `01_architecture_overview.md` must be updated.

The dependency relationship is:

```text
Problem Definition
        ↓
Project Scope
        ↓
System Requirements
        ↓
Architecture Overview
        ↓
Architecture Decisions
        ↓
Implementation
        ↓
Evaluation
```

Architecture decisions should be based on project requirements and constraints rather than technology preference alone.

Each significant decision should maintain traceability to the requirement or architectural concern that justifies it.

---

## 7. Decision Lifecycle

An Architecture Decision Record may use one of the following states:

| Status | Description |
|---|---|
| Proposed | The decision is under discussion and has not been formally approved. |
| Accepted | The development team has approved the decision for implementation. |
| Replaced | The decision has been superseded by a newer accepted decision. |
| Rejected | The proposed solution was evaluated but intentionally not selected. |

### 7.1 Decision Approval

A decision may transition from `Proposed` to `Accepted` when:

1. the team understands the architectural problem;
2. the proposed solution satisfies the relevant requirements;
3. the main alternatives and trade-offs have been considered;
4. the solution is feasible within project constraints;
5. the development team agrees to adopt the decision.

Formal approval does not require extensive documentation beyond the established ADR format.

### 7.2 Decision Changes

If an accepted decision is later changed, the original decision record should remain available for traceability.

The new decision should reference the decision it replaces.

The architecture overview must be updated when the change affects system components, responsibilities, or interaction flows.

---

## 8. Decision Evaluation Criteria

Architectural decisions should be evaluated using the following criteria:

- **Requirement Compliance:** the decision satisfies the relevant functional and non-functional requirements.
- **Technical Feasibility:** the solution can be implemented using available technologies and resources.
- **Maintainability:** the implementation can be understood and modified without unnecessary complexity.
- **Modularity:** the decision preserves separation of responsibilities and limits coupling.
- **Extensibility:** future changes can be introduced without requiring a complete redesign.
- **Reliability:** the solution supports the technical correctness and operational stability required by the MVP.
- **Cost:** implementation and operation remain compatible with available resources.
- **Development Time:** the solution can be completed and evaluated within the academic project schedule.
- **Scope Compliance:** the decision does not introduce unnecessary functionality outside the MVP.

The selected solution does not need to maximize every criterion.

Decisions should prioritize sufficient technical quality and simplicity over unnecessary architectural complexity.

---

## 9. Current State

The project currently defines the following architectural direction:

- **Architectural style:** modular layered monolith.
- **RAG:** required MVP component.
- **Knowledge base:** curated and reviewed technical documentation.
- **Retrieval:** local searchable index with semantic retrieval and metadata filtering.
- **LLM integration:** common provider interface with interchangeable adapters.
- **Initial inference:** GPT-OSS-120B through Groq.
- **Local inference:** supported through future provider implementations.
- **Evaluation:** independent assessment of retrieval and generated response quality.

These directions are consistent with the updated project scope and system requirements.

The architecture is defined at the logical level, while implementation-specific decisions remain subject to team approval.

The project will prioritize completing and evaluating the initial end-to-end workflow before introducing additional technologies, providers, or advanced capabilities.