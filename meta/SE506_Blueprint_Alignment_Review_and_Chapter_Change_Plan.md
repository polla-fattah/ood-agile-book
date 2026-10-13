# SE506: Blueprint alignment review and chapter change plan

**Review date:** 13 October 2026  
**Baseline:** revised *SE506_Textbook_Blueprint_and_Authoring_Instructions(1).md*, labelled Version 0.3, 12 October 2026  
**Scope:** the 19 uploaded Markdown files covering Chapters 1–9 and their companions, plus the Chapter 10 manuscript. The earlier Chapter 10 companion was inspected separately as a supplementary source.

## 1. Overall judgement

**The change of direction has been implemented substantially, but not completely.** Chapters 1–9 contain real improvements rather than only new labels. Chapter 2 now has a substantial UML teaching sequence; Chapter 4 introduces Arrange–Act–Assert; Chapter 7 brings the milestone checklist forward and adds useful midterm practice; Chapters 3–9 make weekly readings and team-project application clearer. The revised companions also strengthen several previously weak assertions.

However, the book should not yet be described as fully aligned with the revised blueprint. The principal outstanding work is:

1. Supply the actual smell-analysis lab in Chapter 5.
2. Resolve and deliver the selected DI-container lab in Chapter 6.
3. Make the AI/data-component thread an explicit, continuous project decision. Chapter 8 offers a useful starting point, but earlier promises and the blueprint's decision deadline are not reconciled.
4. Verify the revised Chapters 7–9 with the build configuration printed for students.
5. Update Chapter 10's teaching and carry the revised earlier checks into its restructured checkpoint.
6. Make required practical work and unavailable supporting references unambiguous.

These are targeted corrections. The existing chapter sequence, Java choice, lending domain, two-file delivery format and most explanations should be retained.

### What this review establishes

Every uploaded file was compared with its earlier local draft. Changed teaching material, relevant code listings, activity instructions, verification records and cross-chapter dependencies were examined against the blueprint. All 18 uploaded files for Chapters 1–9 contain changes; the uploaded Chapter 10 manuscript is identical to the earlier manuscript.

This is a documentary and source-comparison review. **I did not rerun the Java projects, mutation experiments, external-source checks or Mermaid renders for this report.** Run results described below are claims recorded in the supplied companions, not new execution results from this review. A successful historical run of an earlier version does not verify later edits.

No chapter, companion, blueprint or module descriptor was edited during this review. This document specifies the changes to make.

## 2. Priority and status conventions

| Label | Meaning |
|---|---|
| P1: Fix now | A required activity, cumulative checkpoint, or reproducibility claim remains incomplete. Resolve before calling the affected chapter aligned. |
| P2: Fix at consolidation | A teaching, navigation or evidence-record correction needed before student release. It does not justify restarting the chapter. |
| Decision | An author or module-leader decision is needed. Record the owner and outcome; do not invent assessment permissions. |
| Retain | The revision already addresses the requirement adequately within this review's scope. |

“Largely aligned” below is a judgement about the change of direction, not certification of every technical statement or executable example.

## 3. Alignment with the revised ground rules

