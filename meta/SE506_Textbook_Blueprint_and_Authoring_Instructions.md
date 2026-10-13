# OO Development and Agile Practices

## Textbook blueprint and chapter authoring instructions

Version 0.4 • 13 October 2026 • Prepared for Polla Fattah (module leader)

Confirmed authoring decisions: Java is the primary programming language, and the Campus Equipment Lending System is the running project. Both choices were confirmed by the module leader on 11 October 2026.

This document defines the proposed student textbook before chapter drafting begins. It specifies the book’s purpose, chapter sequence, learning progression, running example, exercises, AI integration, and instructions for writing and reviewing every chapter. It is an authoring baseline for review, not an approved module descriptor or a completed manuscript.

The book follows the supplied SE506 weekly schedule. The module descriptor remains under the module leader’s control. Credit values, contact hours, assessment weights, and university policy are outside this document’s scope. The earlier philosophical book, *The Intentional Codebase*, is a separate project and does not determine this textbook’s structure.

## Version 0.4 changes

Version 0.4 keeps the v0.3 ground rules below unchanged except where noted, and records the changes made after the alignment review of Chapters 1–10 (*SE506_Blueprint_Alignment_Review_and_Chapter_Change_Plan.md*, 13 October 2026). Chapter files refer to the ground rules as “Blueprint v0.3”; those references remain correct.

- **Distinct revision.** The earlier and the revised blueprint both carried the label 0.3. The revised one is now 0.4.
- **Review boundary (G13).** The existing drafts are Chapters 1–10, not 1–9. Chapters 1–10 have now been revised against v0.3 and the alignment review (Chapter 10 on 13 October 2026), so drafting of Chapter 11 may start. The remaining chapters are drafted one at a time, in order, and each is reviewed before the next begins (section 8).
- **Route vocabulary (G10).** Each chapter opens with three entries, named **Core reading**, **Minimum required lab** and **Optional extension**. The earlier “core route” and “lab route” mixed required and optional work and are retired. Chapters 1–9 now use the new entries.
- **Companion listings (decided 13 October 2026).** A companion may list only the files that are new or changed and must name the exact revision of the preceding companion that is its input, so that older listings are not copied again and cannot go stale. The reader assembles the checkpoint from the companions in order. Chapters 1–10 keep their complete listings; Chapter 11 onwards use this form.
- **Two-file rule.** Every chapter is exactly two Markdown files: the student manuscript and a *Code, Explanations and Solutions* companion. Lab sheets, instructor notes, checkpoint listings and verification records are sections of those two files, not separate files.
- **Supporting references must not block a lab.** A mandatory activity must be completable from the chapter pair alone. Appendices A, B and E and Chapter 15 sections are described as planned further reading until they exist, and a missing appendix is never the only place that names a tool or a command a lab needs.
- **Decision status.** Section 9 now records the status of every open decision. Nothing is marked closed because a companion contains a feasibility note.

## Version 0.3 ground rules

Version 0.3 incorporates a cross-check against the module descriptor, *SE506_OO_Development_and_Agile_Practices.docx* (version July 2026). The rules below apply to every chapter. Chapters 1–9 were drafted before this version and must be reviewed against it (section 8). Where a rule conflicts with an older statement elsewhere in this document, the rule wins. Items the descriptor does not settle are listed as open decisions in section 9, not decided here.

| ID | Rule | Applied in |
|---|---|---|
| G1 | **Descriptor-required activities are mandatory.** Any lab or topic named in the descriptor’s delivery plan must be supported, even if an earlier draft called it optional. Depth may stay shallow; omission is not allowed. Required items: issue-board setup (Week 1), capacity planning (Week 3), static-analysis smell lab (Week 4), DI container lab (Week 5), mocking-framework lab (Week 6), repository-metrics lab (Week 11), contracts and feature flags (Week 12). | 2, 4, 5, 6, 7, 12, 13 |
| G2 | **Label every practical activity as *Book project* or *Team project*.** Book-project work uses the Campus Equipment Lending checkpoints. Team-project work applies the same skill to the team’s own system. Every chapter includes a short transfer note for teams not using the lending domain. | Section 4; all chapters |
| G3 | **Team domains come from the provided starter domains.** The descriptor names equipment lending and an ML model-serving tool as examples. The book is built on lending; teams on another domain use the transfer notes. Whether the book also supplies a second starter checkpoint is open (D6). | Sections 3, 4 |
| G4 | **Keep two AI threads separate and balanced.** (a) AI-assisted development: Chapter 15 plus short bounded activities. (b) Software around AI and data components, which is the descriptor’s stated aim: a light, consistent thread in the running project, not optional-only. An AI-assistant activity may be shortened or made optional where it would be padding; record that decision in the chapter’s verification record. | Sections 1, 3, 7 |
| G5 | **UML covers what the midterm assesses.** The midterm gives 20% to modelling a scenario with class diagrams. Chapter 2 and Appendix A must therefore cover classes, attributes, operations, associations, multiplicity, aggregation/composition, inheritance and interface realisation. Teach the method as well as the symbols: how to read a box and a line, how to choose a relationship, how to go from code to diagram and from a scenario to a diagram, how to check a diagram against code, and common errors. Include a worked scenario-to-diagram example, a read-and-check exercise, a spot-the-errors exercise and at least one scenario-modelling exercise. Class diagrams only in Chapter 2; sequence, state and component notation is introduced where first used. | 2.6, Appendix A |
| G6 | **Plan for milestone timing.** Milestone 2 (TDD MVP) is due in the week TDD is taught, and Milestone 3 (architecture) in the week architecture is taught. Mitigate by (a) exposing students to Arrange–Act–Assert in Chapter 4 through the starter test, (b) keeping Chapter 7 and Chapter 10 cores short and early, and (c) making their milestone checklists usable before the chapter is finished. | 4, 7, 10 |
| G7 | **Contribution evidence.** The descriptor assesses individual contribution through commits, PR reviews and peer evaluation. The book presents these as evidence inputs, explains what each can and cannot show, and never ranks people by counts. | 14, Appendix E |
| G8 | **Package design belongs in Chapter 10.** Week 9’s required reading is Martin on package design. Package cohesion, coupling and stability are taught under dependency direction, not left to an optional Chapter 12 aside. | 10.4, 12.6 |
| G9 | **Source pool follows the descriptor.** Beyond the six works in section 7, the pool includes Evans (Week 9), Forsgren, Humble and Kim (Week 11), Humble and Farley (Week 12), and Fowler’s smells material (Week 4). Each chapter notes which weekly Martin reading it supports. | Section 7 |
| G10 | **Design for the stated workload.** Self-study is about 7.5 hours a week. Each chapter provides **Core reading**, a **Minimum required lab** and an **Optional extension** (v0.4 vocabulary), so a student can complete the essentials alongside team-project work. Required work is never placed under “optional”, and optional depth is never required to produce the lab's evidence. The book still allocates no official contact hours. | Section 4 |
| G11 | **Label constructed AI output.** Sample AI output supplied for offline use is marked either *constructed to illustrate* or *captured* with tool, model and date. It is never presented as real output when it was written by hand. | Section 7 |
| G12 | **Tiered authoring packet.** Every chapter requires a manuscript, starting and completed checkpoints, a lab sheet, an instructor guide, offline AI sample output and a verification record. Broken examples, diagrams and source notes are produced where the chapter’s teaching needs them. | Section 4 |
| G13 | **Review existing drafts.** Drafted chapters are checked against the current ground rules and revised or annotated with deviations before the next chapter is drafted. As of v0.4 the boundary is Chapters 1–10. | Section 8 |

## 1 Book purpose and boundaries

**Working title:** *OO Development and Agile Practices*  
**Working subtitle:** *Designing, Testing and Evolving Software with AI Assistance*

The textbook should help postgraduate students move from writing classes to designing, testing, reviewing, and changing maintainable software within a team. Its central teaching unit is a software change: understand the requested behaviour, choose a design, implement and test it, inspect the result, and use feedback to plan the next change.

