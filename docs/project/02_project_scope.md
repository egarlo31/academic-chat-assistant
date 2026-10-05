# Project Scope

## 1. Project Goal

The goal of the project is to develop a Minimum Viable Product of an academic programming assistant based on Large Language Models.

The system will provide educational support for students working with C, C++, and Python by analyzing questions, source code, and error messages and generating contextualized explanations and guidance.

The initial version will prioritize a complete and evaluable end-to-end workflow rather than a large number of advanced features.

## 2. MVP Scope

The Minimum Viable Product will implement the minimum functionality required to validate whether an LLM-based assistant can provide useful programming support in an academic context.

The MVP will include:

1. a web-based user interface;
2. a backend API;
3. an abstraction layer for LLM interaction;
4. support for programming-related user queries;
5. conversational context during an active interaction;
6. support for C, C++, and Python;
7. an initial evaluation workflow using predefined tasks and criteria.

## 2.1 In Scope

The following capabilities are included in the MVP.

### User Interaction

- submission of programming-related questions;
- submission of source code as part of a user query;
- submission of compiler or runtime error messages;
- display of generated responses;
- maintenance of relevant conversational context during an active session.

### Programming Support

The assistant may provide support for:

- programming concept explanations;
- code explanation;
- compiler error interpretation;
- runtime error interpretation;
- basic debugging guidance;
- identification of possible logical errors;
- suggestions for code correction;
- generation of small code examples;
- explanation of program behavior.

### Programming Languages

The MVP will support:

- C;
- C++;
- Python.

Support for additional programming languages is not required for the initial version.

### Backend

The backend will:

- expose the required API endpoints;
- validate incoming requests;
- coordinate interaction with the LLM layer;
- construct the information required for model inference;
- return structured responses to the frontend;
- isolate application logic from the specific LLM provider.

### LLM Integration

The system will provide a common interface for interacting with Large Language
Models.

The architecture shall support two inference strategies:

- locally executed LLMs;
- externally hosted LLMs accessed through an API.

The MVP is not required to implement multiple providers simultaneously.
The initial provider or execution strategy will be selected according to
available computational resources, model quality, cost, and implementation
complexity.

### Evaluation

The project will include an initial evaluation process using predefined programming tasks.

Evaluation will consider dimensions such as:

- technical correctness;
- explanation correctness;
- clarity;
- relevance;
- educational usefulness;
- correctness of generated or corrected code when applicable.

## 2.2 Out of Scope

The following capabilities are explicitly excluded from the MVP.

### Advanced AI Capabilities

- model fine-tuning;
- reinforcement learning;
- training a Large Language Model from scratch;
- multi-agent systems;
- autonomous agents;
- unrestricted tool use;
- autonomous code execution;
- autonomous modification of user files.

### Retrieval Systems

A complete Retrieval-Augmented Generation system is not required for the MVP.

Possible future capabilities such as:

- retrieval from programming documentation;
- vector databases;
- document ingestion pipelines;
- semantic search;

may be explored after the initial system has been implemented and evaluated.

### Execution Infrastructure

The MVP will not initially require:

- distributed inference;
- GPU clusters;
- Kubernetes;
- complex container orchestration;
- production-scale cloud infrastructure;
- load balancing;
- high-availability infrastructure;
- large-scale observability systems.

### Educational Platform Features

The MVP will not include:

- course management;
- assignment management;
- automated grading;
- student progress tracking;
- teacher dashboards;
- institutional authentication;
- learning management system integration.

### IDE Integration

The MVP will operate as an independent web application.

Integration with development environments such as:

- Visual Studio Code;
- JetBrains IDEs;
- Jupyter;
- other code editors;

is considered future work.

## 3. MVP Workflow

The expected MVP workflow is:

1. the user submits a programming-related question through the frontend;
2. the frontend sends the request to the backend API;
3. the backend validates the request and prepares the required context;
4. the LLM integration layer constructs the model request;
5. the configured language model generates a response;
6. the backend receives and processes the generated output;
7. the response is returned to the frontend;
8. the frontend displays the result to the user;
9. when applicable, the interaction is later evaluated using the project evaluation criteria.

The simplified workflow is:

```text
Student
   ↓
Frontend
   ↓
Backend API
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

## 4. Assumptions

The project is based on the following assumptions:

- users have basic familiarity with programming concepts;
- users provide sufficient context when requesting debugging assistance;
- the selected LLM is capable of processing programming-related prompts;
- generated responses may contain errors and therefore require systematic evaluation;
- the application is primarily intended for experimentation and academic evaluation rather than production deployment;
- the MVP can operate using either a local model or an external API;
- the system does not need to support a large number of concurrent users during the initial evaluation.

## 5. Constraints

The project is subject to the following constraints:

### Time

The implementation should remain small enough to be completed and evaluated within the available academic development period.

### Computational Resources

Local models must be compatible with the hardware available to the development team.

The project should avoid requiring specialized infrastructure that is not necessary for the MVP.

### Model Limitations

The quality of generated responses depends on the selected LLM.

The system cannot guarantee that every generated response is technically correct.

### Scope Control

Features that do not directly contribute to the core academic assistant workflow or its evaluation should not be added to the MVP unless they become necessary to satisfy a defined requirement.

## 6. Future Work

The following capabilities may be considered after completion and evaluation of the MVP:

- Retrieval-Augmented Generation using programming documentation;
- integration with official language or library documentation;
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