# SE506 Lecture Slides: Authoring Plan and To-Do List

*OO Development and Agile Practices*  
*MSc in Artificial Intelligence - University of Kurdistan Hewlêr (UKH)*  
*Module Leader: Dr. Polla Abdulhamid Fattah*

This register tracks the authoring, review, and verification of all 13 weekly lecture decks. In accordance with the module leader's instructions, each slide deck is authored **individually with full academic depth and rigor** (45 to 55 slides per deck, calibrated for a 2.5 to 3.0-hour interactive lecture), self-contained, and verified against the running Hugo presentation engine before moving to the next week.

---

## Weekly Deck Status

- [x] **Week 01: Foundations: Software That Can Change & OO Beyond Syntax** (Chapters 1 & 2; LO1, LO6; 54 slides authored and verified).
  * Orientation, Campus Lending domain, Invariants, `[start, endExclusive)` interval logic, Encapsulation, `List.copyOf` snapshots, Cohesion/Coupling, Extract Method, Composition vs Inheritance, UML Class Modelling (Midterm prep), Deliberate Faults, AI claim classification.
- [x] **Week 02: Agile Development, Backlogs & Acceptance Criteria** (Chapter 3; LO5; 52 slides authored and verified).
  * Agile values, iterative feedback loops, User Stories, Given-When-Then Acceptance Criteria, Definition of Done, Backlog grooming, synthetic lending backlog.
- [x] **Week 03: From Requirements to an Iteration: Planning & CI** (Chapter 4; LO5, LO6; Milestone 1; 54 slides authored and verified).
  * Capacity planning lab (G1), velocity vs capacity, task breakdown (WBS), Arrange-Act-Assert (AAA), introductory test runner, GitHub Actions CI baseline.
- [x] **Week 04: SOLID I: Single Responsibility, Extension & Substitutability** (Chapter 5; LO1, LO4; 54 slides authored and verified).
  * SRP, Open-Closed Principle (OCP), Liskov Substitution Principle (LSP), code smell taxonomy, PMD static analysis smell lab (7.28.0).
- [x] **Week 05: SOLID II: Interfaces, Dependency Inversion & Composition** (Chapter 6; LO1, LO4; 48 slides authored and verified).
  * Interface Segregation Principle (ISP), Dependency Inversion Principle (DIP), Composition over inheritance, educational plain-Java DI container, Quiz 1 prep.
- [x] **Week 06: Testing as a Design Practice: TDD & Test Doubles** (Chapter 7; LO3; Milestone 2; 48 slides authored and verified).
  * TDD red-green-refactor rhythm, test list management, Test Double taxonomy (Fakes vs Stubs vs Mocks vs Spies), Mockito interface-only mocks, Milestone 2 MVP.
- [x] **Week 07: Creational Patterns & Object Construction** (Chapter 8; LO2; Midterm Prep; 45 slides authored and verified).
  * Factory Method, Builder Pattern, invariant validation during construction, dependency injection seams, Midterm examination preparation.
- [x] **Week 08: Designing Changing Behaviour: Core Patterns** (Chapter 9; LO2, LO4; 51 slides authored and verified).
  * Strategy Pattern, State Pattern (Item lifecycle & 20-cell transition table), Observer Pattern (NotificationPublisher with snapshot dispatch), Command Pattern (execution-time state); Individual Critical Book Review due (Appendix E).
- [x] **Week 09: Layered Architecture & Package Principles** (Chapter 10; LO2, LO6; Milestone 3; 46 slides authored and verified).
  * Layered architecture (domain, application, infrastructure, presentation, bootstrap), Permitted dependency matrix, Package Cohesion (REP, CRP, CCP), Package Coupling (ADP, SDP, SAP), instability metrics ($C_a, C_e, I$), Evans DDD Entities vs Value Objects, Repository port extraction, Milestone 3 Checklist & ADR-010.
- [x] **Week 10: Refactoring & Working Safely with Legacy Code** (Chapter 11; LO3, LO4; 45 slides authored and verified).
  * Legacy code definitions (Feathers), Characterisation testing loop, Parameter seams with `LocalDate`, Extract Method/Class (`FinePolicy` record), Rollback discipline, Technical debt registers, Quiz 2 revision clinic (Weeks 5-9).
- [x] **Week 11: Measuring Progress, Flow & Technical Health** (Chapter 12; LO5, LO6; 47 slides authored and verified).
  * Empirical flow metrics (Lead Time, Cycle Time, Throughput, WIP, Work-Item Age), Measurement contract, Burn-Down & Burn-Up dynamics, Little's Law, Method RM-12 real repository metrics, DORA / Accelerate metrics, CR-12 Visiting Researcher impact analysis (AC1-AC18).
- [x] **Week 12: Continuous Delivery, Feature Flags & Contract Tests** (Chapter 13; LO3, LO6; Milestone 4; 47 slides authored and verified).
  * Real boundary testing, `@TempDir` FileApprovalSource, JDK HttpClient stalled deadlines, 5-stage CI pipeline (`scripts/pipeline.sh`), Surefire tagged scopes, feature flag lifecycle & removal, rollback realities, CR-12 acceptance matrix (AC1-AC18), AI integration test auditing, Milestone 4 dossier.
- [x] **Week 13: Responding to Change, Handover & Engineering Reflection** (Chapter 14; LO1-LO6; 46 slides authored and verified).
  * Change absorption footprint, coordinator invariant, small diff vs clean design, 3-way triage rule (fix/defer/accept), Fowler's YAGNI carrying costs, handover dossier & TraceabilityTest, dry-run setup verification, 10-minute technical demo, evidence-based retrospectives, qualitative contribution analysis, AI README audits, module capstone synthesis.


---

## Authoring Standards per Deck
1. **Length:** 45 to 55 detailed, substantive slides.
2. **Pedagogical Structure:** 6-part anatomy with section dividers (`# Title`).
3. **Engine Compatibility:** Standard markdown separated by `---`, rendered via `FrontEndBook/layouts/slides/page.html`.
4. **Interactive Teaching Anchors:** Every deck must include a Prediction Exercise, a Deliberate Fault Experiment, and an AI Assistance Bounded Critique.
5. **No Em-Dashes:** Zero `-` characters throughout.