The intended audience is the SE506 MSc in Artificial Intelligence cohort. For textbook planning, assume basic programming familiarity, including functions, collections, classes, exceptions, and simple debugging. These are pedagogical assumptions, not newly imposed formal module prerequisites. Include a short diagnostic and a catch-up appendix for students whose experience is mainly notebooks or procedural scripts.

By the end, a reader should be able to justify a modest OO design, implement it with useful tests, participate in an iterative team workflow, and demonstrate how that design responds to changed requirements. AI assistance supports those activities. The book must remain usable without a paid AI service.

The descriptor’s aim is to prepare AI students to engineer reliable, extensible software *around* AI and data components. The book therefore treats two ideas separately: using AI to help build software (Chapter 15 and short activities) and building software that depends on AI or data components (a thread in the running project; see section 3). Neither replaces the other (G4).

### Scope decisions

| Area | Treatment |
|---|---|
| OO responsibilities, contracts, cohesion, coupling and SOLID | Central; explain, apply and critique |
| TDD, test doubles, regression protection and refactoring | Central; demonstrated through executable changes |
| Agile planning, feedback and team workflows | Central; connected to actual project evidence |
| Named patterns in the descriptor | All covered; depth varies explicitly |
| Application architecture and DDD vocabulary | Modest layered application; selected modelling concepts |
| AI-assisted development | Short integrated activities plus a reusable reference chapter (G4) |
| Software around AI/data components | Light, consistent thread in the running project: a model or scoring dependency behind a contract, its failure handling, and a test double (G4) |
| Language syntax and tool commands | Brief support material and appendices |
| Model training, RAG, agent frameworks and LLM application development | Outside scope |
| Distributed systems, microservices and cloud infrastructure | Outside scope except brief context where essential |
| Exhaustive GoF coverage or Agile certification preparation | Outside scope |

### Depth vocabulary

- **Core:** students explain, implement, test and justify the concept in a small realistic case.
- **Working knowledge:** students trace a worked example and adapt it with guidance.
- **Awareness:** students recognise the purpose, limits and situations requiring further study.

Depth labels guide reading and exercises. They do not silently alter the module’s assessment requirements. Each substantial chapter should normally have three to five core ideas; supporting terminology should not become a second syllabus.

## 2 Alignment with the supplied module

The six outcome labels below are shortened traceability labels drawn from the supplied descriptor. They do not replace its wording.

| Label | Existing module outcome focus |
|---|---|
| LO1 | Apply OO principles and SOLID to maintainable design |
| LO2 | Select patterns and architectural styles and justify trade-offs |
| LO3 | Apply TDD and automated testing, including doubles and integration tests |
| LO4 | Recognise smells and refactor legacy code safely |
| LO5 | Plan and deliver iteratively using Agile practices and metrics |
| LO6 | Use professional workflows and critically reflect on decisions |

### Chapter and week map

| Chapter | Title | Module timing | Main alignment | Evidence or assessment connection |
|---|---|---|---|---|
| 1 | Developing Software That Can Change | Orientation; no additional week | Introduces LO1–LO6 | Readiness diagnostic and book navigation |
| 2 | Object-Oriented Development Beyond Syntax | Week 1 | LO1, LO6 | Starter inspection, team formation, domain choice, first reviewed change |
| 3 | Agile Development and the Nature of Change | Week 2 | LO5 | Draft backlog, stories, acceptance criteria and Definition of Done |
| 4 | From Requirements to an Iteration | Week 3 | LO5, LO6 | Milestone 1: Sprint 0 artefacts and repository with CI |
| 5 | Responsibilities, Extension and Substitutability | Week 4 | LO1, LO4 | SOLID I and formative smell analysis |
| 6 | Interfaces, Dependencies and Composition | Week 5 | LO1, LO4 | SOLID II; Quiz 1 preparation refers to Weeks 1–4 |
| 7 | Testing as a Design Practice | Week 6 | LO3 | Milestone 2: MVP, TDD, SOLID, demo and retrospective |
| 8 | Creating and Connecting Objects | Week 7 | LO2 | Pattern practice; midterm assesses Weeks 1–6 |
| 9 | Designing Changing Behaviour | Week 8 | LO2, LO4 | Behavioural patterns; critical book review due |
| 10 | From Classes to Application Structure | Week 9 | LO2, LO6 | Milestone 3: patterns, architecture, demo and retrospective |
| 11 | Refactoring and Legacy Code | Week 10 | LO3, LO4 | Legacy-code lab; Quiz 2 preparation refers to Weeks 5–9 |
| 12 | Measuring Progress, Flow and Technical Health | Week 11 | LO5, LO6 | Requirement change introduced; impact and response planning |
| 13 | Integration, Delivery and Feedback | Week 12 | LO3, LO6 | Milestone 4: change implemented, integration tests and CI/CD |
| 14 | Responding to Change and Handing Over | Week 13 | LO1–LO6 | Final-sprint workshop, documentation and retrospective |
| 15 | AI as a Software Engineering Assistant | Reference used throughout | Supports especially LO3, LO4, LO6 | AI review and verification record; no separate teaching week |

Week 14 remains independent review and project work. Weeks 15–16 remain the final project demonstration and submission period. The book supplies preparation material, not extra scheduled teaching.

The source also includes an individual critical book review due in Week 8. Introduce its reading method in Chapter 1 and Appendix E so students can begin early. Use the module leader’s approved reading list; do not imply that reading this textbook automatically satisfies that assessment.

### Sequence safeguards

1. Chapter 4 needs a minimal CI check before the formal testing chapter. Supply a working starter test and explain how to run it; defer TDD and test-double theory to Chapter 7.
2. Chapters 5–6 need safe small changes before the legacy-code chapter. Supply regression checks and show elementary refactoring steps, then defer systematic legacy-code work to Chapter 11.
3. Chapter 8 coincides with the midterm. Make its classroom route selective; all named patterns remain available as structured readings and exercises.
4. Chapter 12 introduces the assessed requirement change in Week 11. Chapter 13 implements and verifies it by Week 12. Chapter 14 evaluates and hands over the result; it does not introduce the change for the first time.
5. Chapter 15 is available from the start. Students read its relevant sections before each AI activity rather than waiting until the end of the semester. It keeps its number and is labelled a companion reference to be read alongside Chapter 1; do not renumber.
6. Milestone 2 falls in the week TDD is taught, and Milestone 3 in the week architecture is taught (G6). Chapter 4 gives students their first Arrange–Act–Assert exposure through the starter test. Chapters 7 and 10 each open with the three route entries and a milestone checklist usable before the chapter is finished.
7. The Week 4 static-analysis lab and Week 11 repository-metrics lab are required (G1). Chapter 5 and Chapter 12 each include the lab or an explicit pointer to it.

## 3 Running example design

### Confirmed running project

Use the confirmed **Campus Equipment Lending System** as the book’s running example. Keep it narrower than a general campus resource-management platform. The descriptor has teams build one system from a *provided starter domain* (it names equipment lending and an ML model-serving tool as examples) on a provided starter codebase with intentional smells. The lending starter is the book’s version of that codebase. Teams on another provided domain follow each chapter’s transfer note (G2, G3). Every practical activity states whether it runs on the **Book project** or the **Team project**.

The system allows a borrower to inspect equipment availability, request a reservation, borrow an approved item, and return it. Later requirements introduce borrowing policies, notifications, an external directory, and approval rules. Use synthetic records throughout.

Start with one item per reservation and explicit loan periods. Explain the initial assumptions rather than attempting a production inventory system. Begin with an in-memory store and a simple command-line or thin demonstration interface. Introduce durable storage only when an integration boundary needs to be taught. Do not let UI development or database configuration displace OO design.

Initial domain vocabulary: **Borrower, EquipmentItem, Reservation, Loan, LoanPeriod**. Candidate collaborators may later include **BorrowingPolicy, NotificationSender, BorrowerDirectory** and a storage interface. Introduce each abstraction only when the example develops a reason for it; these names are not an instruction to build all interfaces in advance.

