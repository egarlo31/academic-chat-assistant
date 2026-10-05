# Problem Definition

## 1. Background

Programming students frequently encounter compiler errors, runtime errors, incorrect program behavior, and conceptual difficulties while learning how to design and implement software.

Although documentation, forums, search engines, and generative AI tools can provide technical assistance, the information obtained from these sources is not always adapted to the student's level of understanding or to an educational context. In many cases, existing tools focus primarily on producing a working solution rather than helping the student understand the cause of the problem and the reasoning required to solve it.

Large Language Models (LLMs) provide an opportunity to build interactive systems capable of explaining programming concepts, analyzing source code, identifying possible errors, and generating contextualized guidance through natural language.

However, the usefulness of these systems in an academic environment depends not only on whether they can generate technically plausible answers, but also on whether their explanations are correct, understandable, relevant, and appropriate for supporting the learning process.

## 2. Problem Statement

Students learning programming may have difficulty identifying the causes of errors in their code, understanding programming concepts, and interpreting compiler or runtime messages.

Traditional resources often require students to independently search, filter, and adapt information to their specific problem. General-purpose AI assistants can reduce this effort, but their responses may contain incorrect explanations, unnecessary complexity, or complete solutions that provide limited educational value.

There is therefore a need for an academic programming assistant that can provide contextualized support while prioritizing explanation and understanding instead of only producing final answers.

## 3. Target Users

The primary users of the system are students who are learning programming and require support with introductory or intermediate programming tasks.

The initial version of the system will focus on students working with:

- C;
- C++;
- Python.

The system is intended to support users who may understand basic programming syntax but still require assistance identifying errors, understanding concepts, or reasoning about program behavior.

## 4. Current Limitations

Current programming support methods present several limitations:

- documentation may be technically accurate but difficult for beginners to interpret;
- search engines require users to identify appropriate terminology before finding useful information;
- forum answers may address problems that are similar but not identical to the student's case;
- general-purpose LLMs may generate plausible but incorrect technical explanations;
- AI-generated answers may provide complete code without explaining the underlying reasoning;
- the quality and educational usefulness of generated responses are not always systematically evaluated.

These limitations can reduce the usefulness of existing tools as learning support systems.

## 5. Proposed Approach

The project proposes the development of an LLM-based academic programming assistant capable of receiving programming-related questions and generating contextualized educational responses.

The assistant will focus on tasks such as:

- explaining programming concepts;
- analyzing source code provided by the user;
- identifying and explaining possible errors;
- interpreting compiler or runtime error messages;
- explaining program behavior;
- suggesting corrections or improvements;
- generating small examples when they support understanding.

The system will use a modular architecture so that the language model used by the application can be changed without requiring major modifications to the rest of the system.

This will allow the project to support both externally hosted LLM APIs and locally executed open-weight models.

## 6. Project Objective

The objective of the project is to design, implement, and evaluate an academic programming assistant based on Large Language Models that provides technically correct, understandable, and contextually relevant support to students learning C, C++, and Python.

The system should prioritize educational guidance and explanation while maintaining sufficient modularity to allow experimentation with different language models and future extensions.

## 7. Success Criteria

The project will be considered successful if the Minimum Viable Product is capable of:

- receiving programming-related questions through a user interface;
- processing questions related to C, C++, and Python;
- generating coherent and relevant responses using an LLM;
- explaining programming concepts and errors instead of only returning final solutions;
- maintaining the necessary conversational context during an interaction;
- allowing the underlying LLM provider to be replaced through a common interface;
- operating end-to-end through the frontend, backend, and LLM integration layers;
- being evaluated using predefined programming tasks and evaluation criteria.

The quality of the assistant will be evaluated primarily in terms of technical correctness, explanation correctness, clarity, relevance, and educational usefulness.