| Rule | Finding in the supplied chapters | Remaining action |
|---|---|---|
| G1: scheduled activities | Issue-board setup, capacity planning and the mocking-framework lab are present. The smell analyser is unnamed; the adopted DI container is unresolved. | Complete Chapters 5–6. Repository metrics, contracts and feature flags belong to future Chapters 12–13 and are not omissions from Chapters 1–10. |
| G2–G3: Book/Team distinction and transfer | Chapters 1–9 now distinguish the main practical work and explain transfer. Chapter 10 still lacks the same explicit treatment. | Label Chapter 10 work; distinguish supplied book checkpoints from evidence produced on the assessed team project. Decide how teams obtain any second starter domain. |
| G4: two AI threads | AI-assistant activities are well developed. Chapter 1 promises an AI/data collaborator; Chapter 8 explicitly connects its directory adapter to data/model boundaries. | Resolve D7 and document a continuous route through contracts, doubles, failure handling and architecture. A directory can support a data-component route, but the choice must be explicit. |
| G5: UML preparation | Chapter 2 now includes notation, code-to-diagram reasoning, a worked scenario, reading/checking tasks, an error exercise and a scenario exercise with solutions. | Retain this expansion; complete the supporting notation reference and correct the specific diagram issues noted below. |
| G6: milestone timing | Chapter 4 has AAA preparation; Chapter 7 has an opening Milestone 2 checklist. Chapter 10 retains its checklist material near the end. | Add the early Chapter 10 checklist and minimum architecture exercise. |
| G7: contribution evidence | Early chapters support real review and avoid treating commit counts as sufficient evidence. Full coverage is allocated to Chapter 14 and Appendix E. | Preserve this approach; do not add a new contribution rubric to these chapters. |
| G8: package design | Chapter 10 explains layers, source dependencies, ports and a dependency gate. It does not explicitly teach the required package cohesion, coupling and stability treatment. | Add a focused Section 10.4 extension and corresponding exercise/solution. |
| G9: weekly reading | Chapters 3–9 now map to the weekly Martin reading. Chapter 2 lacks that explicit mapping; Chapter 10 lacks the Martin package-design and Evans reading connection. | Add these mappings and verify the cited sections. Chapter 1 is orientation and can point to the Week 1 route. |
| G10: manageable routes | Chapters 1–9 have core/lab labels, but “lab route” often mixes required work with optional extensions. Chapter 10 has no equivalent task route. | Define minimum required reading, minimum required practical work and optional depth separately. |
| G11: AI-output provenance | Constructed fixtures are explicitly identified. | Retain; no need to regenerate them merely to obtain real model output. |
| G12: authoring packet | The two-file pairs already contain much of the required teaching packet. Some required lab components and supporting references remain unavailable. | Complete the missing content inside the existing two-file format. |
| G13: review record | Companions say they were reviewed against v0.3 and explain many checks, but important unresolved items remain. | Use an explicit deviation register with status, reason, owner and completion evidence. Include Chapter 10 in the review boundary. |

## 4. Corrections shared across chapters

### 4.1 Resolve the AI/data route without forcing a second application

**Evidence:** Chapter 1 Section 1.6 promises a model- or data-backed collaborator. Blueprint D7 requires choosing the concrete collaborator before Chapter 6. Chapter 6 continues to teach notification injection, and Chapter 8 Section 8.5 introduces the directory as a data-backed collaborator and supplies an ML-domain transfer paragraph.

This is partial implementation, not an entirely missing thread. The directory already provides useful material about translation, missing data, invalid results, failure and substitution. What is missing is a recorded decision connecting that material to the book-wide objective.

**Change:** choose and record one of these approaches:

- **Data-component route:** formally designate the directory as the cumulative data boundary. Adjust Chapter 1's promise accordingly; preview its contract in Chapter 6; use a small relevant double example in Chapter 7; retain the adapter in Chapter 8; locate it explicitly in Chapter 10. Allocate transport timeouts and an explicit fallback-or-failure policy to Chapter 13. Record the delayed introduction relative to D7.
- **Model-component route:** introduce one small synthetic model/scoring collaborator, with a narrow contract and bounded outcomes. Add only the contract, substitution and failure examples needed in Chapters 6–8, and place it in Chapter 10's structure. Define a neutral or disabled baseline so earlier reservation behaviour is not silently changed.

The blueprint allows AI **or data** components. Do not add a prediction model merely to make the book appear more AI-oriented. Equally, a transfer paragraph alone should not be reported as completion of a cumulative project thread. Neither approach requires training a model, a paid AI account, or a live service in early chapters.

**Completion evidence:** one decision entry; a chapter-to-capability table; matching actual code/checkpoints; stated invalid-output and failure behaviour; tests using a substitute; an explicit later integration plan.

### 4.2 Separate the required lab from optional depth

Several opening routes put required outcomes under “Core route” and leave a mixture of additional required work, AI exercises, review questions and optional extensions under “Lab route.” This makes the labels poor guides to the minimum weekly workload.

**Change:** use three short entries: **Core reading**, **Minimum required lab**, and **Optional extension**. Label Book project and Team project work within the required lab. Identify which book examples students trace or run and which changes they must independently implement on their team project. Do not require rebuilding all book examples and repeating all of them on the team project unless that workload is intentional.

Examples needing attention include Chapter 1's fault task, Chapter 2's Git/issue-board work, Chapter 6's container exercise, Chapter 7's demonstration/retrospective, and the working-knowledge pattern examples in Chapters 8–9. “Working knowledge” means limited required depth, not automatic omission.

### 4.3 Make supporting references usable now

Chapters 1–9 now direct students to specific Chapter 15 sections, often saying “read ... before this activity.” Appendices A and B are also described as if available. These supporting manuscripts are not in this review set; the Chapter 9 companion explicitly says Appendix E is not yet written.