**AI/data component thread (G4):** introduce one small AI or data-backed collaborator once the example needs it, for instance an estimator that scores return risk and sits behind a contract that the domain depends on. Use it to teach substitution, test doubles, timeouts, fallbacks and validation of results. Keep the model itself trivial and synthetic; model training and inference engineering are out of scope. The concrete choice was made on 13 October 2026 (D7): the data-component route. The book's collaborator is the borrower directory of Chapter 8, previewed as a contract in Chapter 6, substituted with doubles in Chapter 7, built in Chapter 8, placed in the application structure in Chapter 10 and given timeouts and a fallback-or-failure policy in Chapter 13. No model component is added; a model-serving team applies the same questions to its own model runtime.

Initial invariants include valid loan periods, no conflicting confirmed reservation for the same item and period, and no return of an inactive loan. Define the period-boundary convention explicitly when coding begins. A later storage exercise should discuss the limits of an in-memory availability check under concurrent requests without expanding into a distributed-systems chapter.

### Evolution and checkpoints

| Stage | Chapters | Change or activity | Expected state |
|---|---|---|---|
| Orientation | 1–2 | Run a deliberately imperfect but functioning starter | Understand behaviour and identify design pressure |
| Backlog and kickoff | 3–4 | Define reservation stories and delivery workflow | Milestone 1: vision, backlog, wireframes, repository and CI |
| MVP | 5–7 | Separate responsibilities, add borrower-policy variation, test core behaviour | Milestone 2: small working reservation and loan flow |
| Extension | 8–10 | Add an external directory adapter and notification behaviour; organise layers | Milestone 3: justified patterns and application structure |
| Recovery | 11 | Repair a supplied legacy overdue-reporting component | Characterisation tests and a documented refactoring sequence |
| Changed requirement | 12–13 | Introduce a new approval/policy rule; implement and verify it | Milestone 4: changed behaviour, regression protection and delivery evidence |
| Handover | 14 | Review residual defects, document use and decisions, rehearse demo | Reproducible final submission and individual reflection |

Suggested worked change: visiting researchers may borrow selected equipment only after sponsor approval and under a shorter loan limit. Keep the rules precise and small; avoid adding payments, deposits and financial workflows at the same time.

The textbook may disclose this worked change because it is teaching material. Provide a separate instructor-only change bank for assessment, such as maintenance lockouts, extended loan permissions or restricted equipment categories. Release the assessed variant in Week 11 so it tests adaptation rather than advance copying of the worked answer.

Not every pattern belongs in the final system. Use isolated micro-examples for patterns whose inclusion would complicate it. Every chapter should state whether an example becomes part of the cumulative codebase or remains a separate teaching branch.

### Language and toolchain decision

**Java is the confirmed primary implementation language.** Use Java consistently for the cumulative project, runnable examples, tests and worked solutions. Explain transferable design principles while grounding language-specific behaviour in Java’s actual semantics. Do not alternate implementation languages between chapters.

The proposed supporting toolchain is JUnit for tests and Maven for builds. Begin with plain Java, manual constructor injection, in-memory storage and a simple command-line interface. Introduce persistence or an external-service integration when the chapter requires it. Keep frameworks and advanced language features subordinate to the learning outcomes; avoid unnecessary interfaces and class hierarchies.

The descriptor requires four further tool categories, so the toolchain must also name (G1):

- the **educational DI container** written for the book, used for the Week 5 lab as a short walkthrough after manual wiring (D3, closed; no library container is pinned);
- a **mocking framework** for the Week 6 lab, introduced after hand-written doubles (D4);
- a **static-analysis tool** for the Week 4 smell lab (D5);
- a **repository-metrics method**, such as `git log` scripts or a repository-analysis tool, for the Week 11 lab.

The Week 1 “modern OOP refresh” implies current Java idioms such as records, lambdas and sealed types. Decide which are allowed before drafting executable chapters, and cover them briefly in Appendix A (D2). Decide the integration boundary used in Chapters 8 and 13, such as a local HTTP stub, a file-backed store or an embedded database, together with the toolchain (D1). Pin every version before the tool appears in a chapter.

Chapter 1 can now proceed with both language and domain settled. Before drafting Chapter 2’s runnable examples, verify and pin a compatible supported JDK, test-framework version and build configuration, then establish the starter project and reproducible commands. Exact tool versions remain implementation details to resolve during setup.

## 4 Standard chapter design

### Student-facing structure

1. **Opening problem:** one concrete behaviour, change request or team difficulty.
2. **Learning outcomes:** four to six observable capabilities using verbs such as explain, diagnose, implement, compare, test and justify.
3. **Prerequisites and reading route:** what the reader already needs; identify core and optional sections.
4. **Concepts through a worked example:** introduce terminology when it becomes useful.
5. **Engineering decision:** compare a simple approach with one or two alternatives; explain costs and consequences.
6. **Running-project application:** identify the starting checkpoint, change, and resulting checkpoint.
7. **AI in practice:** a bounded candidate output that the student must inspect and verify.
8. **Common mistakes:** misconceptions demonstrated with a small counterexample.
9. **Practical activity:** task, supplied materials, expected artefacts and completion checks.
10. **Review and transfer:** conceptual questions, a code or artefact critique, and a new scenario.
11. **Summary and sources:** concise conclusions, next-chapter connection and verified reading references.

Use this structure flexibly. Process chapters should compare backlogs, plans or metrics rather than force artificial before-and-after code. The introductory chapter can use a diagnostic instead of a full lab. Chapter 15 is a reference workflow rather than another project milestone.

### Chapter authoring packet

Every chapter requires: manuscript; starting and completed checkpoints; a lab sheet; a solution or instructor guide; sample AI output for offline use (labelled under G11); and a short verification record. Produce the following where the chapter’s teaching needs them: intentionally broken examples, diagrams and source notes (G12). These are future deliverables, not files supplied with this blueprint.

**Core reading, minimum required lab and optional extension (G10):** open each chapter with three short entries. *Core reading* names the sections every student reads. *Minimum required lab* names the tasks that produce every required artefact, labels each as Book project or Team project, and says which book examples students trace or run and which changes they must implement independently on the team project. *Optional extension* lists everything else. A student with about 7.5 hours of weekly self-study should be able to complete the first two alongside team-project work. “Working knowledge” depth means limited required depth, not omission.

**Two files per chapter.** Each chapter is the student manuscript plus one *Code, Explanations and Solutions* companion; lab instructions, instructor notes, checkpoint listings and verification records are sections of those files. Each companion records which revision of the preceding companion is its input, so that an old test is not silently carried forward.

Target a manageable core reading of roughly 3,000–4,500 words for a normal teaching chapter, excluding code, exercises and references. Chapters 1 and 15 may be shorter. Pattern chapters can be longer if they clearly distinguish the core reading and minimum lab from optional depth. These are planning ranges, not word quotas.

### Exercise design

Each teaching chapter should contain approximately four short concept questions, two applied diagnosis questions, one main practical activity, and one transfer challenge. Include a model reasoning path in instructor material; accept alternative designs when their behaviour and trade-offs are justified. Do not grade by number of patterns, interfaces, tests, commits or AI prompts.

The practical activity must state whether it runs on the Book project or the Team project, its input, expected output, acceptance conditions, evidence to submit, and optional extension. Add a transfer note for teams working in another provided domain (G2, G3). Identify instructor demonstration, guided practice and independent work without allocating official contact hours that the programme has not confirmed.

## 5 Chapter specifications

### Chapter 1 Developing Software That Can Change

**Role and entry point:** orientation before or alongside Week 1. No additional teaching week. Assume only basic programming experience.

**Learning outcomes:** explain the difference between functioning code and maintainable software; describe how design, tests and feedback support change; identify the evidence needed to trust a proposed change; navigate the book and diagnose prerequisite gaps.

