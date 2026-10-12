# Project Scope

## 1. Project Goal

The goal of the project is to develop a Minimum Viable Product (MVP) of an academic programming assistant based on Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG).

The system will provide educational support for students working with C, C++, and Python by analyzing questions, source code, and error messages and generating contextualized explanations and guidance.

To improve technical reliability, the system will retrieve relevant information from a curated and reviewed technical knowledge base, allowing responses to be grounded in verifiable documentation and account for language standards, compiler versions, and interpreter versions when applicable.

The initial version will prioritize a complete and evaluable end-to-end workflow rather than a large number of advanced features.

## 2. MVP Scope

The Minimum Viable Product will implement the minimum functionality required to validate whether an LLM-based assistant supported by RAG can provide useful, technically grounded programming assistance in an academic context.

The MVP will include:

1. a web-based user interface;
2. a backend API;
3. an abstraction layer for LLM interaction;
4. support for programming-related user queries;
5. conversational context during an active interaction;
6. support for C, C++, and Python;
7. a curated technical knowledge base;
8. a minimal RAG pipeline for documentation indexing and retrieval;
9. source references and version-aware technical guidance;
10. an initial evaluation workflow using predefined tasks and criteria.

### 2.1 In Scope

The following capabilities are included in the MVP.

#### User Interaction

- submission of programming-related questions;
- submission of source code as part of a user query;
- submission of compiler or runtime error messages;
- display of generated responses;
- display of relevant technical references when applicable;
- maintenance of relevant conversational context during an active session.

#### Programming Support

The assistant may provide support for:

- programming concept explanations;
- code explanation;
- compiler error interpretation;
- runtime error interpretation;
- basic debugging guidance;
- identification of possible logical errors;
- suggestions for code correction;
- generation of small code examples;
- explanation of program behavior;
- explanations of language syntax and standard library functionality;
- guidance on language-standard and compiler compatibility when supported by available documentation.

#### Programming Languages

The MVP will support:

- C;
- C++;
- Python.

Support for additional programming languages is not required for the initial version.

#### Language and Compiler Version Coverage

The system will distinguish between programming language versions, language standards, compiler versions, and interpreter versions.

The following version coverage is proposed as the initial target and must be confirmed after reviewing the availability and suitability of technical documentation:

| Component | Proposed Coverage |
|---|---|
| C | C11, C17 |
| C++ | C++11, C++14, C++17, C++20, C++23 |
| GCC/G++ | GCC 9 through GCC 14 |
| Python | CPython 3.10 through 3.13 |

These ranges define the proposed documentation coverage rather than a guarantee of complete support for every language feature.

The MVP will:

- provide version-specific explanations when the required documentation is available;
- distinguish language-standard requirements from compiler-specific implementation support;
- avoid assuming that a compiler fully implements every feature of a particular language standard;
- identify version constraints when they affect the correctness of an explanation;
- acknowledge uncertainty when compatibility cannot be established from available sources.

Exhaustive compatibility verification across all combinations of language standards, compiler versions, operating systems, and architectures is not required.

Support for other compilers or interpreter implementations is not guaranteed by the initial MVP.

#### Technical Knowledge Base

The MVP will include a curated collection of technical documentation relevant to the supported programming languages.

The knowledge base may contain:

- language syntax and semantics;
- standard library documentation;
- compiler documentation;
- language-standard specifications or technical references;
- version compatibility information;
- explanations of common compiler and runtime errors.

Documentation incorporated into the knowledge base must undergo an initial review to assess its relevance, technical reliability, version coverage, and provenance.

The system will preserve sufficient metadata to identify:

- document source;
- source reference or URL;
- programming language;
- applicable language standard or version, when relevant;
- applicable compiler or interpreter version, when relevant.

The knowledge base will initially use a controlled collection of documents rather than unrestricted retrieval from the Internet.

Complete coverage of all language features, libraries, and compiler behaviors is not required.

#### Retrieval-Augmented Generation (RAG)

The MVP will implement a minimal RAG workflow to support technically grounded response generation.

The RAG component will provide:

- ingestion of selected technical documentation;
- document preprocessing and fragmentation;
- generation of embeddings;
- indexing and storage of document representations;
- retrieval of relevant technical information;
- filtering based on available language and version metadata;
- integration of retrieved information into the LLM context;
- preservation of source references associated with retrieved information.

