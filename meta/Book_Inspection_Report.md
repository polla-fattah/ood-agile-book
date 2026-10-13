# Book Inspection Report: Chapters 1 to 15

*OO Development and Agile Practices*  
Inspection date: 14 October 2026. Scope: the 15 chapters in `content/book/chapter-01.md` to `chapter-15.md` (about 105,000 words), checked against their companions, Appendix D, the Curriculum page and the module's external sources. Nothing in the chapters was edited during the inspection; every finding below is a recommendation for the author to accept or reject.

## 0. Status after the fixes (14 October 2026, later the same day)

Fixes were applied in the order of Section 7. After them, the full site builds with no error or warning, the reference scripts report no broken `Section`, `Figure`, `Chapter`, appendix or companion-section reference, all 31 Mermaid diagrams render, and the affected lecture decks measure with no overflowing slide. Nothing is committed.

| Item | Done |
|---|---|
| 1. 136 -> 159 (High) | Fixed in `chapter-12.md` (book), `companion/chapter-12.md` (three places) and the Chapter 12 deck. |
| 2. Cross-document inconsistencies | Figure 10.1 now draws Presentation -> Domain and Bootstrap -> Domain and its caption names what is not permitted (deck figure redrawn to match). Chapter 10 now teaches CCP, CRP, REP, ADP, SDP and SAP by name, with a new subsection on abstractness, so the Curriculum page is correct (deck gained two slides). Chapter 13 companion: version 0.13.1 and 203/26/3 throughout; Chapter 14 companion and book: 0.13.1. |
| 3. Figures | Numbered captions added to Chapters 4, 7 and 12; Figure 12.1 now plots all eleven days and its caption identifies both lines; Figure 13.1 draws the two outside boxes with dashed borders; Chapter 3 gained Figure 3.1 (Sprint events) and Figure 3.2 (the board and its limit). |
| 4. Over-packed sections | 5.1 reordered (rule and stages first, evidence gathering last, five analyser terms defined). 7.4 retitled and bridged. 10.4 split: 10.4 "Dependency direction and its check", new 10.5 "Package design: cohesion, coupling and stability" (later sections renumbered 10.6 to 10.13). 12.7 given a bridge and the chapter description updated. 14.3 split: 14.3 "Documents, decision records and release notes", new 14.4 "Keeping the evidence true: rehearsal and traceability" (later sections renumbered 14.5 to 14.11). Section references in the other chapters, Appendices D, E and C, the companions and the decks were updated. 9.12 shortened, numbered and given a stable anchor. 6.3, 4.2 and the Chapter 8 description retitled; repeated Chapter 8 subheadings now name their pattern. |
| 5. Sources | Chapter 10 [9] now cites Martin's own 2000 paper instead of Wikipedia; the paper's text was extracted and it contains the definitions used (Ca, Ce, I, A and all six package principles). Chapter 6 [1] is the same paper, now confirmed to state ISP and DIP, so the "could not be machine-checked" caveat was removed. Six moved addresses updated (all return 200). Gamma et al. now carries the year 1994. |
| 6. Long lists | Milestone checklists (Chapters 7, 10, 13) and the "Acceptance conditions" paragraphs (Chapters 8, 9, 10, 11, 13, 14, 15) are now numbered or bulleted lists. Chapter 7's checklist now has the same eight items, in the same order, as its table (and its deck). |
| Also done | Chapter 2 now prints the extracted `confirmationFor` method; Chapter 1 Section 1.6 paragraph shortened; Chapter 4, 13 and 15 gained short glosses for CI tooling terms, HTTP and Maven; Chapter 11's "five appears twice" sentence made exact (and its deck); heading conventions made uniform ("Opening scenario", "Summary and next chapter", "Concept questions", "Applied diagnosis", "Task A:" style labels); two long headings shortened. |

**Not done (left as optional, Low severity):** reorder Chapter 1 Sections 1.5 and 1.6; a slicing pointer in Chapter 3; multiplicities in Figure 5.1; citing the ten sources that are listed but not cited by number; mentioning IDE refactorings in Chapter 11; moving the Quiz 1 and Quiz 2 pointers (Chapters 6 and 11); shortening the repeated data-backed-collaborator passage in Chapters 8 and 10; a Little's Law note in Chapter 12 (left out on purpose: the synthetic history is not a stable system, so the relation would not hold on its own table).

The findings below are kept as written during the inspection, so section numbers in them (for example 10.4, 14.3, 7.4) refer to the numbering before the fixes.

## 1. How the inspection was done