**Section order:** 1.1 A working program meets a new requirement; 1.2 Behaviour, quality and maintenance; 1.3 The connection between OO development and iterative delivery; 1.4 Testing, review and feedback; 1.5 AI assistance and human judgement; 1.6 The running example and semester route; 1.7 How to study and read critically.

**Worked example and activity:** show a short reservation routine that works for one borrower category but becomes awkward when a second policy appears. Compare the questions an engineer must ask before making the change; do not solve the example with unexplained SOLID or pattern names. The diagnostic asks students to read a class, predict behaviour, identify a boundary case and explain a proposed modification.

**AI activity:** inspect a supplied plausible explanation containing one unsupported assumption. Students point to the code or requirement that confirms or contradicts it. No account or live generation is necessary.

**Exit artefact:** a personal readiness checklist and a short statement of what would count as evidence that the change is safe.

**Author instructions and boundaries:** use practical language rather than a philosophical manifesto. Avoid claims that AI has made programming trivial or that all development is faster with AI. Introduce the critical-reading assignment and point to Appendix E. Preview the book’s concepts without teaching them in full.

### Chapter 2 Object-Oriented Development Beyond Syntax

**Timing and alignment:** Week 1; LO1 and LO6. Entry: Chapter 1 and basic class syntax.

**Learning outcomes:** assign responsibilities to collaborating objects; distinguish encapsulation from merely exposing fields through accessors; diagnose cohesion and coupling problems; compare composition with inheritance; model a small class relationship; make and review a small version-controlled change.

**Section order:** 2.1 Objects, identity, state and behaviour; 2.2 Responsibilities and invariants; 2.3 Encapsulation and information hiding; 2.4 Cohesion, coupling and dependencies; 2.5 Composition and inheritance; 2.6 UML class diagrams: reading, drawing and checking; 2.7 Git history, branches and review.

**Worked example:** inspect the starter’s reservation coordinator, which mixes availability rules, storage and notification formatting. Identify its responsibilities before splitting anything. Draw the relationships needed to explain it and make one small behaviour-preserving improvement using supplied checks.

**AI activity:** compare an AI explanation of the coordinator with actual control flow, state changes and side effects. Record both correct statements and errors.

**Practical activity and exit artefact:** produce an annotated class diagram, a short coupling/cohesion diagnosis and one reviewed commit. Students should be able to explain the diff and run the starter checks. Include team formation and approved-domain selection prompts.

**Descriptor additions (G1, G5):** include issue-board setup in the Git workflow lab. Section 2.6 covers the class-diagram notation the midterm assesses (classes, attributes, operations, associations, multiplicity, aggregation/composition, inheritance, interface realisation) and teaches the method (reading, choosing relationships, code to diagram, scenario to diagram, checking, common errors) with a worked example and three short exercises, since UML class modelling carries 20% of the midterm.

**Author instructions and boundaries:** use UML only where it clarifies the example; do not write a full notation tutorial beyond G5. Explain trunk-based and short feature-branch workflows at introductory depth without claiming a universal winner. Defer a complete SOLID treatment to Chapters 5–6. Git command reference belongs in Appendix B.

### Chapter 3 Agile Development and the Nature of Change

**Timing and alignment:** Week 2; LO5. Entry: the running domain and Chapter 2’s collaboration basics.

**Learning outcomes:** distinguish iterative and incremental delivery; explain Agile values through practical choices; compare Scrum and Kanban; write testable stories and acceptance criteria; apply INVEST; distinguish acceptance criteria from Definition of Done.

**Section order:** 3.1 Uncertainty and feedback; 3.2 Agile values and principles; 3.3 Iteration and increments; 3.4 Scrum’s core accountabilities, events and artefacts; 3.5 Kanban and explicit workflow; 3.6 Epics, stories and INVEST; 3.7 Acceptance criteria and Definition of Done; 3.8 Relative estimation and uncertainty.

**Worked example:** transform “manage equipment” into small user-centred stories, with examples for overlapping reservations, invalid periods and unavailable items. Show that a story template alone does not make a requirement useful.

**AI activity:** ask for missing assumptions and candidate acceptance criteria. Students mark each suggestion accepted, rejected or needing stakeholder clarification, with reasons.

**Practical activity and exit artefact:** draft an ordered backlog, several small stories, a Definition of Done and a simple board. The completion check is whether another team can understand and test the top story.

**Author instructions and boundaries:** distinguish formal Scrum terminology from classroom adaptations and common optional practices. Do not claim Scrum requires user stories or story points. Keep estimation introductory here; Chapter 12 owns measured flow and forecasting. Introduce critical reading through a short comparison of two process recommendations.

### Chapter 4 From Requirements to an Iteration

**Timing and alignment:** Week 3; LO5 and LO6; Milestone 1. Entry: Chapter 3’s draft backlog.

**Learning outcomes:** define a bounded project vision; slice one feature into a deliverable increment; form a capacity-aware iteration plan; set up a reviewed repository workflow; run a minimal CI check; assemble the kickoff evidence.

**Section order:** 4.1 Vision, scope and constraints; 4.2 Domain assumptions and wireframes; 4.3 Prioritisation and vertical slicing; 4.4 Release outlook and iteration planning; 4.5 Team agreements and review workflow; 4.6 Starter build and CI; 4.7 Milestone 1 preparation.

**Worked example:** prepare a thin reservation journey with a lightweight wireframe, acceptance examples, a starter command and a small executable check. Show which work is necessary to demonstrate the story and which work can wait.

**AI activity:** critique an overambitious generated sprint plan. Students remove unsupported tasks and check remaining work against capacity and acceptance criteria.

**Practical activity and exit artefact:** vision, epics and stories, prioritised backlog, wireframes, repository instructions and an observed passing CI run. Include a deliberately failing check to establish that the pipeline detects failure.

**Descriptor additions (G1, G6):** include a capacity-planning exercise (the Week 3 lab). Walk through the starter test in Arrange–Act–Assert terms so Chapter 7 is not the first encounter with test structure.

**Author instructions and boundaries:** retain “Sprint 0” as the descriptor’s kickoff label, while explaining that it is a local preparation convention, not a formal Scrum event. Supply a starter test without requiring prior TDD knowledge. Reserve comprehensive pipeline design for Chapter 13 and keep planning tools interchangeable.

### Chapter 5 Responsibilities, Extension and Substitutability

**Timing and alignment:** Week 4; LO1 and LO4. Entry: Chapters 2–4 and supplied regression checks.

**Learning outcomes:** identify independent reasons for a class to change; apply SRP to a concrete responsibility problem; justify an extension point under OCP; evaluate a subtype against behavioural expectations; perform a small protected refactoring and explain its trade-off.

**Section order:** 5.1 Change pressure in a reservation service; 5.2 Responsibility and SRP; 5.3 OCP and anticipated variation; 5.4 Behavioural contracts; 5.5 LSP and unsafe inheritance; 5.6 Small refactorings and regression checks; 5.7 Avoiding premature abstraction.

**Worked example:** separate loan-rule decisions from message formatting. Introduce a borrower-policy variation only after showing the second rule. Use a small separate subtype example for LSP if the domain example would require contrived inheritance.

**AI activity:** inspect a “make this SOLID” response containing excessive interfaces or altered behaviour. Require students to cite a concrete defect or cost rather than dismiss the design by appearance.

**Practical activity and exit artefact:** a smell diagnosis, a small before-and-after change with regression results, and a short rationale linking each structural change to a requirement or maintenance concern.

**Descriptor addition (G1):** the Week 4 lab uses a static-analysis tool to find smells. Include a short walkthrough of the pinned tool (D5) and have students compare its findings with their own manual diagnosis, noting what it misses and what it reports that does not matter.

**Author instructions and boundaries:** SRP does not mean one method per class. OCP does not forbid editing existing code. LSP concerns client-visible behaviour, not only matching signatures. Introduce any needed interface syntax locally; defer dependency direction and injection to Chapter 6. Save the systematic smell catalogue for Chapter 11.

### Chapter 6 Interfaces, Dependencies and Composition