Retrieval will be performed when relevant technical documentation is needed to support a user request.

The system should avoid presenting unsupported technical or compatibility claims as established facts.

When available documentation is insufficient or contradictory, the system should communicate the limitation rather than generate an unjustified conclusion.

The specific embedding model, retrieval strategy, and storage technology will be selected through subsequent architectural decisions.

#### Backend

The backend will:

- expose the required API endpoints;
- validate incoming requests;
- coordinate interaction with the RAG and LLM layers;
- prepare the information required for retrieval and model inference;
- manage relevant conversational context;
- return structured responses and source references to the frontend;
- handle application, retrieval, and inference errors;
- isolate application logic from the specific LLM provider.

#### LLM Integration

The system will provide a common interface for interacting with Large Language Models.

The architecture shall support two inference strategies:

- locally executed LLMs;
- externally hosted LLMs accessed through an API.

The initial implementation will use GPT-OSS-120B through the Groq API.

The LLM integration layer must remain independent from the RAG implementation so that changing the language model does not require redesigning the retrieval pipeline.

The MVP is not required to implement multiple providers simultaneously.

Additional providers and local inference implementations may be incorporated later through the common interface.

#### Evaluation

The project will include an initial evaluation process using predefined programming tasks.

Evaluation will consider dimensions such as:

- technical correctness;
- explanation correctness;
- clarity;
- relevance;
- educational usefulness;
- correctness of generated or corrected code when applicable;
- relevance of retrieved documentation;
- consistency between generated responses and retrieved evidence;
- source traceability;
- version compatibility when applicable;
- appropriate handling of insufficient documentation.

The evaluation should allow comparison between responses generated with RAG and responses generated without retrieved context.

The evaluation process will prioritize a controlled set of representative programming questions rather than exhaustive testing of every possible language feature.

### 2.2 Out of Scope

The following capabilities are explicitly excluded from the MVP.

#### Advanced AI Capabilities

- model fine-tuning;
- reinforcement learning;
- training a Large Language Model from scratch;
- multi-agent systems;
- autonomous agents;
- unrestricted tool use;
- autonomous code execution;
- autonomous modification of user files.

#### Advanced RAG Capabilities

The MVP will not require:

- unrestricted web crawling;
- real-time Internet search;
- automatic synchronization with external documentation websites;
- continuous knowledge base updates;
- autonomous discovery and ingestion of new sources;
- knowledge graphs;
- advanced multi-stage retrieval architectures;
- complex reranking pipelines;
- distributed vector databases;
- exhaustive indexing of all supported language documentation;
- automatic verification of every generated technical claim.

These capabilities may be considered after the initial RAG workflow has been implemented and evaluated.

#### Execution Infrastructure

The MVP will not initially require:

- distributed inference;
- GPU clusters;
- Kubernetes;
- complex container orchestration;
- production-scale cloud infrastructure;
- load balancing;
- high-availability infrastructure;
- large-scale observability systems.

#### Educational Platform Features

The MVP will not include:

- course management;
- assignment management;
- automated grading;
- student progress tracking;
- teacher dashboards;
- institutional authentication;
- learning management system integration.

#### IDE Integration

The MVP will operate as an independent web application.

Integration with development environments such as:

- Visual Studio Code;
- JetBrains IDEs;
- Jupyter;
- other code editors;

is considered future work.

#### Code Execution and Compatibility Verification

The MVP will not require:

- executing user-submitted code;
- compiling programs using multiple compiler versions;
- automatically testing code against different language standards;
- installing or managing multiple compiler environments;
- verifying compatibility through actual compilation or execution.

Compatibility guidance will initially rely on the reviewed technical documentation available in the knowledge base.

## 3. MVP Workflow

The system will operate through two main workflows: documentation indexing and user interaction.

### 3.1 Documentation Indexing Workflow

The documentation indexing workflow will prepare the technical knowledge base used by the RAG component.

The expected workflow is:

1. select technical documentation from relevant sources;
2. review the documentation for reliability, relevance, and version coverage;
3. preprocess and divide accepted documents into appropriate fragments;
4. associate fragments with source and version metadata;
5. generate embeddings for the document fragments;
6. store the indexed information for subsequent retrieval.

The simplified workflow is:

