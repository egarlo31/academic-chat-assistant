# Architecture

## 1. Purpose

This document describes the initial architecture of the Academic Chat Assistant.

The architecture defines the main system components, their responsibilities, and the general interaction flow between the user interface, backend, LLM integration layer, and language model.

The architecture is intentionally kept simple for the MVP and may evolve as technical decisions are validated by the development team.

---

## 2. Architectural Style

The system will follow a **modular layered architecture**.

For the MVP, the project should remain a **modular monolith** rather than being divided into multiple microservices.

The main objective is to separate responsibilities without introducing unnecessary deployment or communication complexity.

The architecture will be divided into the following logical layers:

1. Presentation Layer
2. Application Layer
3. LLM Integration Layer
4. Model Inference Layer
5. Evaluation Layer

$$$ [ DIAGRAMA DE ARQUITECTURA GENERAL QUE MUESTRE LAS CAPAS PRINCIPALES DEL SISTEMA Y SU RELACIÓN ] $$$

---

## 3. Main Components

### 3.1 User Interface

The User Interface will allow students to interact with the system.

Its responsibilities include:

- receiving programming-related questions;
- receiving source code and error messages;
- displaying generated responses;
- supporting conversational interaction;
- communicating with the backend.

The User Interface must not contain model-specific logic.

---

### 3.2 Application Backend

The Application Backend will coordinate the main application workflow.

Its responsibilities include:

- receiving requests from the User Interface;
- validating user input;
- managing application-level logic;
- preparing the required context;
- invoking the LLM Integration Layer;
- processing generated responses;
- handling application errors;
- returning structured responses to the frontend.

The backend should remain independent from the specific model provider.

---

### 3.3 LLM Integration Layer

The LLM Integration Layer will act as the interface between the application and the selected language model.

Its responsibilities include:

- receiving normalized requests from the backend;
- preparing model-specific input;
- managing prompts and instructions;
- invoking the selected LLM;
- normalizing generated responses;
- handling model or provider errors.

The system should support either:

- a locally executed language model; or
- an external language model accessed through an API.

The rest of the application should interact with both alternatives through a common interface.

$$$ [ DIAGRAMA DE ABSTRACCIÓN DEL LLM QUE MUESTRE BACKEND → INTERFAZ LLM → MODELO LOCAL O API EXTERNA ] $$$

---

### 3.4 Model Inference

The Model Inference component represents the actual execution of the Large Language Model.

The specific inference strategy is still pending.

Possible alternatives include:

- local inference using an open-weight model;
- inference through an external API.

The final strategy will depend on factors such as:

- model quality;
- available hardware;
- cost;
- latency;
- implementation complexity.

---

### 3.5 Evaluation Component

The Evaluation Component will be used to measure the behavior and quality of the assistant.

Its responsibilities may include:

- loading predefined evaluation tasks;
- executing tasks through the same LLM workflow used by the application;
- recording generated responses;
- storing evaluation results;
- comparing results using predefined criteria.

The evaluation component should remain logically separated from normal user interaction.

---

## 4. General Interaction Flow

The expected interaction flow is:

1. the student submits a programming-related request;
2. the User Interface sends the request to the backend;
3. the backend validates and prepares the request;
4. the LLM Integration Layer prepares the model input;
5. the configured language model generates a response;
6. the response is returned to the backend;
7. the backend processes the result;
8. the User Interface displays the response to the student.

$$$ [ DIAGRAMA DE FLUJO DE SOLICITUD Y RESPUESTA QUE MUESTRE EL RECORRIDO DE LOS DATOS ENTRE USUARIO, FRONTEND, BACKEND Y LLM ] $$$

---

## 5. Conversation Context

The system should preserve the minimum conversational context required to support follow-up questions during an active interaction.

The exact context management strategy is not yet defined.

Possible alternatives include:

- context managed by the frontend;
- context managed temporarily by the backend;
- persistent context storage.

Permanent conversation storage is not required unless it becomes necessary for the MVP.

---

## 6. Containerization

The project is expected to use containers to provide a reproducible execution environment.

Possible containerized components include:

- frontend;
- backend;
- local model runtime;
- database, if persistence becomes necessary.

The final container structure will depend on the selected technologies and deployment strategy.

Containerization should not imply a microservice architecture.

$$$ [ DIAGRAMA DE DESPLIEGUE EN CONTENEDORES QUE MUESTRE LOS COMPONENTES CONTAINERIZADOS; ESTE DIAGRAMA SE COMPLETARÁ CUANDO SE DEFINA LA ESTRATEGIA DE DESPLIEGUE ] $$$

---

## 7. Data Storage

Persistent storage is not currently considered mandatory.

A database should only be introduced if a concrete requirement requires persistent data such as:

- conversation history;
- user information;
- evaluation results;
- experiment metadata.

Simple structured files may be sufficient for early evaluation data.

---

## 8. Architectural Principles

The implementation should follow these principles:

- separation of concerns;
- low coupling between components;
- provider-independent LLM integration;
- configuration separated from source code;
- clear component responsibilities;
- incremental development;
- avoidance of unnecessary infrastructure;
- architecture driven by actual MVP requirements.

---

## 9. Open Decisions

The following decisions remain pending:

- local LLM or external API;
- initial model selection;
- frontend technology;
- backend technology;
- conversation context strategy;
- persistence requirements;
- containerization strategy;
- evaluation result storage.

These decisions will be recorded in `02_architecture_decisions.md`.