**Change:** either supply the referenced material or make the local activity self-contained and describe the future material as additional reading. A missing appendix must not be the only place containing the tool name or command needed to complete a mandatory lab. Check exact Chapter 15 section numbers once its manuscript exists.

This is a delivery dependency, not a reason to expand every chapter with repeated setup instructions.

### 4.4 Reconcile the verification environment and the published build

The revised Chapter 7 companion Section 12 and Chapter 8/9 verification sections state that their printed dependency versions were **not** used for the new runs. The reported runs used JDK 24.0.2, Maven 3.9.16, JUnit 6.0.3, Mockito 5.23.0, Compiler Plugin 3.15.0 and Surefire 3.5.6. The printed configuration continues to specify Java 17, Maven 3.9.11, JUnit 5.13.4, Mockito 5.20.0, Compiler Plugin 3.14.1 and Surefire 3.5.4.

The disclosure is good. It also means the revised deliverable has not yet passed its exact published setup. Compiling application source with `--release 17` does not, by itself, establish that the complete test toolchain runs on the intended Java 17 runtime.

**Change:** run the revised listings using the unchanged published configuration and a full Java 17 JDK. Alternatively, deliberately adopt a new compatible toolchain and update all affected POMs, setup instructions, CI configuration and references together. Do not silently substitute cached versions.

Keep historical and current runs in separate, clearly labelled tables. Claims such as “the supplied configuration was verified” must identify which source revision and dependency set were actually used. Mockito agent observations made with the alternative versions must remain qualified as observations of that setup.

### 4.5 Preserve the two-file format and identify exact checkpoints

Keep one student manuscript and one code/explanations/solutions file per chapter. Lab instructions, instructor notes, checkpoint listings and verification records can remain sections in those files.

Record which revision of each preceding companion is the input to the next chapter. Repeated complete listings make the book convenient to use, but they can also carry old tests forward. Chapter 10 currently demonstrates that risk. Preserve intentional changes to package/import/constructor wiring while carrying forward substantive assertions and fixes.

## 5. Chapter-by-chapter changes

### Chapter 1: Developing Software That Can Change

**Status: largely aligned; small consolidation changes.**

**Retain:** the separate orientation example, Book project label, two distinct AI themes, constructed fixture, common-mistakes table and stronger evidence statement in Task C. The companion supplies both duration- and count-boundary explanations.

| File and location | Change | Priority / completion check |
|---|---|---|
| Manuscript: opening reading route and Section 1.9 | Put Task B in the minimum required diagnostic because the output checklist requires the fault-revealing input. Keep running the program optional. | P2: a student following the minimum route produces every required diagnostic artefact. |
| Manuscript: Section 1.6 | Make the AI/data promise match the D7 decision, with the first concrete chapter named. | Decision + P2: the promise points to actual material or an explicitly tracked future dependency. |
| Manuscript: Chapter 15 / Appendix A–B–E references | Remove mandatory reliance on unavailable material or supply it. | P2: Activity 1A and the diagnostic can be completed from the delivered files. |
| Companion: Section 4 | Distinguish the working Java 17 baseline used elsewhere from any still-unconfirmed institutional setup. The statement that the semester JDK is “not yet pinned” needs the same decision status as the rest of the book. | P2: one consistent toolchain decision, without mislabelling the reported JDK 24 run as a new Java 17 run. |

No redesign of the introductory code is needed.

### Chapter 2: Object-Oriented Development Beyond Syntax

**Status: major required changes implemented; retain the UML expansion.**

The new Section 2.6, kit-modelling exercise and companion Sections 6.2a–6.2b directly address G5. Issue-board setup and a branch-policy decision are now explicit in Part D.

