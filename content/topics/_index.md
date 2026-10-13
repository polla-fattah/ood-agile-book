---
title: "Curriculum Blueprint & Topics"
description: "Syllabus mapping, learning outcomes (LO1–LO6), and chapter topics for Object Oriented Development and Agile Practices."
type: docs
---

*Object Oriented Development and Agile Practices (SE506)*  
*Module Leader: Dr. Polla Abdulhamid Fattah*

This blueprint documents the pedagogical structure of the course, its alignment with the SE506 module descriptor, and the chapter-by-chapter learning progression.

## Module Learning Outcomes

| Label | Module Outcome Focus |
|---|---|
| **LO1** | **Object-Oriented Design & SOLID**: Apply OO principles, responsibilities, cohesion, coupling, and SOLID to design maintainable software. |
| **LO2** | **Design Patterns & Architecture**: Select and justify creational, structural, and behavioral patterns and layered architectural styles. |
| **LO3** | **TDD & Automated Testing**: Apply test-driven development, Arrange-Act-Assert, test doubles, mocks, stubs, and integration contracts. |
| **LO4** | **Code Smells & Refactoring**: Recognize structural code smells and safely refactor legacy code using characterisation tests and seams. |
| **LO5** | **Agile Planning & Flow Metrics**: Plan and deliver iteratively using user stories, capacity planning, and empirical repository metrics (cycle time, throughput). |
| **LO6** | **Professional Workflows & Reflection**: Use professional Git workflows, pull request reviews, and critically justify design trade-offs. |

---

## Chapter Curriculum Progression

### Part I: Foundations & Object-Oriented Principles

#### 1. Developing Software That Can Change {#topic-1}
- Orientation and readiness diagnostic.
- Why functioning programs can be difficult to change; distinguishing system assumptions from class responsibilities.
- [Read Manuscript]({{< relref "/book" >}}) · [View Companion]({{< relref "/companion" >}}) · [Lecture Slides]({{< relref "/slides/chapter-01" >}})

#### 2. Object-Oriented Development Beyond Syntax {#topic-2}
- Encapsulation, invariants, and modeling with UML class diagrams.
- First reviewed change in the Campus Equipment Lending System.
- [Read Manuscript]({{< relref "/book" >}}) · [View Companion]({{< relref "/companion" >}}) · [Lecture Slides]({{< relref "/slides/chapter-02" >}})

#### 3. Agile Development and the Nature of Change {#topic-3}
- User stories, acceptance criteria, backlog management, and sprint planning.
- The nature of changing requirements in agile software engineering.
- [Read Manuscript]({{< relref "/book" >}}) · [View Companion]({{< relref "/companion" >}}) · [Lecture Slides]({{< relref "/slides/chapter-03" >}})

#### 4. From Requirements to an Iteration {#topic-4}
- Translating user stories into technical tasks and executable tests.
- Introduction to Arrange-Act-Assert and Definition of Done.
- [Read Manuscript]({{< relref "/book" >}}) · [View Companion]({{< relref "/companion" >}}) · [Lecture Slides]({{< relref "/slides/chapter-04" >}})

#### 5. Responsibilities, Extension, and Substitutability {#topic-5}
- Single Responsibility, Open/Closed, and Liskov Substitution principles.
- Detecting code smells with static analysis tools (PMD).
- [Read Manuscript]({{< relref "/book" >}}) · [View Companion]({{< relref "/companion" >}}) · [Lecture Slides]({{< relref "/slides/chapter-05" >}})

#### 6. Interfaces, Dependencies, and Composition {#topic-6}
- Interface Segregation and Dependency Inversion.
- Composition over inheritance; decoupling modules with contracts.
- [Read Manuscript]({{< relref "/book" >}}) · [View Companion]({{< relref "/companion" >}}) · [Lecture Slides]({{< relref "/slides/chapter-06" >}})

---

### Part II: Testing, Creation & Behavioral Patterns

#### 7. Testing as a Design Practice {#topic-7}
- Test-Driven Development (TDD) cycle (Red-Green-Refactor).
- Test doubles: dummies, stubs, fakes, and mocks using Mockito.
- [Read Manuscript]({{< relref "/book" >}}) · [View Companion]({{< relref "/companion" >}}) · [Lecture Slides]({{< relref "/slides/chapter-07" >}})

#### 8. Creating and Connecting Objects {#topic-8}
- Factory Method, Abstract Factory, and Builder patterns.
- Dependency injection concepts and educational container walkthroughs.
- [Read Manuscript]({{< relref "/book" >}}) · [View Companion]({{< relref "/companion" >}}) · [Lecture Slides]({{< relref "/slides/chapter-08" >}})

#### 9. Designing Changing Behaviour {#topic-9}
- Behavioral patterns: Strategy, State, Observer, and Command.
- Encapsulating algorithms and state transitions cleanly.
- [Read Manuscript]({{< relref "/book" >}}) · [View Companion]({{< relref "/companion" >}}) · [Lecture Slides]({{< relref "/slides/chapter-09" >}})

---

### Part III: Architecture, Packages & Legacy Systems

#### 10. From Classes to Application Structure {#topic-10}
- Layered architecture and domain-driven design concepts.
- Package cohesion (REP, CRP, CCP) and package coupling (ADP, SDP, SAP).
- [Read Manuscript]({{< relref "/book" >}}) · [View Companion]({{< relref "/companion" >}}) · [Lecture Slides]({{< relref "/slides/chapter-10" >}})

#### 11. Refactoring and Legacy Code {#topic-11}
- Working with legacy systems: characterisation tests, finding seams.
- Safe refactoring steps: Extract Method, Move Method, and managing technical debt.
- [Read Manuscript]({{< relref "/book" >}}) · [View Companion]({{< relref "/companion" >}}) · [Lecture Slides]({{< relref "/slides/chapter-11" >}})

---

### Part IV: Flow Metrics, Continuous Delivery & AI Assistance

#### 12. Measuring Progress, Flow and Technical Health {#topic-12}
- Empirical metrics: lead time, cycle time, WIP, throughput, and work-item age.
- Velocity vs. item throughput; repository metrics analysis.
- [Read Manuscript]({{< relref "/book" >}}) · [View Companion]({{< relref "/companion" >}}) · [Lecture Slides]({{< relref "/slides/chapter-12" >}})

#### 13. Integration, Delivery and Feedback {#topic-13}
- Integration and contract testing; boundary testing against local services.
- Continuous Integration gates and feature flags with controlled rollouts.
- [Read Manuscript]({{< relref "/book" >}}) · [View Companion]({{< relref "/companion" >}}) · [Lecture Slides]({{< relref "/slides/chapter-13" >}})

#### 14. Responding to Change and Handing Over {#topic-14}
- Final change delivery, architecture decision records (ADRs), and retrospectives.
- Qualitative contribution evidence without vanity commit counting.
- [Read Manuscript]({{< relref "/book" >}}) · [View Companion]({{< relref "/companion" >}}) · [Lecture Slides]({{< relref "/slides/chapter-14" >}})

#### 15. AI as a Software Engineering Assistant {#topic-15}
- Vendor-neutral engineering practices for leveraging AI assistants.
- Boundary condition validation, prompt engineering, and human accountability.
- [Read Manuscript]({{< relref "/book" >}}) · [View Companion]({{< relref "/companion" >}}) · [Lecture Slides]({{< relref "/slides/chapter-15" >}})