**Timing and alignment:** Week 5; LO1 and LO4. Entry: Chapter 5’s responsibilities and contracts.

**Learning outcomes:** design an interface around a client’s needs; explain ISP; distinguish DIP from dependency injection and inversion of control; construct a small object graph using constructor injection; assess when an interface adds useful separation.

**Section order:** 6.1 Dependencies that make change difficult; 6.2 Client-specific contracts and ISP; 6.3 Policy and implementation dependencies; 6.4 DIP; 6.5 Constructor injection and composition roots; 6.6 IoC and DI containers; 6.7 Costs of abstraction.

**Worked example:** remove direct notification-provider construction from a reservation service. Place object assembly at the application boundary and show the dependency direction. Manual wiring is the main explanation; a small container walkthrough supports the descriptor’s lab topic.

**AI activity:** critique a generated refactoring that replaces concrete dependencies with interfaces but still mixes provider configuration and business policy. Ask whether dependency direction actually improved.

**Practical activity and exit artefact:** an injected notification contract, two simple implementations, a composition diagram and regression evidence. Explain why each interface exists and who consumes it.

**Descriptor addition (G1):** the Week 5 lab is “refactoring with interfaces and DI containers.” Keep manual wiring as the main explanation and add a short container walkthrough using the adopted educational container (D3, closed 13 October 2026: `DemoContainer`, no library container pinned), showing what it automates and what it hides.

**Author instructions and boundaries:** do not equate DIP with “always use interfaces” or DI with a framework. A hand-written substitute may preview testing, but the full test-double taxonomy belongs in Chapter 7. Include Quiz 1 revision pointers to Chapters 2–5, reflecting its stated Weeks 1–4 coverage rather than adding Week 5 content to the quiz.

### Chapter 7 Testing as a Design Practice

**Timing and alignment:** Week 6; LO3; Milestone 2. Entry: an MVP under development and replaceable collaborators.

**Learning outcomes:** turn acceptance examples into focused tests; demonstrate a complete red–green–refactor cycle; choose an appropriate test double; distinguish behavioural checks from implementation-coupled tests; recognise limitations in a passing test suite.

**Section order:** 7.1 Behaviour and test evidence; 7.2 Test anatomy and Arrange–Act–Assert; 7.3 Red–green–refactor; 7.4 Boundaries and deterministic tests; 7.5 Dummies, stubs, fakes, spies and mocks; 7.6 Testability and design feedback; 7.7 Weak or brittle tests; 7.8 Milestone 2 evidence.

**Worked example:** test borrower limits and conflicting reservations using a controlled clock and in-memory data where appropriate. Include one complete TDD sequence and explain why the initial failure is the intended failure. Introduce a mocking framework after hand-written doubles clarify the roles.

**AI activity:** have AI propose an implementation from human-reviewed acceptance examples, then separately propose omitted edge cases. Students inspect expected values and show that a deliberately incorrect implementation is rejected by at least one relevant test.

**Practical activity and exit artefact:** working MVP behaviour, a traceable TDD example, useful tests, a justified double, and demo/retrospective notes for Milestone 2.

**Descriptor additions (G1, G6):** the Week 6 lab is a mocking-framework lab, so include it after hand-written doubles (D4). Milestone 2 is due this week: open the chapter with the three route entries and a Milestone 2 checklist students can use before finishing the chapter. The midterm (Week 7) asks students to write unit tests with test doubles; state which doubles and framework are permitted there.

**Author instructions and boundaries:** passing tests do not prove correctness; coverage alone does not establish test quality. Avoid using AI-generated tests and implementation as mutual proof. Keep integration and E2E detail for Chapter 13. Supply midterm practice based on Chapters 2–7 only.

### Chapter 8 Creating and Connecting Objects

**Timing and alignment:** Week 7; LO2. Entry: SOLID, composition and unit tests.

**Learning outcomes:** identify a construction or compatibility problem; distinguish Factory Method from a simple factory and Abstract Factory; use Builder when staged construction is justified; adapt an incompatible interface; compose an optional responsibility using Decorator and discuss its costs.

**Section order:** 8.1 Why object creation can become a design problem; 8.2 Factory Method; 8.3 Abstract Factory; 8.4 Builder; 8.5 Adapter; 8.6 Decorator; 8.7 Choosing the simpler alternative.

**Depth:** Adapter and Factory Method at core depth; Builder and Decorator at working knowledge with implementation exercises; Abstract Factory at working knowledge using a compact family-of-products example. All five named patterns remain present. In a week containing the midterm, prioritise two live demonstrations and assign the remaining structured examples as guided reading.

**Worked examples:** use an external borrower-directory Adapter in the cumulative project. Demonstrate true Factory Method separately if a simple construction function is sufficient in the project. Keep Builder and Abstract Factory micro-examples separate unless an actual requirement needs them. A Decorator example should expose order and error-handling consequences.

**AI activity:** inspect a factory-based answer and classify the pattern actually implemented; repair inaccurate naming and unnecessary layers.

**Practical activity and exit artefact:** integrate one justified boundary pattern with tests, then compare two designs for a second scenario. Produce a problem–solution–consequence explanation.

**Author instructions and boundaries:** each pattern follows problem, simple attempt, change pressure, structure, test, trade-off and non-use case. Do not require the semester codebase to contain every pattern. The midterm remains on Weeks 1–6, not this chapter’s new material.

### Chapter 9 Designing Changing Behaviour

**Timing and alignment:** Week 8; LO2 and LO4. Entry: Chapters 7–8.

**Learning outcomes:** distinguish interchangeable algorithms from state-dependent behaviour; select Strategy or State for an explicit problem; explain Observer notification and failure concerns; represent an action with Command; compare a pattern with a simpler conditional implementation.

**Section order:** 9.1 Variation in behaviour; 9.2 Strategy; 9.3 State and transitions; 9.4 Observer and notification; 9.5 Command; 9.6 Testing pattern-based behaviour; 9.7 Pattern selection and limits.

**Depth:** Strategy and State at core depth; Observer and Command at working knowledge with small executable examples.

**Worked examples:** borrowing-rule variation for Strategy and reservation lifecycle transitions for State. Use a notification micro-example for Observer and a request-action example for Command. Keep event ordering, subscriber failure and command side effects visible; do not imply that these patterns automatically solve reliability.

**AI activity:** compare generated Strategy and State proposals for the same scenario. Students choose using requirements and transition behaviour, not the model’s confidence.

**Practical activity and exit artefact:** replace one demonstrably awkward conditional structure, protect its behaviour with tests, and justify either adopting or declining a second pattern.

**Author instructions and boundaries:** patterns are optional solutions, not required decorations. Keep broker infrastructure, distributed event delivery and CQRS outside scope. Remind students of the critical review submission and link to Appendix E; its evidence must come from the selected book and verified sources, not an AI summary of an unread text.

### Chapter 10 From Classes to Application Structure

**Timing and alignment:** Week 9; LO2 and LO6; Milestone 3. Entry: a modest tested application with selected patterns.

**Learning outcomes:** organise responsibilities into application layers; distinguish domain rules from orchestration and infrastructure; explain entity identity and value-object semantics; locate repository and service responsibilities; document a dependency decision and review it in a pull request.

**Section order:** 10.1 Why class-level design is insufficient; 10.2 Layers and separation of concerns; 10.3 Presentation, application, domain and infrastructure; 10.4 Dependency direction; 10.5 Entities and value objects; 10.6 Repositories and services; 10.7 A small architecture decision; 10.8 Peer review and Milestone 3.

**Depth:** layered organisation and dependency direction are core; selected DDD modelling vocabulary is working knowledge; Ports and Adapters is an optional comparison. Define strategic DDD terms only if needed to orient further reading.

**Worked example:** reorganise the reservation use case without changing its external behaviour. Show where storage contracts and implementations live, and distinguish runtime call flow from source-code dependencies. A loan-period value object can make validation explicit.

**AI activity:** ask for a dependency review, then confirm each claimed violation by tracing actual imports or references.