| File and location | Change | Priority / completion check |
|---|---|---|
| Manuscript: opening route and Section 2.10 | Identify Parts C and D as minimum required work, including the checked commit and issue board. Include Section 2.8 explicitly if its AI analysis remains a required artefact; neither current route names it. | P2: all required outputs have a route to the explanation and task that produces them. |
| Manuscript: module connection / sources | Add the descriptor's Week 1 Martin reading mapping. | P2: the reading note identifies the introduction/OO fundamentals route without inventing page numbers. |
| Manuscript: Section 2.6 worked workshop scenario | Separate scenario facts from design assumptions. The prose says to include only what the description mentions, but the proposed technician/tool names and printer contract are design choices beyond the exact supplied wording. | P2: label those choices and accept justified alternatives in the answer guidance. |
| Manuscript + companion: UML figures and feedback | Keep diagrams focused and readable. Check the larger left-to-right notation examples at normal reading size; split or use top-down layout if they become too wide. Keep Mermaid only where the relationship explanation benefits. | P2: readable diagrams, consistent legends, and matching model answers. |
| Companion: Section 11 continuity note | Replace the stale statement that the Maven/JUnit starter “that Chapter 4 needs is not yet built.” Chapter 4 deliberately uses a Bash/plain-Java gate; Chapter 7 supplies Maven/JUnit. | P2: describe the actual sequence: Chapter 2 flat files → Chapter 4 conventional folders and plain-Java gate → Chapter 7 Maven/JUnit. |
| Companion: teaching guidance / D2 | Avoid saying students “will have to” draw by hand unless that exam condition is confirmed. State the permitted Java idioms in the setup reference rather than leaving the language decision apparently open. | P2 / Decision: classroom practice remains useful without inventing exam delivery rules. |

Do not replace the expanded UML section with a shorter notation-only summary; the modelling method and exercises are the important improvement.

### Chapter 3: Agile Development and the Nature of Change

**Status: largely aligned; no substantial content rewrite identified.**

**Retain:** Team project instructions, the distinction between formal Scrum and classroom adaptations, explicit workflow policies, weekly reading links, constructed AI-output classification and the strengthened two-sided adjacency example.

| File and location | Change | Priority / completion check |
|---|---|---|
| Manuscript: opening route and Section 3.10 | Clarify the minimum backlog/board/estimation activity and separate optional execution from required process evidence. | P2: the minimum route produces the artefacts listed in the completion check. |
| Manuscript: Section 3.9 | Apply the common Chapter 15-reference correction. | P2: the supplied fixture is enough to complete the activity now. |
| Companion: Section 8 and verification record | Preserve both directions of adjacency in `Chapter03AcceptanceExamples` in every later full checkpoint. Record which Chapter 2 input version was used. | P1 for downstream continuity: Chapter 10 must not revert to the earlier one-sided AC-03. |
| Companion: process solutions | Keep the existing model answers; add a compact pointer from each required team artefact to its worked example if needed during route consolidation. | P2: students can locate the model without treating it as their own project evidence. |

There is no need to add an artificial AI-model implementation to this process chapter. Any newly selected data/model work can appear as a clearly planned backlog item where relevant.

### Chapter 4: From Requirements to an Iteration

**Status: the main directional changes are implemented.**

Section 4.4 already contains a concrete capacity calculation and replanning discussion. Section 4.6 now introduces AAA. The practical task asks for the team's own availability, real CI evidence and a fresh-checkout check. These requirements should not be reported as missing.

| File and location | Change | Priority / completion check |
|---|---|---|
| Manuscript: opening route / Section 4.10 | Describe steps 1–8 as the minimum milestone lab, distinguishing the supplied lending demonstration from each team's actual work. | P2: required work is not confused with optional depth. |
| Manuscript: Section 4.8 | Keep the AI planning activity self-contained until its Chapter 15 target is delivered. | P2: no unavailable prerequisite. |
| Companion: repository instructions and Section 10 | Retain `.gitattributes`, the flat-directory migration explanation and the explicit “hosted run not performed” boundary. Keep environment-specific observations attached to the tested environment. | Retain / P2: a local or partially completed WSL run is not recast as a full hosted/Linux validation. |
| Companion: checkpoint copies | Preserve the revised acceptance runner and LF-script configuration in later chapters. | P1 for downstream continuity: final checkpoint listings include the intended revisions. |

Keep Maven/JUnit at Chapter 7 unless a deliberate book-wide toolchain change is made. The revised blueprint does not require moving the entire test-framework lesson into kickoff week.

### Chapter 5: Responsibilities, Extension and Substitutability

**Status: partially aligned; the smell-analysis lab remains incomplete.**

**Evidence:** Section 5.1 supplies a real `javac -Xlint:all` command and explains why a clean compiler report does not diagnose the coordinator's responsibilities. It then says to run “the smell-oriented analyser your module has pinned in Appendix B.” No analyser name, version, ruleset, runnable setup or worked findings are supplied in this chapter pair. The companion's verification reports compiler lint, not a completed smell-analyser lab.