| Method | What it covered |
|---|---|
| Close reading of all 15 chapters, in order | Criteria 1 to 5, 8, 9, 10; every section, table, figure caption and exercise. |
| Scripted checks over the whole book | Every heading (length, numbering, duplicates); every `Section X.Y`, `Figure N.M`, `Chapter N` and appendix reference; every reference to a companion section; the citation numbers in the text against each source list. |
| Re-computation of every worked number | Chapter 1 and 5 tables; Chapter 3 acceptance cases; Chapter 4 capacity arithmetic; Chapter 10 instability table; Chapter 11 fine table; Chapter 12 issue history (scope, completed, WIP, lead, cycle, wait, ages, velocity); Chapter 13 and 14 test counts and file counts; Chapter 15 fault counts. |
| External references | All 122 distinct URLs were requested (status check only, nothing saved). The three GitHub Actions versions used in the workflow, and the PMD 7.28.0 release and its date, were checked on the project pages. For seven sources the page text was also searched for the phrases the chapter relies on (Kanban Guide, Scrum Guide, GitHub Copilot card, Keep a Changelog, Oracle `HttpRequest.Builder`, Fowler's Technical Debt, arXiv 2406.10279): all seven contain them. |
| Diagrams | All 29 Mermaid diagrams were opened on the built book pages and checked for rendering errors, then read against their captions and the text. |
| Readability statistics | Sentence and paragraph length in every chapter, to locate the hardest passages objectively. |

**Not done:** the companion Java code was not re-run in this inspection (earlier sessions ran it); the books cited (Martin 2002, Fowler 2018, Feathers 2004, Gamma et al. 1994, Beck 2002, Evans 2004, Humble and Farley 2010, Forsgren et al. 2018, Rubin 2012) were not available to read, so their pages cannot be confirmed; an external URL that returns "200" shows that a page exists, not that it supports the sentence that cites it (only the seven sources named above were searched for their wording). Where I could judge a claim from what I know of the source (the Scrum Guide 2020, the Kanban Guide 2025, the Liskov and Wing paper, the arXiv abstract) I did, and I say so in the chapter notes.

## 2. Verdict in one table

Rating scale: **Strong** (no action needed), **Good** (small fixes), **Needs work** (a real problem that a reader would hit).

| # | Criterion | Rating | Evidence in one line |
|---|---|---|---|
| 1 | Understandability | **Strong** | Mean sentence 13.5 to 17.7 words, median 13 to 16; only 56 sentences over 40 words in 105,000 words. The longest (60 to 119 words) are the milestone checklists and "Acceptance conditions" written as one sentence (Chapters 7, 10, 11, 13, 14, 15). Chapters 13 and 14 are the densest (mean 17.5 words; 6 and 14 sentences over 40). |
| 2 | Not jumping subjects | **Good** | The running example and the "Opening problem ... Summary and next chapter" frame keep the thread. Nine places change subject without a bridge (Section 3, item 5, and the chapter tables). |
| 3 | Comprehensiveness | **Strong** | Every chapter delivers what its learning outcomes promise, states its scope limits, and defers explicitly. The gaps found are small (Chapter 2 does not show the extracted method; Chapter 10 does not teach REP and SAP although the Curriculum page says it does; Chapter 3 has no figure). |
| 4 | Correct examples and explanations | **Good** | I found no wrong teaching claim. Every recomputed number agrees with its table. One real inconsistency between chapters (Chapter 12 says the Chapter 11 checkpoint has 136 tests; Appendix D and Chapters 11, 13, 14 say 159), plus a few smaller ones in the companions. |
| 5 | Correct references to other points in the book | **Good** | 0 broken `Section`, `Figure`, `Chapter`, appendix or companion-section references across 15 chapters; all citation numbers resolve. Problems are consistency, not breakage (Chapter 7 checklist versus its table; the Curriculum page versus Chapter 10; two companions disagree with their chapters). |
| 6 | Real, available external references | **Strong** | 122 of 122 URLs resolve; five GitHub documentation pages have moved and redirect. Two sources are weak for the weight they carry (Wikipedia in Chapter 10; a scanned PDF the author could not read in Chapter 6). Ten listed sources are never cited by number in the text. |
| 7 | Correct diagrams, sufficiently explained | **Good** | All 29 diagrams render and are explained in the text. Three have no figure number (Chapters 4, 7, 12); Figure 10.1 contradicts the table it illustrates; Figure 13.1's caption describes styling the drawing lacks; Chapter 3 has no diagram. |
| 8 | Titles | **Good** | Chapter titles are academic and well chosen. Seven section titles under-describe their content (6.3, 4.2, 7.4, 10.4, 12 (chapter), 14.3, 8 description). Heading conventions drift between chapters (Section 5). |
| 9 | Fluent narrative | **Strong** | Each chapter picks up its opening scenario, ends by naming the next chapter, and reuses earlier results by name. The one repeated device that tires is the "data-backed collaborator" itinerary, restated in Chapters 1, 6, 8 and 10. |
| 10 | Not assuming too much | **Good** | Terms are defined at first use almost everywhere. Hot spots: Chapter 1 Section 1.6; Chapter 5 Section 5.1 (PMD metrics); Chapter 4 Section 4.6 (CI tooling); Chapter 13 Section 13.2 (HTTP); Chapter 15 Section 15.7 (Maven terms). |

## 3. Priorities

### High (fix before the book is used again)

1. **Chapter 12 quotes the wrong test count.** `content/book/chapter-12.md`, Section 12.6: "136 passing tests in the Chapter 11 checkpoint". The Chapter 11 checkpoint has **159** invocations (Appendix D, Chapter 11 companion, Chapters 13 and 14). Same error twice in `content/companion/chapter-12.md` (the "136-test Chapter 11 suite" and "136 JUnit invocations") and once in the lecture deck `content/slides/chapter-12.md` (line 621).

### Medium (a reader will notice)

2. **Figure 10.1 contradicts its table.** Caption: "a missing arrow means the reference is not permitted", yet the Section 10.2 matrix permits Presentation -> Domain and Bootstrap -> every package, and the figure has neither arrow. Add the arrows or amend the caption. The deck for Chapter 10 copies the omission.
3. **The Curriculum page promises package principles the chapter does not teach.** `content/topics/_index.md` line 84 lists REP, CRP, CCP, ADP, SDP, SAP; Chapter 10 teaches the ideas behind CCP, CRP, ADP and the stable-dependencies idea without the abbreviations, and does not teach REP or SAP (abstractness).
4. **Two companions disagree with their chapters.** Chapter 13 companion: version "0.13.0" (lines 126 and 1924) against 0.13.1 in its own POM hunk and Appendix D; its B1 model answer gives 202/25/3 invocations against 203/26/3 in its expected output and in the book. Chapter 14 companion line 158: "from 0.13.0" against 0.13.1.
5. **Sections that change subject without saying so.** Chapter 10 Section 10.4 (about 2,500 words: direction, jdeps, cohesion, coupling, stability, placement worked example, Ports and Adapters); Chapter 14 Section 14.3 (documents, decision records, a flag-removal rehearsal, traceability, release notes); Chapter 7 Section 7.4 (boundaries and clocks, then a new LoanService feature); Chapter 5 Section 5.1 (change pressures, then a tooling lab, then the staff rule); Chapter 12 Section 12.7 (a full requirement contract inside a metrics chapter).
6. **Weak sources for central claims.** Chapter 10 [9] (Wikipedia) supports the definitions of afferent coupling, efferent coupling and instability; Chapter 6 [1] (a scanned PDF) supports ISP and DIP and the chapter itself says its text "could not be machine-checked". Replace with Martin's own articles or the module's required book with a chapter number.
7. **Chapter 2 never shows the refactoring it asks for.** Section 2.4 says the confirmation expression is extracted into `confirmationFor` but the chapter does not print the helper; the central teaching artefact of the practical is only in the companion.
8. **Figures that cannot be cited or are not self-explanatory.** Chapters 4, 7 and 12 have a diagram with no "Figure N.M" caption; Figure 12 (burn-up) has two unlabelled lines on a beta Mermaid chart type, sampled on five of eleven days; Figure 13.1's caption says "outer boxes" but all boxes look identical; Chapter 3 has no diagram although it explains a cycle of events and a board.
9. **Mixed-up assumptions in one place each.** Chapter 1 Section 1.6 last paragraph (itinerary of five later chapters with unexplained terms); Chapter 5 Section 5.1 (cyclomatic complexity, NPath, WOC/NOPA/NOAM/WMC undefined); Chapter 13 Section 13.2 (no HTTP primer); Chapter 4 Section 4.6 (Temurin, YAML, exit status).
10. **Milestone checklists and "Acceptance conditions" as single long sentences** (Chapters 7, 10, 13, plus the "Acceptance conditions" paragraphs of 11, 13, 14, 15). They contain the most important instructions in the chapter and are the hardest sentences in the book (up to 119 words). Set them as numbered or bulleted lists.

### Low (polish)

See the per-chapter tables in Section 6 and the heading conventions in Section 5.

## 4. What is very good (keep it)

- **One teaching device, used consistently:** *claim -> evidence -> what the evidence does not show*. Chapters 1, 4, 7, 12, 13, 14, 15 all end up building the same habit, and the AI activities apply it with constructed fixtures labelled as such.
- **Honest scope statements.** Nearly every chapter says what its checkpoint does not do (no persistence, sequential only, no hosted CI run, no Java 17 run), and says what is a teaching rule rather than a university policy.
- **Counterexamples before definitions.** Chapter 5 (`PositiveOnlyHistory`), Chapter 6 (an interface-typed field that still constructs its collaborator), Chapter 11 (the fine table with three suspected defects), Chapter 13 (the 1,700 ms stalled body), Chapter 14 (a one-line change that passes every unit test).
- **Numbers that reconcile.** The test counts (34, 5, 44, 28, 35, 63, 107, 121, 159, 232, 235), the instability table, the capacity arithmetic and the issue history all recompute exactly.
- **Heading structure.** All chapters have continuous section numbering; no gaps or repeats; every cross-reference to a numbered section resolves.

## 5. Cross-cutting findings

### 5.1 Heading conventions drift between chapters (low, but visible in the table of contents)

| Convention | Chapters | Recommendation |
|---|---|---|
| "Opening scenario" (1 to 7, 11) versus "Opening problem" (8 to 10, 12 to 15) | mixed | Choose one. |
| Summary: "1.11 Chapter summary", "2.12 ...", "3.13 ..." (numbered) versus "Summary and next chapter" (unnumbered, 4 to 14), "Summary and where to go next" (15) | mixed | Use "Summary and next chapter" everywhere (Chapter 15 may keep its variant). |
| "Diagnosis questions" (1 to 3) versus "Applied diagnosis" (4 to 15); "Concept questions" versus "Short concept questions" (4 to 7) | mixed | Use "Concept questions" / "Applied diagnosis". |
| Task and activity headings without punctuation ("Task A Read and explain", "Activity 1A Evaluate ...", "Part A Understand the request") | Chapters 1, 2, 3 | Add a colon after the label. |
| Quiz revision pointers placed after the transfer challenge (6.13, 11.11), midterm practice (7.12), "Appendix E reading checkpoint" (unnumbered, Chapter 9) | 6, 7, 9, 11 | Move assessment aids to one predictable place (end of chapter, before the summary) and number them. |
| Repeated subheading "Test, trade-off and non-use case" | Chapter 8 (three times) | Prefix with the pattern name. |

### 5.2 Repeated roadmap text

The "data-backed collaborator" paragraph (the equipment directory and the chapters that develop it) is restated in Chapters 1, 6, 8 and 10. It is consistent each time, but a reader meets the same sentence four times. Keep the full version in Chapter 1 Section 1.6 (and shorten it, see 1.1 below) and refer to it with one clause elsewhere.

### 5.3 Sources listed but not cited by number in the text

Chapter 7 [7] (Maven Compiler Plugin), Chapter 8 [6] (JUnit), Chapter 9 [5] (JUnit), Chapter 11 [10], [11], [12] (ChronoUnit, Period, JUnit), Chapter 12 [6] (Duration), Chapter 13 [10] (JUnit), Chapter 14 [9] (Hodgson, Feature Toggles), Chapter 15 [8]. They are described in the source list, so they are not wrong, but a bracketed citation at the point of use would make the support for each claim checkable.

### 5.4 GitHub documentation addresses that have moved (all still work through a redirect)

| Chapter(s) | Old address (path) | Now redirects to |
|---|---|---|
| 13 | `/en/actions/writing-workflows/workflow-syntax-for-github-actions` | `/en/actions/reference/workflows-and-actions/workflow-syntax` |
| 14, Appendix E | `.../why-are-my-contributions-not-showing-up-on-my-profile` | `/en/account-and-profile/how-tos/contribution-settings/troubleshooting-missing-contributions` |
| 14, Appendix E | `.../creating-a-commit-with-multiple-authors` | `/en/pull-requests/how-tos/commit-changes/creating-a-commit-with-multiple-authors` |
| 14, Appendix E | `.../about-pull-request-reviews` | `/en/pull-requests/reference/pull-request-reviews` |
| Appendix B | `.../about-pull-requests` | `/en/pull-requests/reference/pull-requests` |
| 10 | `domainlanguage.com/wp-content/uploads/...DDD_Reference_2015-03.pdf` | `www.domainlanguage.com/...` (same file) |

### 5.5 Things that were checked and are fine

- Week and quiz mapping: Chapter 2 = Week 1, ..., Chapter 14 = Week 13; Quiz 1 pointers cover Chapters 2 to 5 (Weeks 1 to 4); Quiz 2 pointers cover Chapters 6 to 10 (Weeks 5 to 9).
- Test-count arithmetic in Appendix D (35 -> 63 -> 107 -> 121 -> 159 -> 232 -> 235) matches the chapters.
- GitHub Actions versions used in the workflows (`checkout@v7`, `setup-java@v6`, `upload-artifact@v7`) exist and are the latest major versions; PMD 7.28.0 was released on 25 September 2026.
- The `--release 17` / `List.getFirst()` (Java 21) example in Chapter 15, `PrintStream.checkError()` stickiness in Chapter 6, `Map.copyOf` and `List.copyOf` semantics in Chapters 2, 6 and 10 are accurate.

## 6. Findings by chapter

Severity is Low, Medium or High; "OK" rows record something that was checked and found correct. Criterion numbers refer to the ten criteria in the request.


## Chapter 1: Developing Software That Can Change

**Overall:** the most reader-friendly chapter. One small class carries the whole argument; the Java is explained line by line; the evidence tables (1.2, 1.4) are good. The narrative is smooth up to 1.5. Findings are mostly about the final third.

| # | Criterion | Finding | Severity |
|---|---|---|---|
| 1.1 | 10 (assumes too much) / 2 | Section 1.6, last paragraph (the data-backed collaborator) is one very long paragraph that uses "adapter", "test double", "provider contract", "timeouts", "fallback-or-failure policy" and names five later chapters. None of these terms exist for a first-week reader. It is a roadmap, not an explanation. | Medium |
| 1.2 | 2 (jumping) | Section 1.5 (AI assistance) arrives right after testing and before the running example is introduced (1.6). The AI material is good, but the order is: change -> OO/iteration -> testing -> AI -> running example. Moving 1.6 (running example and vocabulary) before 1.5, or after the tasks, would let the AI activity use already-introduced vocabulary (borrower, reservation). | Low |
| 1.3 | 1 / 8 | Headings "Activity 1A Evaluate a candidate explanation" and "Task A Read and explain" have no punctuation separating label from title; the other chapters use a colon in some places and not in others. Pick one convention. | Low |
| 1.4 | 10 | Section 1.1 uses `final`, `public`, `&&` explained. The word "Boolean" and "method" are used without definition (the Prerequisites paragraph says methods and classes are assumed). Acceptable, but the keyword explanation sits after the code while the code is first shown without any lead-in. | Low |
| 1.5 | 3 (comprehensive) | The chapter promises to prepare for "iterative delivery" (1.3) but gives only two sentences on Agile principles and one diagram. That is deliberate (Chapter 3), and the text says so. No gap. | None |
| 1.6 | 5 (references) | "Core reading. Read Sections 1.1-1.8" but the tasks (1.9) and review questions (1.10) that the "Minimum required lab" depends on are outside the core range. Not wrong, but the reading route and the minimum lab point at different parts. | Low |
| 1.7 | 7 (diagram) | Figure 1.1 is explained in its caption and in the paragraph after it. Adequate. The diagram has a decision node but the caption does not name the two exits ("Yes -> demonstrate", "No -> inspect"); the reader must read the diagram. | Low |
| 1.8 | 4 (examples) | Checked: table in 1.1 matches the code (2,7 true; 3,7 false; 0,0 false; 0,8 false; -1,2 false). Acceptance examples in 1.4 match the staff rule (4 true, 5 false). Task B output `true / false` is correct. | OK |
| 1.9 | 6 (external references) | All 4 links resolve. Source 4 (GitHub Copilot card) is described as one vendor's account, not a general claim; this is handled honestly. | OK |
| 1.10 | 9 (narrative) | The opening scenario is picked up again in 1.1, 1.4 and the summary. The transition to Chapter 2 is present. | OK |

## Chapter 2: Object-Oriented Development Beyond Syntax

**Overall:** accurate and carefully hedged (immutability, `final`, `List.copyOf` limits are exactly right). The UML section is the best teaching material in the book: read, draw, check, spot the errors. The weakness is load: one chapter (8,490 words, the second longest of the book after Chapter 14) teaches objects, invariants, encapsulation, cohesion, composition, UML, Git review and AI.

| # | Criterion | Finding | Severity |
|---|---|---|---|
| 2.1 | 2 (jumping) / 9 | The chapter changes subject four times: objects and invariants (2.1-2.3) -> design vocabulary (2.4-2.5) -> a long notation section (2.6, about a third of the chapter) -> Git (2.7). Each switch is signposted by a heading but not by a bridging sentence. 2.6 opens with "A class diagram is a selective explanation" without saying why the notation arrives here (the midterm reason is stated only in the reading route). A two-sentence bridge at the start of 2.6 and 2.7 would fix the flow. | Medium |
| 2.2 | 3 / 4 | Section 2.4 promises "We will extract the confirmation expression into a private method named `confirmationFor`" but the chapter never shows the extracted method or the before/after diff; the reader must open the companion. The principal teaching point of the practical (a reviewable refactoring) is therefore invisible in the chapter. Showing the six-line helper and the call would cost little. | Medium |
| 2.3 | 10 (assumes too much) | 2.6 uses "navigable association", "multiplicity", "realisation", "dependency" in the outcomes before they are explained, but each is explained when first needed in the section. The "Reading the lines" rule (look at the far end) is clear and correct. No problem. | None |
| 2.4 | 7 (diagrams) | Figures 2.1-2.4 are correct against their descriptions. Checked: Fig 2.1 matches the code (Reservation shows no `LoanPeriod` attribute, only the line: the chapter's own "do not show it twice" rule). Fig 2.3 multiplicities match the six-step text. Fig 2.4 contains more than the five mistakes the text promises (attribute `-Locker locker` and a line; reversed multiplicity with a diamond on the wrong side; inheritance for "logs"; dependency on the concrete printer; solid line for realisation; missing multiplicity on the tool association): that is fine because the text says "at least five". | OK |
| 2.5 | 7 | Fig 2.1 does not show a `<<interface>>` box, yet the prose explains the guillemet label with it as the example; Figure 2.2 shows it. Readers meet the label before they see one. Minor. | Low |
| 2.6 | 5 (cross-references) | "Chapter 5 tests this claim with the Liskov Substitution Principle" is correct (Chapter 5 covers LSP). Appendix A/B pointers (A syntax; B.8 for the Git workflow) exist. Source 8 lists `git switch` but the chapter text never names it (it appears only in the companion). | Low |
| 2.7 | 4 | Statements checked: `==` on references; `final` field vs list mutation; `List.copyOf` unmodifiable snapshot (correct, and it throws on null elements, not mentioned, irrelevant here); `git diff` after staging is empty (correct); "Immutable" claim for `Reservation` requires all fields final and immutable types: true as described. | OK |
| 2.8 | 8 (titles) | "Practical activity: one checked design improvement" and "Git history, branches and review" are good. "2.6 UML class diagrams: reading, drawing and checking" is long but informative. | OK |
| 2.9 | 3 | Concurrency is mentioned as a limit twice ("sequential", "not thread-safe") with only a pointer to "later integration work". Chapter 13 notes concurrency as not addressed; the book never teaches it. That is a scope choice, but the opening claim in 2.2 that checking conflicts "prevents the demonstrated overlap" within sequential use is correctly bounded. | Low |
| 2.10 | 6 | All 10 sources resolve. Source 10 (Martin 2002) cannot be checked online and defers pages to Moodle; acceptable. | OK |

## Chapter 3: Agile Development and the Nature of Change

**Overall:** clear, honest about what is Scrum and what is a local convention (it repeatedly separates "Scrum Guide says" from "our teaching choice"), and the criteria/DoD distinction is well taught. The order of topics (uncertainty -> values -> iteration/increment -> Scrum -> Kanban -> stories -> criteria -> estimation) is natural.

| # | Criterion | Finding | Severity |
|---|---|---|---|
| 3.1 | 7 (diagrams) | The chapter has no figure at all, although it explains a cycle (Sprint with four events), a board with five columns and a WIP limit, and an artefact-to-commitment mapping. The five-column board and the "hypothetical later snapshot" in Part B are tables that a reader must mentally draw. A Scrum-events figure and a board figure would remove that effort (the slide deck now has them). | Medium |
| 3.2 | 10 | "Definition of Done" appears in 3.4 (artefact-commitment sentence) four sections before it is defined in 3.7. The sentence is correct, but a first-time reader cannot use it. Add "(defined in 3.7)" or one clause. | Low |
| 3.3 | 2 | The jump from 3.3 (iteration/increment) into 3.4 (full Scrum vocabulary) is abrupt: eight terms in one table. The paragraphs after the table are good, but a one-sentence reason for introducing the formal framework ("the course uses these words, so we need the precise meanings") is missing. | Low |
| 3.4 | 4 (accuracy) | Checked against the Scrum Guide 2020: Product Owner, Developers, Scrum Master accountabilities, Sprint <= one month, Daily Scrum 15 minutes, Sprint Review as a working session, Retrospective purpose: all correct. "The guide mentions neither user stories nor story points" is correct. Kanban Guide 2025: SLE as elapsed time plus probability: correct. | OK |
| 3.5 | 4 | The "85% within five working days" example is explicitly labelled an unvalidated hypothesis and deferred to Chapter 12. Good practice. | OK |
| 3.6 | 3 (comprehensive) | No treatment of splitting techniques (by workflow step, by rule, by data variation) although "Small" is an INVEST letter and Part A asks learners to refine US-02. The chapter says what a small story is but not how to make a story smaller. Chapter 4 ("slice features") covers it, and 3.3 points forward to Chapter 4 for planning only. Add a one-line pointer to the slicing section of Chapter 4. | Low |
| 3.7 | 5 | Cross-references checked: Chapter 4 (iteration plan, kickoff CI), Chapter 12 (flow measures, forecasting), Appendix C.2/C.3/C.4 (story card, acceptance example, DoD): all exist. | OK |
| 3.8 | 4 | AC-01..AC-05 agree with the Chapter 2 rules (three active, 1-7 days, adjacency allowed). The Given/When/Then example for AC-02 is consistent (B2 requests 21 Oct, overlapping 20-22). | OK |
| 3.9 | 6 | All 8 sources resolve (INVEST and Jeffries pages are blog/personal sites but are the primary sources and are described as such). | OK |
| 3.10 | 8 | Heading "3.9 AI in practice: challenge a story without inventing policy" is good: it states the lesson. | OK |

## Chapter 4: From Requirements to an Iteration

**Overall:** a strong planning chapter. It is unusually honest about what is existing, proposed and missing, and the capacity arithmetic is correct (6+6+5+5=22, minus 4 = 18; 2+4+3+3+2=14, 4 spare). It combines two different subjects, though: project planning (4.1-4.5) and a build/CI starter (4.6), which are connected by the kickoff milestone but not by a narrative bridge.

| # | Criterion | Finding | Severity |
|---|---|---|---|
| 4.1 | 7 (diagrams) / 5 | The only diagram (the review-and-CI flowchart in 4.5) has no numbered caption, unlike every other figure in the book (Figure N.M). It is explained by one paragraph below it, so the explanation is adequate, but the figure cannot be referred to, and the text says "This diagram" instead. Add "Figure 4.1". | Low |
| 4.2 | 2 / 9 | Moving from 4.5 (team agreement, review) to 4.6 (a shell script, `javac --release 17`, line endings, a hosted workflow) is a hard jump. The first sentence of 4.6 ("Continuous integration needs a check that can run without relying on one developer's open IDE") is a good start but does not say that the whole chapter has been about preparing for this. A bridge sentence at the end of 4.5 would help. | Low |
| 4.3 | 10 (assumes too much) | 4.6 uses terms with no explanation: "Temurin" (a JDK distribution), "YAML", "Bash", "WSL", "exit status", "nonzero result", "line endings/CRLF". Some appear in Appendix B (tools), but 4.6 does not point there. A "see Appendix B" pointer in the prerequisites would close the gap; Windows readers are told how to run the script, which is helpful. | Medium |
| 4.4 | 4 | "Chapter 3 proposed the following order" (4.3) lists six items, but Chapter 3 shows a three-item backlog; US-03, US-04 and US-05 are the learner's extension in Chapter 3 Part A. The sentence should say "Chapter 3's order, extended by the three items its Part A asks you to add". | Low |
| 4.5 | 8 (titles) | "4.2 Domain assumptions and wireframes": the section is about wireframes and worked examples; domain assumptions were handled in 4.1 (scope table, assumptions). Rename to "Wireframes and worked examples". | Low |
| 4.6 | 3 / 4 | The Arrange-Act-Assert explanation is limited to reading one excerpt, with a forward pointer to Chapter 7. That is proportionate. The AC-02 excerpt is consistent with the Chapter 3 criterion. | OK |
| 4.7 | 6 (external) | All 7 sources resolve. The three GitHub action versions in the supplied workflow exist and are current: `actions/checkout@v7`, `actions/setup-java@v6`, `actions/upload-artifact@v7` (checked by HTTP status, not by running the workflow). Chapter 14 (KI-12) correctly says no hosted run was made. | OK |
| 4.8 | 5 | Forward references (Chapter 5, 7, 12, 13, Appendix C.6-C.9) all point to existing places. "34 checks" agrees with Chapter 2 Part A. | OK |
| 4.9 | 9 | The sequence vision -> wireframe -> slice -> plan -> agreement -> CI -> milestone evidence is logical and each part uses the previous output. | OK |

## Chapter 5: Responsibilities, Extension, and Substitutability

**Overall:** the best-argued design chapter. It keeps asking "against which change?", refuses to call a switch statement closed, separates refactoring (Stage A) from feature (Stage B), and the LSP section uses a proper counterexample with three variants. The contract table in 5.4 and the deliberate settlement of Chapter 1's negative-count question are model teaching.

| # | Criterion | Finding | Severity |
|---|---|---|---|
| 5.1 | 10 (assumes too much) / 2 | Section 5.1 front-loads a heavy tooling block ("Ask the tools, then ask the code": `javac -Xlint:all`, a manual smell review, and a PMD run with SHA-256 verification). It uses "cyclomatic complexity", "cognitive complexity", "NPath", "God class", "Data class", "WOC, NOPA, NOAM, WMC" before the reader has met SRP, and none is defined. A reader cannot interpret the PMD output block, only copy it. Either define cyclomatic complexity in one sentence (number of independent paths) and drop the Data-class metrics line, or move the PMD lab after 5.2-5.3 where SRP is explained. | Medium |
| 5.2 | 2 (jumping) | The section titled "Change pressure in a reservation service" ends up containing three subjects (change pressures, the analyser lab, the new staff-rule table plus stage definitions). The staff table and "Define success for each stage" are the real framing for the chapter and are buried after the PMD discussion. Reordering to: pressures -> staff rule -> stage definitions -> (optional) tooling would give a cleaner narrative. | Medium |
| 5.3 | 4 (accuracy) | Verified: the staff/student table, the policy contract, the claim that the cyclomatic complexity stays at 12 after both stages (the chapter explains why), `@Override` semantics (JLS 9.6.4.4), Liskov-Wing 1994 citation (TOPLAS 16(6) 1811-1841 is correct), Martin's 2014 blog posts, Fowler 2018 2nd ed. "Bad Smells in Code". PMD 7.28.0 exists and was published on 25 September 2026 (checked via the release page). | OK |
| 5.4 | 7 (diagrams) | Figure 5.1 and its two-paragraph explanation are adequate and unusually careful (it explains why the two dashed arrows are drawn and when they should disappear). The mermaid class diagram lists `ConfirmationFormatter` with an association from the coordinator but no multiplicities, whereas Chapter 2 taught multiplicities for associations. Consistency would suggest "1" at each end; omitted multiplicities should be called out as a simplification. | Low |
| 5.5 | 10 | Terms "precondition", "postcondition", "invariant" are defined in one sentence each in 5.4 and applied immediately. Good. "Overload" (5.3) is used without a gloss. | Low |
| 5.6 | 5 | Forward and backward references verified: Chapter 1's negative-count remark (exists, Section 1.1), Chapter 2 notation table (exists), Chapter 6 for DIP/ISP/injection, Chapter 7, Chapter 10 (package), Chapter 11 (smells). Core reading says "Sections 5.1-5.7", correct. | OK |
| 5.7 | 3 (comprehensive) | SOLID is split across Chapters 5 and 6 and the title says so ("first SOLID chapter"). Nothing missing within scope. The "make this SOLID" AI fixture mixes seven problems; each maps to a section. | OK |
| 5.8 | 8 | Title "Responsibilities, Extension, and Substitutability" is academic and accurate. Section titles "5.4 Behavioural contracts", "5.7 Avoiding premature abstraction" are good. "5.1 Change pressure in a reservation service" under-describes its content (see 5.2 above). | Low |

## Chapter 6: Interfaces, Dependencies, and Composition

**Overall:** the central confusion (an interface-typed field is not dependency inversion) is demonstrated with a concrete "coupled version" and then undone, which is exactly how the topic should be taught. The "DI without DIP" and "DIP without DI" paragraphs are excellent. Figures 6.1 and 6.2 are well chosen as two different views, and the text says explicitly not to read event order from either.

| # | Criterion | Finding | Severity |
|---|---|---|---|
| 6.1 | 8 (titles) | "6.3 Policy and implementation dependencies" does not describe its content. The section is mostly about who owns which decision, the partial-success rule after notification failure, `PrintStream.checkError()`, and the acceptance-example table. Only the first table is about "policy and implementation". Suggest "6.3 Who decides what, and what happens when notification fails". | Medium |
| 6.2 | 9 (narrative) | The last paragraph of 6.6 (about 230 words) repeats itself: it says twice that the lab uses the educational container, not a library container, and twice that a library container does the same three jobs with more machinery. Cutting it to three sentences would remove the repetition. | Low |
| 6.3 | 6 (external references) | Source [1] (Martin 2000, hosted as a scanned PDF at Turku) is described in the chapter itself as one whose text "could not be machine-checked". The chapter relies on it for ISP and DIP in 6.2 and 6.4. The honesty is good, but a source the author could not read is a weak support; the module's required book [8] or Martin's own web articles on ISP/DIP would be verifiable replacements. | Medium |
| 6.4 | 10 | The preview of `BorrowerDirectory` uses `Optional`, `@FunctionalInterface` and "outage as exception" with no gloss. The text flags it as a preview and explains the three promises in prose, which is adequate; a reader who has not met `Optional` still has to infer it. | Low |
| 6.5 | 5 (cross-references) | Verified: Figure 5.1 (exists, compared against Figure 6.1), Chapter 8 (BorrowerDirectory adapter is built there), Chapter 7 (test doubles), Chapter 10 (packages). The Quiz 1 pointers in 6.13 list Chapters 2-5, matching "Weeks 1-4". | OK |
| 6.6 | 7 (diagrams) | Figure 6.1 is correct against the text (every "creates" arrow starts at `ReservationApplication`; the coordinator's outgoing arrows end at roles except the concrete formatter, which the text justifies). The caption admits the map is drawn as one association, which is honest. Figure 6.2 is a flowchart with dotted and solid arrows explained in its caption. | OK |
| 6.7 | 2 | 6.13 (Quiz 1 revision pointers) sits between the transfer challenge and the summary. A study aid that is about Chapters 2-5 is surprising in a Chapter 6 flow and may be missed; consider moving it to Appendix D or making it a short box at the very start of the chapter. | Low |
| 6.8 | 4 | `PrintStream.checkError()` stickiness, `Map.copyOf` shallow/unmodifiable semantics, Spring's definition of a bean: all accurate. | OK |

## Chapter 7: Testing as a Design Practice

**Overall:** the central teaching is strong: expected values must come from the requirement, not from the code; a red result must be the intended failure; a mock must not replace the subject; a surviving fault is information. The honest handling of version facts (Mockito's "current" page is labelled 2.2.7; the dynamic-agent warning) is rare in textbooks. The chapter is, however, overloaded: TDD, test anatomy, boundaries, a new feature (LoanService), five kinds of test double, Mockito, mutation checks, Milestone 2 and a five-task midterm set.

| # | Criterion | Finding | Severity |
|---|---|---|---|
| 7.1 | 2 (jumping) / 8 (titles) | Section 7.4 is titled "Boundaries and deterministic tests" but its second half introduces a new feature, the `LoanService` (checkout/return, a `Loan` record, a table of seven rules, and the "Do not invent lifecycle rules silently" subsection). A reader following the testing thread meets a feature specification mid-section. Give the loan flow its own section ("7.5 A bounded lending flow to test") or move it before 7.4. | Medium |
| 7.2 | 7 (diagrams) | The red-green-refactor flowchart in 7.3 has no numbered caption ("Figure 7.1") and is introduced by a lead-in sentence only. Its explanation is good (the diamond states that only the intended failure counts), but the figure cannot be cited. | Low |
| 7.3 | 10 (assumes too much) | The paragraph on the dynamic agent (7.5) mentions "interface-only proxy mock maker", "ByteBuddy agent", "dynamic proxies" and the JVM flag `-XX:+EnableDynamicAgentLoading`. These are accurate and useful for someone who hits the warning, but they are JVM internals that the chapter does not otherwise need; they interrupt the explanation of why a mock is used. Move to a "Practical warning" box or to the companion (Appendix B has the toolchain). | Low |
| 7.4 | 9 (narrative) | The paragraph in 7.1 that explains why the "add a temporary record and remove it" implementation cannot be caught by a sequential test, and why a separate identifier-consumption example overlaps the unchanged-records check, is correct but requires three re-reads. It is the hardest paragraph in the chapter. Consider splitting into two sentences per idea and giving the "reject it by reading" conclusion first. | Medium |
| 7.5 | 5 (cross-references) | "Section 7.8 explains each item" of the seven-item Milestone 2 checklist at the top, but the table in 7.8 has eight rows (it adds "OO/SOLID rationale") and orders them differently. Make the two lists identical. Also, line 40 begins with a stray leading space (" The companion for this chapter...") after an apparent paragraph break; it renders as a continuation of the Optional-extension paragraph. | Low |
| 7.6 | 4 | Counts agree with earlier chapters (34 + 5 + 44 + 28 internal checks, four JUnit wrapper cases). The sixteen-fault arithmetic is consistent (14 + 1 + 1). The zone example (19 Oct 22:30 UTC in Asia/Baghdad = 20 Oct) is correct (UTC+3). | OK |
| 7.7 | 6 | 10 sources, all resolve. The chapter itself warns that the hosted Mockito "current" page is version 2.2.7 and pins 5.20.0; this is the correct way to cite a moving target. | OK |
| 7.8 | 3 (comprehensive) | The chapter promises "red-green-refactor" and delivers a real worked cycle, test doubles with the Meszaros vocabulary, time control and mutation. It does not discuss test naming conventions beyond one paragraph or test pyramid/levels (deferred to Chapter 13, which says so). Appropriate. | OK |
| 7.9 | 4 | The Task 2 `OverdueReminder` snippet has at least five deliberate flaws (static clock, direct `new MailClient`, hard-coded host and port, `System.out`, mixed responsibilities). Good midterm-style exercise; it is explicitly separate from the project. | OK |

## Chapter 8: Creating and Connecting Objects

**Overall:** the chapter's thesis ("which responsibility needs a boundary, and what is the smallest design that makes it clear?") is applied honestly: only one of the five patterns (Adapter) enters the cumulative project, and each pattern section ends with "Test, trade-off and non-use case". The comparison with the simple alternatives in 8.7 is exactly what an architecture course should teach. The mapping table in 8.5 and the rule "an outage is never absence" are clear and correct.

| # | Criterion | Finding | Severity |
|---|---|---|---|
| 8.1 | 2 (jumping) | Five patterns in one chapter, four of them in isolated examples (export job, receipt family, report builder, decorated sender) with new vocabulary each, then back to the lending system for the Adapter. A reader loses the thread twice. The chapter says this up front (core vs working-knowledge reading), which mitigates it. An explicit sentence at the start of 8.2 ("the next four sections use small separate examples; the lending project returns in 8.5") would help. | Low |
| 8.2 | 8 (titles) | The front-matter description says "Creational patterns: Factory Method, Builder, and dependency injection seams", but the chapter also covers Abstract Factory, Adapter and Decorator and no dependency injection seams as such. The chapter title "Creating and Connecting Objects" is accurate (connecting = Adapter, Decorator). Fix the description to match. Three sections carry the identical subheading "Test, trade-off and non-use case" (8.2, 8.3? 8.4, 8.6): it is a consistent device but makes in-page navigation ambiguous; prefix with the pattern name. | Low |
| 8.3 | 9 (narrative) | The paragraph "The directory is the book's data-backed collaborator" lists the same five-chapter itinerary that Chapter 1 and Chapter 6 gave. Repeating the plan three times is consistent but long; here it could be reduced to "(see Section 1.6)". | Low |
| 8.4 | 7 (diagrams) | Figure 8.1 (class diagram) is explained in the paragraph below it, including what `#`, `<<abstract>>` and the dashed arrow mean. Figure 8.2 (sequence diagram) is introduced with a full paragraph defining participants, lifelines, `alt` frames and notes, because it is the first sequence diagram in the book. This is exactly the right amount of sufficient explanation. The caption admits the malformed-data case is omitted. | OK |
| 8.5 | 4 (accuracy) | Verified against the literature: Factory Method (creation hook in an inherited workflow) vs simple factory; Abstract Factory (related product roles); the Builder discussion states that a fluent builder is a variant and that GoF's Director is not implemented; Adapter as object adapter; Decorator order table (audit outside retry: `attempt, sent`; retry outside audit: `attempt, failed, attempt, sent`) is correct for a delegate that fails once. | OK |
| 8.6 | 10 | 8.2 uses "protected hook", "abstract class", "lambda", "workflow inheritance"; 8.3 "product roles", 8.4 "staged construction". Each is explained in the surrounding paragraph at its first use. Reasonable for readers who have done Chapters 5-7. | OK |
| 8.7 | 5 | Cross-references: Chapter 6 (`ReservationApplication.create(sender)`, notification contract: one attempt, no retry) agrees; Chapter 13 (timeouts) agrees; Chapter 10 (application structure) agrees. "63-invocation baseline" in the reading route should be checked against Appendix D (see the cross-chapter checks section). | Check |
| 8.8 | 6 | 7 sources. The two InformIT articles are publisher excerpts, not the book itself, and are described as excerpts. Gamma et al. is cited without year in the list; add 1994. | Low |

## Chapter 9: Designing Changing Behaviour

**Overall:** very good. The opening separates three requests that look alike but vary for different reasons, and the four-row "four questions" table (which rule? which action is legal now? who reacts? what request object?) is the clearest statement of why Strategy, State, Observer and Command differ that appears in the book. The transition table, the 20-row test (5 permitted + 15 rejected) and the distinct treatment of partial failure are all correct and checkable.

| # | Criterion | Finding | Severity |
|---|---|---|---|
| 9.1 | 2 (jumping) / 9 | The chapter ends with an unnumbered section "Appendix E reading checkpoint" about the individual critical book review due in Week 8. It follows the transfer challenge and precedes the summary, so the pattern narrative is interrupted by assessment logistics, and the same reminder already appears in the "Reading reminder" paragraph at the top. Keep the top reminder (it has the link) and move the longer guidance to Appendix E, or number it as a section (9.12) and place it after the summary. | Medium |
| 9.2 | 7 (diagrams) | Figures 9.1 (state diagram), 9.2 (two implementations), 9.3 (observer sequence diagram) are all correct and each introduces its notation in prose (state, transition, `[*]`, guard; realisation arrows; exception on a dashed return). One small gap: the state diagram explanation says "a state with no outgoing arrow, such as RETURNED" but CANCELLED is equally terminal; Mermaid does not draw an end marker. Mention both. | Low |
| 9.3 | 4 (accuracy) | Verified: 5 statuses x 4 actions = 20 rows, with 5 permitted transitions (REQUESTED: confirm, cancel; CONFIRMED: check out, cancel; ON_LOAN: return) and 15 rejections. `phase = phase.cancel()` leaves the phase unchanged when the call throws: correct. `Throwable.addSuppressed` semantics correct. | OK |
| 9.4 | 8 (titles) | "Designing Changing Behaviour" is grammatical but reads awkwardly; "Designing for Changing Behaviour" or "Varying Behaviour with Patterns" would be clearer. Section titles ("9.3 State and transitions", "9.5 Command") are good. | Low |
| 9.5 | 3 (comprehensive) | Observer is explained with a custom synchronous publisher and a pointer to `PropertyChangeSupport`, but there is no mention that Java's old `java.util.Observable` is deprecated, a common first search result for students. One sentence would pre-empt copying it. | Low |
| 9.6 | 6 | 6 sources resolve. Gamma et al. appears without a year (also in Chapter 8): add 1994 for citation consistency. | Low |
| 9.7 | 5 | Anchor `#appendix-e-reading-checkpoint` exists (the heading is at the end) and the `relref "appendix-e"` resolves (site build succeeded). Chapter 8 (directory adapter, `DirectoryReservationService`) and Chapter 10 pointers are correct. | OK |

## Chapter 10: From Classes to Application Structure

**Overall:** technically the most rigorous chapter. It separates source dependencies from runtime calls, ties every rule to a compiled check (`jdeps`), reports instability with explicit counting rules, and uses a worked rejection (Option B for `NotificationException`) to show that the direction and cycle checks catch what the ratios do not. The instability table was recomputed and is correct (e.g. 3/(14+3) = 0.18; 4/(9+4) = 0.31; 1/(2+1) = 0.33).

| # | Criterion | Finding | Severity |
|---|---|---|---|
| 10.1 | 7 (diagrams) / 4 | **Figure 10.1 contradicts the table it illustrates.** The caption says "A missing arrow means the reference is not permitted", but the matrix in 10.2 permits `presentation -> domain` and `bootstrap -> every package` (including `domain`), and Figure 10.1 draws neither arrow. A reader who trusts the caption would conclude that presentation may not use domain types, which the checkpoint does. Fix by adding the two arrows, or by amending the caption ("arrows from Bootstrap and Presentation to Domain are omitted for readability; the table in 10.2 is authoritative"). The slide deck for this chapter copies the same omission and should be corrected together. | Medium |
| 10.2 | 2 (jumping) / 8 (titles) | Section 10.4 is titled "Dependency direction and package design" and is about 2,500 words: it contains dependency direction, a sequence diagram, the `jdeps` check, package cohesion, coupling, stability with a metrics table, a worked placement comparison and an optional Ports and Adapters section. The title names two things, the section contains at least five. Split into "10.4 Dependency direction and its check" and "10.5 Package design: cohesion, coupling and stability" (renumbering later sections), or at least add a lead-in listing the subsections. | Medium |
| 10.3 | 10 (assumes too much) / 9 | The Milestone 3 checklist is one paragraph of about 230 words with eight numbered items inline. It is correct and important but hard to scan; set it as a numbered list (as Chapter 12 does for its list). The same applies to Chapter 7's checklist. | Low |
| 10.4 | 6 (external references) | Source [9] (Wikipedia, "Software package metrics") is used to confirm the definitions of afferent coupling, efferent coupling and instability, because the chapter's author could not check Martin's book directly. The chapter says so, which is honest, but a secondary encyclopaedia entry is a weak citation for the central metric of a section. Replace with Martin's own 2000 paper (cited in Chapter 6 as [1]) or his 1996 "Granularity" article, or cite the module's required book with chapter and let the reader verify. | Medium |
| 10.5 | 4 | Other claims checked: `Reservation` immutability without `equals`; `LoanPeriod` object equality; `PeriodValue` record equality; the 20-row/16-class counts are consistent with the table; the isolated-package rule ("undefined, not 0 or 1") is correct mathematically (0/0). The statement that the layer matrix cannot rule out cycles inside a layer (directory <-> notification) is correct and shows why the separate cycle test exists. | OK |
| 10.6 | 5 | Cross-references: Chapter 8 (directory), Chapter 9 (`behaviour` package demonstration), Chapter 11 (next), Appendix/`PackageMetrics` and ADR-010 (companion) all exist. The numbering "Sections 10.1-10.4 establish the structural model ... 10.5-10.6 ... 10.7-10.8" matches the headings. | OK |
| 10.7 | 3 / 5 | The Curriculum page (`content/topics/_index.md`, line 84) says this chapter covers "package cohesion (REP, CRP, CCP) and package coupling (ADP, SDP, SAP)". The chapter itself never uses these abbreviations. It teaches the two cohesion rules in plain words (things that change together, things used together, i.e. CCP and CRP), the acyclic dependencies principle by name, and the stable-dependencies idea; the reuse/release equivalence principle (REP) and the stable-abstractions principle (SAP, abstractness) are not taught. Either add two short paragraphs (REP; abstractness and SAP) or change the Curriculum page to match the chapter. | Medium |

## Chapter 11: Refactoring and Legacy Code

**Overall:** one of the strongest chapters. It teaches a method (observe, seam, pin, reshape, then change behaviour) on a single realistic 40-line method, keeps "known / likely / unknown" apart, and lets the reader meet each surprise before explaining it. The fine table was recomputed and is correct (S: 3 days = 0.50, 10 days = 4.00, cap 10.00 reached at 22 days; T: grace 5, cap 5.00 reached at 25 days; "s" lower-case at 3 days = 3.00, six times the student fine).

| # | Criterion | Finding | Severity |
|---|---|---|---|
| 11.1 | 4 (accuracy) | Opening scenario: "The number five appears twice in the staff branch, once in a comparison and once in a subtraction". In the listing the literal `5` appears three times in the staff branch (`late > 5`, `late - 5` and the cap `fine > 5` / `fine = 5`). The grace number does appear twice, but the sentence invites a search-and-replace of `5`, which would also change the cap. State it precisely ("the grace number appears twice, and the same literal 5 also stands for the cap") and the example becomes stronger evidence for the magic-numbers smell used later. | Low |
| 11.2 | 4 | Section 11.3 says "The list shows one of each class" but then names examples of three classes (surprising, suspected defect, unknown); no "expected" example is named, although the table has plenty (S 3 days, T 6 days). Say "one of each non-expected class", or add the expected example. | Low |
| 11.3 | 10 (assumes too much) | "oracle" ("keep a copy of the original code as an oracle") and "differential test" are used with one gloss only (the second). Define "oracle" as a trusted source of expected results at first use. `@ParameterizedTest/@CsvSource` and `Clock.fixed` are assumed from Chapter 7: fine. | Low |
| 11.4 | 7 (diagrams) | Figures 11.1, 11.2, 11.3 are correct and explained in captions; Figure 11.3 even clarifies "an agreement needs a specific rule". Figure 11.1 puts the rollback loop on `Reshape`, while the text says rollback applies after any failing step (the seam edit has no tests yet, so it cannot roll back by test failure; the probe covers it). Fine. | OK |
| 11.5 | 2 (jumping) / 5 | Section 11.4 "Seams and dependency isolation" starts with a three-row table of hidden dependencies, then deals only with the clock in depth and says the locale and output stream are "left alone". The reader may expect all three to be solved. The chapter does say why (the edit would be bigger than the tests justify), so this is a sequencing remark: put that sentence before the table. | Low |
| 11.6 | 6 | 15 sources, all resolve. Source 15 (Fowler 2018) is flagged "Not reopened for this chapter", an honest limitation. Fowler's "Legacy Seam" (2024) and Feathers's InformIT chapter are used for the seam definition and are correctly attributed. | OK |
| 11.7 | 5 | Quiz 2 pointers in 11.11 correctly map Weeks 5-9 to Chapters 6-10. The closing sentence "four recorded oddities" agrees with the table (three suspected defects and one unknown). Chapter 12 is correctly introduced as the next chapter and as the place where the visiting-researcher request appears. | OK |
| 11.8 | 3 (comprehensive) | The chapter is clear that it teaches a method, not a catalogue of smells ("Chapter 5 introduced smells"). Missing, deliberately: automated refactoring tools in the IDE, and version-control mechanics beyond `git restore`/`git revert`. A one-line pointer to IDE refactorings would help beginners (a mechanical refactoring performed by a tool is a safer way to do Extract Method). | Low |

## Chapter 12: Measuring Progress, Flow and Technical Health

**Overall:** the arithmetic is correct and unusually well explained; the chapter's rule that a metric needs a unit, a boundary and a decision is repeated in every section. The measurement contract and the two-way reading of the burn-up (scope events) are model teaching. I recomputed every number: scope 20 -> 23 -> 25 -> 23, completed 0 -> 3 -> 5 -> 10 -> 13 -> 16, WIP per day (1,2,2,1,2,2,3,3,3,2,2), lead/cycle/wait means 4.6 / 2.8 / 1.8, median cycle 3, ages 4 and 3, velocity 16 points, throughput 5 items. All agree with the tables.

| # | Criterion | Finding | Severity |
|---|---|---|---|
| 12.1 | 5 (cross-references) / 4 | **A numerical contradiction with other chapters.** Section 12.6 says "There are 136 passing tests in the Chapter 11 checkpoint" (and the Chapter 12 companion repeats "136" twice, at its lines 277 and 298). Appendix D, Chapter 11's companion, Chapter 13 and Chapter 14 all give the Chapter 11 checkpoint as **159 invocations** (121 inherited + 28 for the legacy report + 10 for the bridge). 136 appears to be an earlier state of Chapter 11. Change "136" to "159" in `content/book/chapter-12.md` (12.6) and in `content/companion/chapter-12.md` (two places). | High |
| 12.2 | 7 (diagrams) | The only figure is a Mermaid `xychart-beta` with two unlabelled lines. It has no figure number or caption, and the format has no legend, so the reader learns which line is scope and which is completion only from the sentence above it. The chart samples five dates (01, 04, 06, 08, 11), which hides the day-04 rise that the paragraph just above explains. Add a caption ("Figure 12.1. Upper line: scope; lower line: completed points; sampled on five dates") and consider sampling all 11 days, or sampling the days the text discusses (03, 04, 07, 08). `xychart-beta` is also a beta Mermaid type and may render differently across versions. | Medium |
| 12.3 | 8 (titles) / 2 | The title says "Measuring Progress, Flow and Technical Health", but Section 12.7 (about 25% of the chapter's substance) is a change-impact analysis and a full requirement contract for CR-12. A reader following the title does not expect it, and the transition (12.6 on metric misuse -> 12.7 a new feature specification) is abrupt. Either mention the changed requirement in the title or description ("...and Planning a Changed Requirement") or add a bridge sentence at the end of 12.6. The chapter's own opening problem does introduce the new request, which mitigates this. | Medium |
| 12.4 | 10 (assumes too much) | The chapter takes WIP, Definition of Done, Sprint and velocity as known (Chapters 3-4 introduced them), but "work-item age" and "cohort" are used from the learning outcomes onward and are defined only in 12.1 and 12.5. The measurement-contract table (12.1) is excellent once read, but it is the first technical content of the chapter and defines 10 fields in a block: break the "Reporting interval", "Snapshot" and "Completion cohort" rows out with a one-sentence example each. | Low |
| 12.5 | 9 (narrative) | Section 12.2 (Estimation revisited) sits between the issue history and velocity and is mostly prose about estimates, with no new calculation. It reads as a reminder of Chapter 3 plus CR-12 seeds ("for the approval change, start with a concrete example"). Adding "see Chapter 3, 3.8" and shortening it would make 12.1 -> 12.3 more direct. | Low |
| 12.6 | 6 (external references) | 8 sources; the six online ones resolve. The Goodhart caution is given without a source and is flagged as "a general interpretive warning, not a numerical law". The SPACE paper is correctly cited (ACM Queue 19(1), 2021). *Accelerate* is not checkable online; the chapter says it does not claim access to the whole book. | OK |
| 12.7 | 3 (comprehensive) | The chapter explains lead/cycle/throughput/WIP/age and burn charts, but not Little's Law (WIP = throughput x cycle time), cumulative flow diagrams or how to display a cycle-time distribution (scatter plot/percentiles). All are deliberately left to "optional extension" and the Kanban Guide; a one-sentence pointer to Little's Law would give the reader the relation between three of the five measures the chapter defines. | Low |
| 12.8 | 4 | Statement "Dividing seven by 16 gives 0.4375 iterations" is arithmetic only; the text carefully states it is not a forecast. The AI fixture's claims (six items and 18 points, mean cycle two days, 0.44 iterations) are each refutable from the tables. | OK |

## Chapter 13: Integration, Delivery and Feedback

**Overall:** excellent. The risk-first table (what could go wrong -> where -> cheapest check -> what it cannot show) is the right way to introduce test scope; the failure-policy table for the HTTP client turns an implicit decision into a reviewable one; the stalled-body experiment (1,700 ms against a 300 ms timeout) teaches that "a test of a failure path covers the failure you imagined". Figure 13.3 matches the code's decision order, and the text states that the order is observable (a four-day request with an unreadable register fails with the register's error). Counts agree with Appendix D (203 + 26 + 3 = 232; 159 inherited + 73 new).

| # | Criterion | Finding | Severity |
|---|---|---|---|
| 13.1 | 7 (diagrams) | Figure 13.1's caption says "Solid boxes are our code; the two outer boxes ... are what we do not control", but the Mermaid source draws every box in the same style; the reader cannot see which boxes are "outer". Add a class definition (different fill or dashed border) for `Directory service` and `approvals.tsv`. Figures 13.2 and 13.3 are fine; Figure 13.3's caption correctly says the FAILURE box is an exception that nothing on the request path catches. | Medium |
| 13.2 | 10 (assumes too much) | 13.2 assumes HTTP vocabulary (status 200/404/500, headers versus body, a loopback address, an ephemeral port, a stub server). That is reasonable for a postgraduate software course, but the chapter neither defines these in a line nor points to Appendix B. A short "HTTP in one paragraph" box (status code, headers, body, timeout) would remove the dependence on prior knowledge for students from other backgrounds. | Medium |
| 13.3 | 2 / 9 | 13.2 is the longest section (file boundary, network boundary, failure policy, timeout trap, two kinds of contract test). The timeout subsection is the chapter's best material but arrives as a long digression. Each subsection has its own heading, so the structure is clear; a two-sentence preview at the start of 13.2 listing what it covers would help. | Low |
| 13.4 | 5 (cross-references) / 4 | Consistency with the companion: the Chapter 13 companion says the version becomes **0.13.0** (its section 2.1 table, line 126, and the `pom.xml` instruction, line 1924) while its own POM hunk, Appendix D and Chapter 14 say **0.13.1**. Its B1 model answer says "202, 25, 3" invocations while its expected-output section (1.2) says 203, 26, 3 (the book and Appendix D use 203/26/3). The chapter text itself is correct; fix the companion. | Medium |
| 13.5 | 6 (external references) | All 14 sources resolve. Source 4 (GitHub Actions workflow syntax) has moved: the URL redirects to `/en/actions/reference/workflows-and-actions/workflow-syntax`. Update the link. | Low |
| 13.6 | 8 (titles) | "13.9 AI in practice: inspect an integration test that replaces its boundary" is accurate but long (13 words); the other chapters use shorter AI titles. "13.9 AI in practice: an integration test that mocks its boundary" would match the rest. | Low |
| 13.7 | 3 (comprehensive) | The chapter covers three test scopes, contract tests, a pipeline, delivery versus deployment, a flag and rollback, and states what it does not do (hosted run, real provider, concurrency). Not covered, reasonably: test data management for databases, containerised test environments, performance tests. The limits list in 13.8 mentions several. | OK |

## Chapter 14: Responding to Change and Handing Over

**Overall:** very good, and the most honest chapter about evidence. It shows an experiment where a one-line change passes the whole unit stage (E3: 4 of 232 fail, all 203 unit invocations pass), uses it to say that a small diff is not a better design, then closes the gap in an exercise (B8). The numbers recompute: 23 files added and 10 changed; 399 lines in 9 new production files; 45 of 159 and 73 of 235 tests failing in the two "what breaks" experiments; 14 known issues = 1 fixed + 7 deferred + 6 accepted; the 16 README statements = 6 supported, 8 contradicted, 2 not established.

| # | Criterion | Finding | Severity |
|---|---|---|---|
| 14.1 | 2 (jumping) / 8 (titles) | Section 14.3 "Documentation and decision records" holds five different subjects: the six-document model, decision records, ADR-014 with its rehearsed flag removal (11 files, 87 lines added, 131 removed), requirements-to-evidence traceability with `TraceabilityTest`, and release notes. The rehearsal and the traceability test are not "documentation" in the usual sense. They are good material, but a reader looking for traceability would not look under this title. Split into "14.3 Documents and decision records" and "14.4 Keeping the evidence true: rehearsal and traceability", renumbering later sections. | Medium |
| 14.2 | 5 (cross-references) | B8 says "Close the gap that E3 found", but the chapter body never names the experiment E3 (the experiments are labelled only in the companion). Add "(experiment E3 in the companion)" where the one-line adapter change is described in 14.1. | Low |
| 14.3 | 5 | Cross-references verified: Appendix C (C.5, C.10, C.11, C.12), Appendix E (E.4 contribution evidence, E.5 final handover, E.6 reflection) all exist; Chapter 15 is correctly named as the next chapter. The Chapter 14 companion (line 158) says the version changes "from 0.13.0 to 0.14.0" but the hunk below it shows 0.13.1 -> 0.14.0. | Low |
| 14.4 | 7 (diagrams) | Figures 14.1 (footprint), 14.2 (triage) and 14.3 (traceability chain) each have a caption that says what the arrows mean. Figure 14.1's caption ("an existing file using a new one, or a new file using another") matches the drawn arrows. | OK |
| 14.5 | 10 (assumes too much) | 14.4 mentions `sun.misc.Unsafe` warnings and a "dynamic-agent warning" as things a reader "may see that are not errors". Correct, but a student cannot know why they appear. One sentence ("these come from the JDK version, not from your code") would help. | Low |
| 14.6 | 3 / 9 | Contribution evidence (14.5) is handled with maturity: four rankings give three orders; no ranking is offered; GitHub's contribution-graph rules (email, default branch, forks) are cited. The final-submission section (14.6) uses the descriptor's five phrases as an evidence index and says the book creates no new marking rules. | OK |
| 14.7 | 6 (external references) | Sources 1-9 resolve; three GitHub documentation URLs (contribution graph, commits with multiple authors, pull-request reviews) have moved and redirect to new addresses. Update them. | Low |

## Chapter 15: AI as a Software Engineering Assistant

**Overall:** the clearest statement in the book of a single method (define the task, derive examples first, check against evidence the assistant did not write, record the decision), with a worked task in which both rejected attempts are instructive and are kept. The honesty rules (constructed output is labelled; "I tested it" is a claim; a green build is not review) are consistent with every earlier AI activity. The table of Chapters 1 to 14 activities matches what those chapters actually contain.

| # | Criterion | Finding | Severity |
|---|---|---|---|
| 15.1 | 6 (external references) | The hallucinated-package statistics (16 models, 576,000 samples, at least 5.2% commercial and 21.7% open-source) agree with the abstract of arXiv 2406.10279 (Spracklen et al.). The chapter correctly warns that the figures describe that study, not the reader's tool. `List.getFirst()` (Java 21) and `--release` semantics are correct. The PMD, Maven Central, OWASP and Oracle sources resolve. | OK |
| 15.2 | 2 (jumping) | As a reference chapter the order workflow -> work orders -> explanations -> code and tests -> refactoring -> failure modes -> privacy -> records -> offline alternatives is logical. The worked task (15.4) comes after the explanation section; students who only do the minimum lab (B1-B4) go straight to the lab files, and the reading route says so. | OK |
| 15.3 | 8 (titles) | The subsection heading "Ask for explanations that are about the code, and then check them" (12 words) is long and slightly clumsy. "Explanations: ask for claims, then check them" would read better. Other titles are clear and academic. | Low |
| 15.4 | 7 (diagrams) | Figure 15.1 (six-step workflow) and Figure 15.2 (the worked example) both have captions. Figure 15.1's caption says the first box is the user's own and that the loop is where the work happens. Figure 15.2 records the experimental outcomes on its arrows (2 errors; EX4 and EX5 fail; 9 examples pass). | OK |
| 15.5 | 4 (accuracy) | Fault experiment: 8 of 10 faults caught by the acceptance examples, 4 of 10 by the generated tests; the two survivors are equivalent (the exception type is unchanged). The key result, that the generated tests miss the assistant's own fault (a window one step too long), is demonstrated and explained. | OK |
| 15.6 | 10 (assumes too much) | 15.7 uses "Maven Central coordinate", "group ID", "pinned version" and SHA-256 with the Maven background of Chapter 7. The chapter declares no entry checkpoint, so a reader who starts here lacks that background. Add "(see Appendix B.4)" at the first Maven term. | Low |
| 15.7 | 5 (cross-references) | Chapter 1's promise ("Section 15.1 gives a longer introduction"), Appendix C.13 (record template), Appendix F and the "Chapters 6, 7, 8, 13" itinerary for the directory are consistent. "This chapter has no teaching week" agrees with Chapter 1. | OK |


## 7. Suggested order of work

1. Fix the High item (Chapter 12 "136" -> "159": book, companion, deck). Ten minutes.
2. Fix the cross-document inconsistencies (Figure 10.1 and its deck copy, the Curriculum page, the two companions). One hour.
3. Add the missing figure captions and the two small figure changes (Figure 13.1 styling, Figure 12 labels). One hour.
4. Rework the five over-packed sections (5.1, 7.4, 10.4, 12.7, 14.3) by reordering or splitting, with bridges. This is the only item that changes section numbers, so do it last and re-run the cross-reference check afterwards.
5. Replace the two weak sources and update the six moved addresses. One hour.
6. Convert the milestone checklists and acceptance-conditions paragraphs to lists.

The scripts used for the mechanical checks (headings, cross-references, citations, readability) can be re-run after each batch of edits to confirm that no reference was broken.