**Practical activity and exit artefact:** a compact component diagram, reviewed restructuring PR, passing checks and an architecture decision note for Milestone 3.

**Descriptor additions (G6, G8):** Week 9’s required reading is Martin on package design. Section 10.4 teaches package cohesion, coupling and stability alongside dependency direction. If instability is quantified, define the quantities and formula correctly and treat the zero-dependency case explicitly. Milestone 3 is due this week: open with the three route entries and a Milestone 3 checklist, and make the layering exercise usable before the chapter is finished.

**Author instructions and boundaries:** explain that architecture also exists in small single-process systems. Do not equate it solely with cloud deployment. Avoid full DDD, microservices and unnecessary generic repository frameworks. A repository is not automatically useful for every class.

### Chapter 11 Refactoring and Legacy Code

**Timing and alignment:** Week 10; LO3 and LO4. Entry: Chapters 5–7 and 10.

**Learning outcomes:** diagnose a smell from concrete change difficulty; distinguish refactoring from behaviour change; establish characterisation tests around poorly understood code; apply small refactorings with checks between steps; document uncertainties and known defects separately.

**Section order:** 11.1 Working with unfamiliar code; 11.2 Smells as investigation prompts; 11.3 Characterisation and regression tests; 11.4 Seams and dependency isolation; 11.5 Extract Method, Extract Class, Move Method and Rename; 11.6 Incremental changes and rollback; 11.7 Technical debt and evidence.

**Worked example:** supply a legacy overdue-reporting routine with duplication, long methods and hidden time dependencies. Preserve an intentionally surprising behaviour in a characterisation test, record whether it is a suspected defect, and separate any correction into a later functional change.

**AI activity:** review a refactoring patch that accidentally changes a boundary condition. Students reproduce the difference and reject or repair the patch using evidence.

**Practical activity and exit artefact:** initial behavioural observations, characterisation tests, a sequence of small commits and a before-and-after rationale. The completed example must distinguish structural improvement from intentional functional correction.

**Author instructions and boundaries:** do not suggest every smell requires immediate repair or that tests establish complete equivalence. Teach risk-based protection and review. Cross-reference Chapter 5 rather than repeat SOLID definitions. Quiz 2 preparation should cover Chapters 6–10, matching Weeks 5–9; keep the new legacy lab separate from its stated scope.

### Chapter 12 Measuring Progress, Flow and Technical Health

**Timing and alignment:** Week 11; LO5 and LO6; assessed requirement change introduced. Entry: a project history and backlog.

**Learning outcomes:** calculate and interpret simple flow measures; distinguish velocity from throughput; explain scope effects in burn charts; use evidence to revise a forecast; evaluate a technical-debt claim; plan the response to a new requirement.

**Section order:** 12.1 What decision needs a measure; 12.2 Estimation revisited; 12.3 Velocity and its limits; 12.4 Burn-down and burn-up; 12.5 Lead time, cycle time, throughput and WIP; 12.6 Technical health and metric misuse; 12.7 Changed requirement and impact analysis.

**Worked example:** use an explicitly synthetic issue history with scope changes and a blocked item. Define start/end events before calculating durations. Explain how equal throughput can conceal different delays. Introduce the worked visiting-researcher requirement and identify affected rules, tests, data and interfaces.

**AI activity:** ask AI to explain the supplied metrics, then check its arithmetic and reject causal explanations unsupported by the data.

**Practical activity and exit artefact:** a small calculations table, cautious interpretation, updated backlog and change-impact note. Preserve the pre-change code checkpoint for comparison with Chapter 13.

**Descriptor addition (G1):** the Week 11 lab is a repository-metrics analysis. In addition to the synthetic issue history, include a short exercise that derives cycle time or throughput from real repository data (git history, PR timestamps or issue exports), using the method pinned in the toolchain. State start and end events before measuring, and discuss what repository data cannot show.

**Author instructions and boundaries:** do not rank people by velocity, commits or lines of code. Present metric gaming and Goodhart’s Law briefly as interpretive cautions. Package instability is taught in Chapter 10 (G8); refer to it here rather than re-teaching it. Avoid a long metrics catalogue or claims of causality from a tiny sample.

### Chapter 13 Integration, Delivery and Feedback

**Timing and alignment:** Week 12; LO3 and LO6; Milestone 4. Entry: Chapter 12’s change specification and plan.

**Learning outcomes:** choose unit, integration and E2E checks for different risks; explain a contract test’s scope; implement the changed behaviour with regression protection; configure and interpret a modest delivery pipeline; distinguish continuous delivery from continuous deployment; evaluate a feature flag and rollback plan.

**Section order:** 13.1 Boundary risks and test scope; 13.2 Integration and contract tests; 13.3 Focused E2E journeys; 13.4 CI stages and quality gates; 13.5 Delivery and deployment; 13.6 Feature flags, configuration and rollback; 13.7 Changed behaviour verification; 13.8 Milestone 4 evidence.

**Worked example:** implement the visiting-researcher approval rule, verify existing borrower behaviour, and test one genuine boundary such as persistent storage or an external-directory adapter against a controlled local test service. Include both old and new paths if a flag is used.

**AI activity:** inspect a proposed integration test that replaces the very boundary it claims to test. Repair the test and explain what it now verifies. A secondary activity may inspect a real pipeline failure summary.

**Practical activity and exit artefact:** changed feature, regression and integration evidence, an observed pipeline run, demo and retrospective. Use a local or controlled staging target; public deployment is not required to understand delivery.

**Decision D7 follow-up (13 October 2026):** the book's data-backed collaborator is the borrower directory of Chapter 8. Chapter 13 must add what a real provider needs and the synthetic fixture lacks: a transport timeout and an explicit fallback-or-failure policy for the directory (an outage must not become “not found”, and must not default a borrower to staff), tested against a controlled local service or a deliberately slow and failing stub. It must also say what boundary it adds (D1).

**Descriptor addition (G1):** contracts and feature flags are named in the Week 12 topic and in the indicative content, so both stay in the chapter. Keep feature flags to a short, working-knowledge treatment: one flag, both paths tested, and a removal plan.

**Author instructions and boundaries:** label simulated deployments as simulations. An E2E test should identify the actual system boundary even for a command-line application. Do not claim green CI establishes security or universal correctness. Keep orchestration platforms and production operations beyond the modest course scope.

### Chapter 14 Responding to Change and Handing Over

**Timing and alignment:** Week 13; integrates LO1–LO6. Entry: Milestone 4 completed or its remaining defects explicitly identified.

**Learning outcomes:** evaluate how the design accommodated change; prioritise remaining release work; produce reproducible handover instructions; trace requirements to implementation and tests; support retrospective conclusions with evidence; explain an individual contribution.

**Section order:** 14.1 Reviewing the change outcome; 14.2 Defects, polish and scope control; 14.3 Documentation and decision records; 14.4 Reproducible setup and demonstration; 14.5 Retrospective and individual reflection; 14.6 Final submission preparation.

**Worked example:** compare the pre-change and post-change project using affected responsibilities, test failures, revised assumptions and review feedback. Explain why a small diff is not automatically a better design and a larger justified change is not automatically failure.

**AI activity:** ask for a draft README or release note, then validate every command, feature claim and limitation against the submitted version.

**Practical activity and exit artefact:** handover bundle containing setup instructions, usage example, known limitations, test instructions, requirements-to-evidence table and demo outline. A different student should be able to follow the setup. Include a team retrospective and a separate individual reflection.

**Author instructions and boundaries:** the requirement change began in Week 11; do not turn this chapter into a late new feature sprint. Link to Week 14 independent review and Weeks 15–16 final submission. The descriptor assesses individual contribution through commits, PR reviews and peer evaluation (G7). Present each as an evidence input, explain what it can and cannot show, and describe contribution qualitatively, without treating commit counts as a fair measure of work.

### Chapter 15 AI as a Software Engineering Assistant