| File and location | Change | Priority / completion check |
|---|---|---|
| Manuscript: Section 5.1 and practical steps 1/8 | Name the chosen tool and version, specify the exact checkpoint and command, and give a short walkthrough of one relevant finding. Retain compiler lint as a useful comparison. | P1: the required lab can be run without an unnamed future tool. |
| Manuscript: smell comparison | Ask students to distinguish a useful finding, a low-value/context-dependent finding and a manual design concern missed by the tool. Do not promise every category will arise naturally from the tiny starter. | P1: if necessary, supply a small labelled smell fixture, separate from the cumulative project. |
| Companion: add a lab solution beside the responsibility diagnosis | Supply configuration, reproducible invocation, a small findings table and a model manual-versus-tool comparison. State tool/rule/location, interpretation and action. | P1: the solution explains the evidence rather than merely listing warnings. |
| Companion: verification record | Record an actual run of the selected tool and distinguish it from the existing lint results. Close D5 or record the precise outstanding dependency. | P1: no claim that `-Xlint` alone fulfils the planned smell-oriented exercise. |
| Both files: route / review task | Keep peer or honestly labelled solo review in the required practical route. | P2: the stated review outcome is supported by a task. |

Retain the two-stage refactoring/feature separation, contract discussion, LSP example and improved dependency diagram.

### Chapter 6: Interfaces, Dependencies and Composition

**Status: useful conceptual revision, but the container decision and delivered lab are not closed.**

The educational container is already executable and teaches registration, resolution and lifetime. It should not be described as absent. However, Section 6.6 still says “if your module pins a container” and “if an instructor uses a container.” The companion labels its Spring experiment as feasibility work, explicitly says it is not part of the chapter, and says no container has been adopted.

| File and location | Change | Priority / completion check |
|---|---|---|
| Manuscript: Section 6.6 | Resolve D3. Prefer a short, pinned library-container walkthrough after manual wiring. If the educational container is intentionally the adopted lab tool, say so explicitly, version it and record the rationale/deviation against the blueprint's supporting-tool expectation. | P1 / Decision: no conditional wording about whether the required lab exists. |
| Companion: container listings / feasibility note | For a library-container route, supply the complete isolated lab setup and build configuration, not an account of manually assembling cached jars. Keep the cumulative plain-Java application unchanged. | P1: a fresh learner can run the lab and observe construction, lifetime and a missing binding. |
| Both files: AI/data progression | Implement the chosen D7 bridge: introduce or preview the actual collaborator contract and identify the later chapter that implements its boundary. | P1: the book-wide promise has a concrete, traceable route. |
| Manuscript: Figure 6.2 and caption | Correct arrow semantics. The caption says every arrow means “is passed to the constructor of,” but arrows from the application entry point to the policy map/sender/coordinator actually depict creation. Label creation and injection separately or remove the entry-point edges and show only constructor arguments. | P2: every arrow has the meaning claimed in its legend. |
| Manuscript: Figure 6.1 explanation | Say the coordinator holds a category-to-policy map, rather than implying one direct `BorrowingPolicy` field. Keep the simplified association if its collection role is stated. | P2: diagram explanation matches the final coordinator's `Map<BorrowerCategory, BorrowingPolicy>`. |
| Companion: current checks | Preserve the two new unexpected-sender-failure checks and serial-warning correction in subsequent checkpoints. | P1 for continuity: later chapters do not restore the old 26-check variant. |

Do not select a particular framework solely because one version happened to be cached. Compatibility with the book's chosen runtime is part of the decision.

### Chapter 7: Testing as a Design Practice

**Status: pedagogically much improved; exact-configuration verification remains open.**

**Retain:** the early Milestone 2 checklist; manual doubles before Mockito; stronger snapshot assertion; team-project TDD task; expanded UML/diagnosis/refactoring/test practice with companion solutions. The mocking-framework content itself is present.