```text
Technical Documentation
        ↓
Source Review
        ↓
Document Preprocessing
        ↓
Chunking
        ↓
Metadata Assignment
        ↓
Embedding Generation
        ↓
Knowledge Base
```

This workflow will be executed when preparing or updating the knowledge base and will not be repeated for every user request.

### 3.2 User Interaction Workflow

The expected user interaction workflow is:

1. the user submits a programming-related question through the frontend;
2. the frontend sends the request to the backend API;
3. the backend validates the request and prepares the required conversational context;
4. the system identifies relevant language and version information when available;
5. the RAG component retrieves relevant technical documentation when needed;
6. the retrieved information and its references are incorporated into the model context;
7. the LLM integration layer constructs the model request;
8. the configured language model generates a response;
9. the backend processes the generated output and associated references;
10. the response is returned to the frontend;
11. the frontend displays the result to the user;
12. when applicable, the interaction is later evaluated using the project evaluation criteria.

The simplified workflow is:

```text
Student
   ↓
Frontend
   ↓
Backend API
   ↓
Request Validation
   ↓
Context Preparation
   ↓
RAG Retrieval
   │
   └── Technical Knowledge Base
   ↓
Retrieved Documentation
   ↓
Context Construction
   ↓
LLM Integration Layer
   ↓
Language Model
   ↓
Generated Response
   ↓
Backend
   ↓
Frontend
   ↓
Student
```

When retrieval is unnecessary or relevant documentation is unavailable, the system may continue using the appropriate conversational context, provided that unsupported technical claims are not presented as verified facts.

## 4. Assumptions

The project is based on the following assumptions:

- users have basic familiarity with programming concepts;
- users provide sufficient context when requesting debugging assistance;
- the selected LLM is capable of processing programming-related prompts;
- generated responses may contain errors and therefore require systematic evaluation;
- relevant technical documentation is available for the selected initial knowledge base;
- retrieved documentation may improve response reliability but cannot guarantee technical correctness;
- language and version compatibility claims depend on the coverage and reliability of available documentation;
- the application is primarily intended for experimentation and academic evaluation rather than production deployment;
- the MVP will initially use GPT-OSS-120B through Groq;
- the architecture will remain compatible with either local inference or external LLM APIs;
- the system does not need to support a large number of concurrent users during the initial evaluation.

## 5. Constraints

The project is subject to the following constraints:

### Time

The implementation should remain small enough to be completed and evaluated within the available academic development period.

RAG implementation will prioritize a controlled documentation collection and a functional retrieval workflow rather than extensive knowledge base coverage.

### Computational Resources

Local models and embedding generation must be compatible with the hardware available to the development team.

The project should avoid requiring specialized infrastructure that is not necessary for the MVP.

### Model Limitations

The quality of generated responses depends on the selected LLM and the relevance and reliability of retrieved information.

The system cannot guarantee that every generated response is technically correct.

RAG is intended to reduce unsupported technical claims, not eliminate hallucinations entirely.

### Documentation Availability

The quality and coverage of the knowledge base depend on the availability of suitable technical documentation.

Some language features, compiler behaviors, or version combinations may not have sufficient documentation within the initial collection.

The system must not imply complete compatibility coverage when the required evidence is unavailable.

### Documentation Usage

Technical documentation must be reviewed for applicable licenses, terms of use, and redistribution restrictions before being incorporated into the knowledge base.

### Scope Control

Features that do not directly contribute to the core academic assistant workflow, the minimal RAG implementation, or its evaluation should not be added to the MVP unless they become necessary to satisfy a defined requirement.

## 6. Future Work

The following capabilities may be considered after completion and evaluation of the MVP:

- expansion of the technical knowledge base;
- support for additional language standards and compiler versions;
- integration of additional official language and library documentation;
- automatic documentation synchronization;
- advanced retrieval and reranking strategies;
- improved version-aware retrieval;
- automated source consistency verification;
- code execution in an isolated sandbox;
- automated compilation and testing;
- integration with development environments;
- support for additional programming languages;
- comparison between multiple LLMs;
- local open-weight model optimization;
- fine-tuning or instruction tuning;
- student modeling and personalization;
- automated feedback based on previous interactions;
- teacher or administrator interfaces;
- deployment to cloud infrastructure.

These capabilities are considered extensions and are not required to validate the core project hypothesis.