**Role and alignment:** reference chapter used throughout; supports existing outcomes without adding a separate assessed AI outcome. Its short safety and verification introduction is read with Chapter 1.

**Learning outcomes:** provide bounded context for an AI-assisted task; evaluate candidate explanations, code and tests; recognise unsupported APIs and unnecessary abstractions; record useful provenance and verification evidence; complete an equivalent exercise without live AI access.

**Section order:** 15.1 Assistance and accountability; 15.2 Defining task and context; 15.3 Requirements and code explanation; 15.4 Candidate code and test generation; 15.5 Refactoring and review; 15.6 Failure modes; 15.7 Privacy, dependencies and provenance; 15.8 Verification records; 15.9 Offline alternatives.

**Worked example:** follow one small task from acceptance criteria through candidate output, a discovered failure, revision and human acceptance. Make the rejected attempt visible. The prompt includes relevant code, constraints, desired output, and permitted scope; it does not substitute for the underlying requirement.

**Practical activity and exit artefact:** a compact record of task, tool/model if used, relevant context, output accepted or rejected, changes made and verification performed. For offline use, provide the same candidate output and let the student perform the critique.

**Author instructions and boundaries:** stay vendor-neutral. Verify any tool-specific instructions and date them when drafting. Do not invent institutional AI policy or legal certainty about generated code. Explain that permitted assessment use follows the module leader’s current rules. Avoid private data and secrets in examples. Do not depend on model internals, RAG, agents or prompt tricks. AI-supported implementation and AI components inside an application are distinct topics (G4); this chapter covers the first. Label supplied sample output as constructed or captured (G11).

## 6 Appendices and supporting materials

| Appendix | Purpose | First use | Boundary |
|---|---|---|---|
| A Programming readiness and notation | Diagnostic, minimal syntax refresher, exception handling, the Java idioms the book allows (D2), and the class-diagram notation the midterm assesses (G5) plus diagram legend | Chapters 1–2 | Supports the selected language; does not become an introductory programming course |
| B Tools and reproducible setup | Runtime, build/test commands, Git basics, PR workflow, starter CI, and pinned tools for the DI container, mocking framework, static analysis and repository metrics (G1) | Chapters 2–4, then as each tool appears | Versioned separately so tool changes do not require rewriting design explanations |
| C Engineering templates | Story, acceptance criteria, Definition of Done, planning, PR, retrospective and decision-note templates | Chapters 3–4 onward | Every template includes a small example and its purpose |
| D Project checkpoints and glossary | Domain terms, assumptions, chapter starting points, test commands and evolution map | All chapters | Keep cumulative mainline and optional pattern branches distinct |
| E Critical reading and project evidence | Critical review method, source-checking prompts, final handover and reflection guide, and a guide to contribution evidence (G7) | Chapter 1 onward | Follows the supplied assignment; creates no new rubric or assessment policy |

Appendix E’s review method follows the descriptor’s assignment: an individual review of 1,500–2,000 words of a book from the module leader’s approved list, covering purpose and audience, critique of principles and examples, trade-offs and limits, application to AI-enabled systems, and at least three additional sources. It points to the descriptor’s rubric and does not restate or alter it. The approved list itself remains the module leader’s to supply (D8).

Instructor-only material should contain worked solutions, common student errors, demo notes, formative question answers, change variants and assessment preparation guidance. Keep unseen change variants out of the student edition.

## 7 Book-wide writing and technical instructions

### Explanation and examples

Write as a postgraduate teaching text in clear English. Explain the problem before naming a principle or pattern. Define technical terms at first use. Keep paragraphs connected and prefer concrete behaviour over slogans. Each significant recommendation should state when it helps, what it costs, and a situation where a simpler solution is appropriate.

Use the running domain consistently, but use short isolated examples where it prevents artificial complexity. Avoid repeated animal hierarchies and geometric examples as the main basis of design reasoning. Do not claim one OO style is universally correct or that all conditionals are smells.

### Code and repository contract

1. Select and record the language, runtime, build and test commands before executable chapter drafting.
2. Every snippet labelled runnable must run in its stated checkpoint. Label pseudocode, omissions and intentionally failing examples clearly.
3. Keep small before-and-after comparisons traceable to full files. Explain behaviour changes separately from structural changes.
4. Provide one cumulative checkpoint for each meaningful project stage and separate branches or folders for optional demonstrations.
5. Make intentionally flawed examples safe to inspect: no real credentials, live service charges or destructive commands.
6. Use deterministic clocks and fixtures where needed. Avoid order-dependent tests and unexplained random failures.
7. Verify that tests detect the targeted failure. At selected points, make a deliberate small fault to demonstrate this rather than relying only on pass counts.
8. Document setup from a clean checkout. Record what has actually been run; never claim verification based solely on reading code.

### Diagrams

Use Mermaid source for class, sequence, state and component diagrams where suitable. Keep each diagram focused on one design question, with matching code names and a nearby explanation. Do not combine an entire application into a single unreadable diagram. Use tables for exact comparisons and standard plotting tools for any quantitative figures. When exporting to Word or PDF later, render diagrams and inspect the result rather than leaving raw Mermaid visible to students.

### AI activity contract

Every AI activity specifies: engineering objective; required input; permitted task scope; candidate output; independent checks; acceptance/rejection rationale; and a no-account alternative. A successful activity may conclude that the AI proposal should be rejected.

Sample AI output supplied for offline use is labelled *constructed to illustrate* or *captured* (with tool, model and date) (G11). An activity may be shortened or made optional where it would be padding (G4); record that in the verification record.

Examples must not imply that one AI review independently validates another AI-generated answer. Evidence can include requirements, manually checked examples, compiler/type-checker results, meaningful tests, traced dependencies and human review. Each form has limits that the text should acknowledge without turning every activity into a warning checklist.

### Sources and factual accuracy

The current blueprint’s factual course baseline is the attached **SE506_OO_Development_and_Agile_Practices.docx**, whose internal version is July 2026. The chapter designs and depth assignments are proposals created here; Java and the running project were subsequently confirmed by the module leader. These authoring decisions have not been treated as changes to the official file.

During manuscript drafting, verify references against the source actually used. Use the descriptor’s listed works as the initial reading pool: Martin for OO/Agile principles; Gamma and colleagues for patterns; Fowler for refactoring; Beck for TDD; Feathers for legacy code; Rubin and the Scrum Guide for Scrum. Verify the precise publication details and relevant sections before citing them. Consult official documentation for the chosen language and tools. Also include the other works named in the descriptor’s delivery plan: Evans on domain-driven design (Week 9), Forsgren, Humble and Kim on delivery metrics (Week 11), Humble and Farley on continuous delivery (Week 12), and Fowler’s smells material (Week 4) (G9). Each chapter notes which weekly Martin reading it supports. Check current public sources for AI-tool behaviour and other changing technical claims.

Do not reuse earlier claims about an open textbook’s coverage, licence or publication status without verification. This blueprint commits to neither adopting nor adapting an external textbook. Write original explanations and examples; any adaptation must have a documented permission or compatible licence and attribution.

### Terminology and correctness checkpoints

- Keep responsibility, cohesion, coupling, dependency, abstraction and contract distinct.
- Keep DIP, DI and IoC distinct; keep Factory Method, simple factory and Abstract Factory distinct.
- Explain Scrum’s defined elements separately from common practices such as stories, points and the local Sprint 0 label.
- Distinguish test doubles by role and acknowledge framework terminology differences where relevant.
- Keep unit, integration, contract and E2E scopes explicit; do not present one test taxonomy as the only possible terminology.
- Separate continuous integration, continuous delivery and continuous deployment.
- Describe refactoring as preserving intended observable behaviour; document defects separately from preserved observations.
- A test suite is evidence within its scope, not proof of all behaviour or of the adequacy of requirements.
- Keep source dependency direction distinct from runtime control flow.
- Do not equate architecture with distributed infrastructure, static typing with runtime guarantees, or AI-generated output with verified work.

## 8 Drafting workflow and review gates

### Before the first executable chapter