| File and location | Change | Priority / completion check |
|---|---|---|
| Companion: POM, Section 5 and Section 12 | Run the revised source with the printed dependency versions and intended Java runtime, or deliberately update the published baseline everywhere. | P1: a clean build using the documented configuration, with expected TDD red/green outcomes and the new practice solution checked. |
| Manuscript: Section 7.5; companion: mock-maker notes / references | Scope agent-loading observations to the JDK/Mockito combination actually observed. Avoid presenting the warning-suppression setting as a generally established requirement of the pinned setup. | P2: tool-specific guidance matches the setup students actually use. |
| Manuscript: Section 7.12; companion: practice solutions | Record D4's exam-permission decision when supplied by the module leader. Until then, state that the framework permission is pending; do not imply the author can approve it. | Decision: separate the book's teaching tool from permitted assessment tools. |
| Companion: Section 6.1 and fault-experiment row | Reconcile the fault inventory. The text says 15 faults, 13 initially caught and 2 surviving, but the displayed “caught” table contains 14 fault rows, followed by two survivors. | P2: derive totals from a named experiment list, or explain which rows belong to a different round. |
| Manuscript: opening route | Ensure the minimum milestone route includes the needed demonstration/review/retrospective evidence, even though current step 7 sits in the lab route. | P2: the opening checklist and required route agree. |
| Both files: selected AI/data thread | Add a focused substitute/result-validation example only if needed to connect D7; reuse existing double concepts rather than adding a second testing syllabus. | P1 if required by the chosen thread: a concrete contract and independently defined expectations. |

The companion is appropriately candid about its alternative-version run. Preserve that honesty while closing the remaining verification task.

### Chapter 8: Creating and Connecting Objects

**Status: largely aligned in teaching; data-thread and verification decisions remain.**

**Retain:** the sequence-diagram introduction, explicit data-component connection, added Builder/Decorator tasks and their solutions, team transfer, and separation of isolated patterns from cumulative code.

| File and location | Change | Priority / completion check |
|---|---|---|
| Manuscript: Section 8.5 | State whether the directory formally fulfils D7's data-component route or is only an analogy supporting a separate chosen collaborator. | P1 / Decision: later chapters continue the same declared thread. |
| Manuscript + companion: directory setup | Resolve D1's boundary description. The current provider is a synthetic in-process contract/fixture. Record that deliberately, and identify what transport/storage boundary Chapter 13 will add. | Decision: no claim of real-provider or transport integration based only on the fixture tests. |
| Companion: Section 11.2 | Verify the printed POM versions. Separate historical observations from current revised-source evidence. | P1: the same baseline rule as Chapter 7 is satisfied. |
| Companion: fault experiment | Reconcile the stated 19 faults with the table: 8 adapter + 3 service + 2 builder + 4 decorator + 2 family/escaping + 1 Factory Method entry = 20 listed faults. | P2: count or grouping corrected from the experiment record. |
| Companion: end of verification section | Remove or qualify the stale sentence “no extra mutation-run result is claimed,” which conflicts with the new detailed mutation-run report. | P2: one consistent evidence account. |
| Manuscript: opening route / companion: Section 8.4 | Label the Builder and Decorator extension solutions as a separate exercise checkpoint. Keep working-knowledge coverage required, while controlling additional work during midterm week. | P2: no accidental expectation that every optional exercise is already in the 63-invocation baseline. |

Do not add a network service merely to fix a wording issue. The integration decision should determine the smallest necessary implementation.

### Chapter 9: Designing Changing Behaviour

**Status: largely aligned in teaching; complete verification and downstream preservation.**

**Retain:** state/sequence explanations, the explicit Team project task, weekly reading, the critical-review checkpoint, and stronger command-construction and exact-result assertions.

| File and location | Change | Priority / completion check |
|---|---|---|
| Companion: Section 12 | Verify the revised listings using the printed configuration; label inherited historical tables with their source revision. | P1: exact published setup verified. |
| Companion: command tests and checkpoint handoff | Carry forward the new null/blank construction checks and exact confirmation-period assertion into Chapter 10. | P1: package migration preserves these assertions, not just the four-test method count. |
| Manuscript: opening route / practical activity | Keep Observer and Command at bounded working-knowledge depth but make the required minimum explicit. Avoid equating “outside the core reading” with “unnecessary for this week's named topics.” | P2: all four named patterns have an observable learning task. |
| Manuscript: Appendix E checkpoint; companion: Section 11 | Reconcile “Appendix E develops...” with the companion's statement that the appendix is not written. Preserve the local checkpoint as sufficient interim guidance. | P2: students know what is available and that the approved brief governs the assignment. |
| Companion: verification commentary | Replace “strongest in the book so far” for the Observer mutation result with the narrower observation that the ten selected faults were detected. Different fault sets do not establish a comparable ranking of test quality. | P2: evidence supports the exact conclusion stated. |

No new AI/model pattern example is needed merely to mention that thread. A short connection to the chosen collaborator is enough unless a genuine variation or lifecycle requirement arises.

### Chapter 10: From Classes to Application Structure

**Status: not yet revised to the new direction. Highest combined teaching/continuity priority.**

The uploaded manuscript is unchanged from the earlier version. Its layers, ports, repository example, `jdeps` gate and source-versus-runtime distinction are useful and should be retained.

**Companion scope limitation:** no revised Chapter 10 companion was attached. The findings below refer to the earlier available `Chapter_10_Code_Explanations_and_Solutions.md`, Version 1.0, 13 October 2026. If another revised companion exists, compare it against these findings before editing; do not assume the older copy represents it.

| File and location | Change | Priority / completion check |
|---|---|---|
| Manuscript: opening | Add an immediately usable Milestone 3 checklist and separate core reading, minimum lab and optional depth. | P1: students can begin the required architecture work before reading the whole chapter. |
| Manuscript: Section 10.4 | Add package cohesion, coupling and stability through the actual package map. Discuss what should change together, what clients must depend on, and the consequences of directing dependencies toward more stable contracts. Map this to Martin's package-design reading. | P1: one worked design comparison and a student diagnosis task, with trade-offs. |
| Manuscript + companion: optional quantitative example | If using instability, define the chosen counting unit and use `I = Ce / (Ca + Ce)`, with incoming/afferent `Ca` and outgoing/efferent `Ce`. Treat no dependencies (`Ca + Ce = 0`) as undefined unless a clearly documented reporting convention is chosen. Otherwise keep the explanation qualitative. | P1 only if quantified: formula, example, zero case and interpretation agree; no claim that the number alone measures design quality. |
| Manuscript: reading sources | Add the Week 9 Martin package-design and Evans DDD reading connections, using verified bibliographic/section details. | P2: both required and recommended reading roles are explicit. |
| Manuscript: Section 10.11 | Label the worked restructuring as Book project and add a bounded Team project architecture review/ADR task. Tie the milestone checklist to evidence from that team project. | P1: copying the supplied architecture is not confused with demonstrating the team's own decisions. |
| Manuscript: Section 10.4/10.8 | Explain the compact package/dependency view when first used, and locate the selected AI/data collaborator's contract, implementation and construction point. | P1 for D7 continuity; retain the existing useful Mermaid diagrams. |
| Companion: cumulative listings | Rebase the structural migration on the revised Chapter 9 checkpoint. Preserve substantive changes while applying package/import/constructor moves. | P1: see the concrete preservation list below. |
| Companion: model answers / ADR / verification | Add the package-design answer, minimum-lab guidance, revised migration map and exact-configuration run record. | P1: all new teaching requirements have a solution and appropriate evidence. |

#### Concrete Chapter 10 preservation list

The earlier Chapter 10 companion still carries older versions of several listings. Source inspection found these specific differences from the uploaded revised sequence:

| Earlier improvement | Location to preserve in Chapter 10 |
|---|---|
| Chapter 3's request ending exactly at an existing reservation's start | `Chapter03AcceptanceExamples`: retain the added AC-03 request and assertions. |
| Chapter 6's unexpected sender failure propagation and stored-record checks | `Chapter06Checks`: retain the new `BrokenSender` case and the resulting 28-check record. |
| Chapter 7's unmodifiable loan-list assertion | `LoanServiceTest.checkoutAndReturnUseTheSuppliedClock`: restore the specific `snapshot::clear` assertion. Other snapshot assertions elsewhere do not replace this loan contract check. |
| Chapter 8's plain exporter null-input check | `PatternExamplesTest`: retain the new `plain.run(null)` assertion as well as the HTML check. |
| Chapter 9's command construction validation and exact period | `ReserveEquipmentCommandTest`: retain the added constructor failure assertions and exact confirmation assertion instead of the older prefix-only check. |
| Revised portability and warning fixes | Carry forward `.gitattributes` and the deliberately added exception serialization identifiers where applicable. |

Some strengthened assertions do not increase the number of JUnit invocations. Therefore a reported total of 118 in the older Chapter 10 build cannot establish that the revised earlier assertions were retained. Check their substance and rerun the resulting checkpoint.

## 6. Blueprint housekeeping needed to support these changes

These corrections concern the authoring baseline; they do not change the module descriptor.