Use the confirmed Java language and Campus Equipment Lending System. Verify and pin the supporting toolchain (including the DI container, mocking framework, static-analysis tool and repository-metrics method), and freeze the initial domain glossary and invariants. These setup tasks do not require reopening the language, domain or chapter/week sequence. Instructor-specific AI assessment permissions can remain a clearly identified local policy reference until confirmed.

### Review of existing drafts (G13)

Chapters 1–10 and their code-explanation companions exist and have been revised against v0.3 and the alignment review of 13 October 2026. Before drafting each later chapter, check the previous chapter's checkpoint against the current version, and check each chapter's next-chapter inputs: descriptor-required activities (G1), Book/Team labelling and transfer notes (G2, G3), UML scope (G5), milestone-timing mitigations (G6), package design (G8), weekly reading (G9), routes (G10), AI thread balance (G4, G11) and the toolchain decisions in section 9. Record each deviation in a register as *fix now*, *fix at consolidation* or *accepted*, with status, reason, owner and completion evidence. The current register is `Unresolved_Items_Chapters_1-3.md`, which covers Chapters 1–9.

### Recommended writing order

1. Draft Chapter 1 and the prerequisite diagnostic.
2. Establish the starter project and Appendix B with Chapter 2.
3. Draft Chapters 3–4 and the Milestone 1 materials.
4. Draft Chapters 5–7 as one coherent design-and-test progression; review for midterm preparation.
5. Draft Chapters 8–10 with a deliberate pattern-depth check and Milestone 3 checkpoint.
6. Draft Chapters 11–14, preserving the Week 11 to Week 12 change sequence.
7. Develop Chapter 15’s workflow early, then consolidate its examples and cross-references as other chapters stabilise.
8. Complete instructor materials and conduct a book-wide consistency review.

Write and verify one chapter at a time against this blueprint. Avoid generating a complete untested manuscript in one pass. If the chosen domain makes a planned example awkward, change the example before expanding the syllabus.

### Completion gate for each chapter

| Gate | Evidence needed |
|---|---|
| Alignment | Chapter maps to its week and original outcome focus; no assessment timing drift |
| Descriptor fit | Every lab and topic the descriptor names for the week is supported (G1); Book/Team labels and transfer notes are present (G2); core reading, minimum required lab and optional extension are stated (G10) |
| Learning | Each stated outcome has an explanation, example and observable exercise |
| Technical correctness | Code, terminology, diagrams and expected results agree |
| Progression | Prerequisites have already been taught or are explicitly supplied |
| Restraint | Optional depth is labelled; unnecessary patterns and tools are removed |
| AI use | Candidate output is checked independently and an offline route exists |
| Reproducibility | Starting point, commands, expected result and actual verification are recorded |
| Sources | Citations are verified; adaptation rights and attribution are handled |
| Consistency | Glossary, project state and cross-references match the rest of the book |

### Reusable chapter drafting instruction

> Draft Chapter [number and title] for the SE506 student textbook using this blueprint and the current verified project checkpoint. Follow the chapter’s learning outcomes, section sequence, depth limits and weekly alignment. Use the selected programming language consistently. Introduce the engineering problem before the principle or pattern, then provide a worked example, a justified decision, meaningful verification, common mistakes, a bounded AI activity with an offline equivalent, and the specified exercises. Cross-reference previously taught concepts rather than reteaching them at length. Include instructor solution guidance separately. Verify runnable examples and sources; label pseudocode, simulated results and unverified assumptions. Do not change module assessment rules, introduce new syllabus requirements, or force unnecessary patterns into the running project. Finish with a private review against the chapter completion gate and identify any unresolved dependency before claiming the chapter is complete.

## 9 Decisions and open items

The proposed structure is ready for review: 15 chapters, with Chapters 2–14 following Weeks 1–13, supported by five appendices. The primary language is confirmed as Java, and the running domain is confirmed as campus equipment lending. The chapter plan does not depend on choosing a particular AI product, adopting a commercial platform or changing the module descriptor.

### Open decisions

These items are not settled by the descriptor or by earlier confirmation. Each must be closed, with the decision recorded here, before the chapter that needs it is finalised.

| ID | Decision | Needed before | Owner | Status (13 October 2026) |
|---|---|---|---|---|
| D1 | Integration boundary for Chapters 8 and 13: local HTTP stub, file-backed store, embedded database, or other | Chapter 8 executable examples | Module leader and author | **Open, interim.** Chapter 8's provider is a synthetic in-process contract and fixture, chosen deliberately. Chapter 13 (13 October 2026) adds two real boundaries as an interim choice: a local HTTP stub built on the JDK's HttpServer for the borrower directory, and a local tab-separated approval file. The module leader may still choose another store; the policy table, tests and ADR-013 would stay and the adapters would change. |
| D2 | Java language level and permitted idioms (records, lambdas, sealed types, pattern matching) | Chapter 2 executable examples | Module leader and author | **Working choice, not confirmed.** Java 17 (`--release 17`) is used throughout. Which idioms assessments allow, and the institutional JDK, remain module-leader items. |
| D3 | DI container for the Week 5 lab | Chapter 6 | Author | **Closed 13 October 2026 by the module leader.** The educational container written for the book is the adopted lab tool. Chapter 6 should say so explicitly and name its version. The descriptor's wish for a real library container is recorded as a known deviation; Spring was tried only as a feasibility check. |
| D4 | Mocking framework and version; which doubles and framework are permitted in the midterm | Chapter 7 | Module leader | **Split.** Mockito is the book's teaching tool (working choice). Exam permission for Mockito is the module leader's decision and is not yet recorded. |
| D5 | Static-analysis tool for the Week 4 lab | Chapter 5 | Author | **Closed 13 October 2026: PMD 7.28.0.** The module leader approved the download. The Chapter 5 lab is built: a rule set (`config/pmd-smells.xml`, eight design rules at default thresholds), a script (`scripts/pmd.sh`), a findings table, a rule-set comparison, a run record and an optional extraction experiment. Verified on JDK 24.0.2 only; PMD itself needs Java 8 or above. |
| D6 | Whether to supply a second starter checkpoint for the ML model-serving domain, or transfer notes only | Chapter 2 | Module leader | **Open, module-leader dependency.** Chapters use transfer notes only. |
| D7 | Concrete AI/data collaborator for the running-project thread (G4) | Chapter 6 | Author | **Closed 13 October 2026 by the module leader: the data-component route.** Chapter 8's borrower directory is the book's formal data-backed collaborator. Follow-up edits: adjust Chapter 1's promise, preview the contract in Chapter 6, add a double example in Chapter 7, state it in Chapter 8 §8.5, locate it in Chapter 10, and allocate transport timeouts and a fallback-or-failure policy to Chapter 13. No model component is added. |
| D8 | Approved reading list for the critical review | Before Chapter 1 is finalised | Module leader | **Open, module-leader dependency.** Chapter 9's checkpoint defers to the module leader's list. |
| D9 | Repository-metrics method for the Week 11 lab | Chapter 12 | Author | **Open.** Not yet reached. |

### Next steps

1. Draft Chapters 11–15 and Appendices A–E one at a time, in that order (see `Remaining_Chapters_Todo.md`), starting each from the previous chapter's verified checkpoint.
2. Chapters 11-15 are drafted (Chapter 12 by another author); the appendices and the consistency review remain. D3, D5 and D7 are closed (the D5 lab and the D7 follow-ups are done; Chapter 13 delivered the directory timeout and fallback-or-failure policy). D1 remains open with Chapter 13's interim boundary recorded.
3. The unchanged published build configuration (Maven 3.9.11 and the pinned dependencies) was run for Chapters 7–11 on 13 October 2026 and passed, on JDK 24.0.2. Remaining, and marked as **needing the module leader's attention later** (a JDK 17 download was declined on 13 October 2026): run it on a full Java 17 JDK, or deliberately change the published baseline everywhere.
4. Review each new chapter against the completion gate in section 8 before starting the next.