1. Give the changed blueprint a distinct revision identifier. Both old and revised documents currently use 0.3.
2. Replace the instruction to review Chapters 1–9 before continuing Chapter 10 with the actual current boundary: review Chapters 1–10 before building Chapter 11 on their checkpoint.
3. Reinstate the explicit two-Markdown-file packaging rule.
4. Update D2 and the teaching-tool portion of D4 to distinguish established working choices from institutionally unconfirmed matters. Keep exam permissions under the module leader's control.
5. Close D3, D5 and D7 with actual choices and deliverables. Record D1's current fixture boundary and later integration plan. Do not mark decisions closed merely because a companion contains a feasibility note.
6. Track D6 and D8 as module-leader dependencies. Do not create an unapproved second assessed domain or approved-reading list within a chapter solution.
7. Define “core route” and “lab route” so required labs are never inadvertently presented as optional.

## 7. Recommended implementation order and acceptance gate

| Order | Work | Why this order matters |
|---|---|---|
| 1 | Record the toolchain and D1/D3/D5/D7 decisions; identify unavailable supporting references. | Prevents contradictory fixes in several chapter pairs. |
| 2 | Finish the Chapter 5 analyser and Chapter 6 container/data-contract material. | These establish the missing foundations for subsequent examples. |
| 3 | Apply focused route/reference corrections to Chapters 1–4 and 7–9. | Preserves successful revisions while closing delivery gaps. |
| 4 | Verify the revised Chapters 7–9 with the published build configuration. | Establishes the actual input checkpoint for the architecture chapter. |
| 5 | Update Chapter 10 teaching and migrate the revised Chapter 9 source and tests. | Avoids losing the newly strengthened assertions during restructuring. |
| 6 | Consolidate the deviation register and continue with Chapter 11. | Future work starts from an identified, consistent baseline. |

Before calling a chapter aligned, check:

- Its required lab can be completed from supplied files and explicitly named prerequisites.
- The minimum route produces every required artefact; optional work is separately labelled.
- Book-project demonstrations and team-project evidence are distinguishable.
- Its diagrams, captions, contracts and code describe the same design.
- Its next chapter inherits the intended source and assertions.
- Its verification record identifies the exact revision, runtime and dependency set actually run.
- Unavailable appendices, pending assessment permissions and accepted deviations are visible rather than silently assumed complete.

**Recommended disposition:** accept the overall direction, retain the successful revisions, and close the P1 items before treating Chapters 1–10 as the baseline for further drafting.

## Appendix: source-file register

The uploaded files were read directly from their supplied workspace copies. “Manuscript” and “companion” above refer to these exact filenames; section numbers identify the relevant location without relying on unstable line numbers.

| Chapter | Manuscript | Companion |
|---|---|---|
| 1 | `Chapter_01_Developing_Software_That_Can_Change(1).md` | `Chapter_01_Code_Explanations_and_Solutions(1).md` |
| 2 | `Chapter_02_Object_Oriented_Development_Beyond_Syntax(1).md` | `Chapter_02_Code_Explanations_and_Solutions(1).md` |
| 3 | `Chapter_03_Agile_Development_and_the_Nature_of_Change(1).md` | `Chapter_03_Code_Explanations_and_Solutions(1).md` |
| 4 | `Chapter_04_From_Requirements_to_an_Iteration(1).md` | `Chapter_04_Code_Explanations_and_Solutions(1).md` |
| 5 | `Chapter_05_Responsibilities_Extension_and_Substitutability(1).md` | `Chapter_05_Code_Explanations_and_Solutions(1).md` |
| 6 | `Chapter_06_Interfaces_Dependencies_and_Composition(1).md` | `Chapter_06_Code_Explanations_and_Solutions(1).md` |
| 7 | `Chapter_07_Testing_as_a_Design_Practice(1).md` | `Chapter_07_Code_Explanations_and_Solutions(1).md` |
| 8 | `Chapter_08_Creating_and_Connecting_Objects(1).md` | `Chapter_08_Code_Explanations_and_Solutions(1).md` |
| 9 | `Chapter_09_Designing_Changing_Behaviour(1).md` | `Chapter_09_Code_Explanations_and_Solutions(1).md` |
| 10 | `Chapter_10_From_Classes_to_Application_Structure(1).md` | No revised upload; supplementary review of earlier `Chapter_10_Code_Explanations_and_Solutions.md`, Version 1.0 |

The revised blueprint is the alignment authority for this report. The supplied July 2026 module descriptor remains the authority for official assessment and delivery requirements; this review does not amend it. Earlier chapter files were used only to identify changes and, explicitly for the missing Chapter 10 companion, to assess the available earlier checkpoint.
