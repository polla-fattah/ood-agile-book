# Chapter 6: verification and working evidence (NOT FOR PUBLISHING)

Text removed verbatim from the published chapter files during the first-draft cleanup of 13 October 2026. The originals of the chapter files are in `../backup_before_cleanup/`.

## From `Chapter_06_Code_Explanations_and_Solutions.md`: header version line

*OO Development and Agile Practices*  
Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3

---

## From `Chapter_06_Code_Explanations_and_Solutions.md`: Section on checks, sentence about version 1.0 and 1.1 (reworded)

Two further checks, added in version 1.1, cover the claim that unexpected programming failures are not swallowed. A sender that throws `IllegalStateException` makes the reservation call propagate that exception, and the record is already stored when it does. Version 1.0 made the claim in prose but had no check for it: replacing `catch (NotificationException ...)` with `catch (RuntimeException ...)` passed every check.

---

## From `Chapter_06_Code_Explanations_and_Solutions.md`: Section 13, version paragraphs and observation table

**Version 1.0 (12 October 2026)** was run on Linux with OpenJDK 17.0.20 through a `CHAPTER_JAVAC` wrapper around `java com.sun.tools.javac.Main`, because that environment had no `javac` launcher. That run was not repeated. Learners should use a normal Java 17 JDK and the ordinary commands printed above.

**Version 1.1 (13 October 2026)** was re-verified on Windows 11 in Git Bash with JDK 24.0.2 and the ordinary `javac` launcher, compiling with `--release 17`. All 26 listings were extracted programmatically from this file, so the files that ran are the files printed here.

| Observation | Result |
|---|---|
| Completed gate (`after`) | Exit 0: 34 checks, five acceptance groups, 44 Chapter 5 checks and 28 Chapter 6 checks, then `BUILD AND CHECKS PASSED` |
| `javac --release 17 -Xlint:all` on `after` | Version 1.0 printed one `[serial]` warning for `NotificationException`; fixed in 1.1 with `serialVersionUID`, and the build is now warning-free |
| Starting coordinator (`before`) | Identical to the Chapter 5 coordinator |
| Coupled checkpoint (Chapter 5 copy plus the coupled coordinator and three sender files) | Chapter 5 gate exit 0; accepted requests print console notices while the old assertions still pass |
| Other files against Chapter 5 | `LoanPeriod`, `Reservation`, `ConfirmationFormatter`, `BorrowerCategory`, `BorrowingPolicy` and both rule classes identical. `Chapter02Checks` and `Chapter05Checks` differ only in their construction expressions |
| Acceptance listing | Version 1.0 carried Chapter 3's earlier, narrower AC-03 and omitted `.gitattributes`. Version 1.1 matches Chapter 3 v1.1 once the setup migration is undone, and includes `.gitattributes` |
| Console application | One notice and one result line, as documented; Chapter 4 and 5 demonstrations unchanged |
| Educational container | Shared coordinator observed; missing binding and cycle detected, as documented |
| Directory contract preview (Section 6.4 of the chapter) | Text only, not part of this checkpoint. The `BorrowerDirectory` interface shown there is copied unchanged from the Chapter 8 companion; the Chapter 8 build compiles and tests it |
| Mermaid diagrams | Figure 6.1 (class diagram), Figure 6.2 and the companion's assembly view rendered without error with Mermaid 10.9.1; in a screenshot, every “creates” arrow in Figure 6.1 starts at `ReservationApplication` |
| `PrintStream` error flag | An output that fails on its first write only: `checkError()` returned `true` after the failure and still `true` after a later successful write, so the flag is sticky |
| External notification delivery | Not implemented or attempted |
| Hosted CI and independent review | Not claimed; teams must retain actual evidence |

---

## From `Chapter_06_Code_Explanations_and_Solutions.md`: Section 13, lead-in (reworded; version 1.0 and 1.1 history removed)

**Do the checks detect faults?** Fourteen faults were introduced one at a time into a copy of `after`, and the full gate was run on each. In version 1.0's checks, thirteen were caught and one survived; version 1.1's two extra checks close that gap, so all fourteen are now caught.

---

## From `Chapter_06_Code_Explanations_and_Solutions.md`: Fault table row (the 'Survived in 1.0' wording removed)

| `catch (NotificationException)` widened to `catch (RuntimeException)` | **Survived in 1.0.** Caught in 1.1: `unexpected sender failure is not swallowed` |

---

## From `Chapter_06_Code_Explanations_and_Solutions.md`: Section 13, 'Container lab' paragraph (Blueprint decision D3, dates and the pointer to the feasibility note removed)

**Container lab (Blueprint decision D3, closed 13 October 2026).** The student chapter's required container lab (practical step 7) uses the educational container `DemoContainer`, listed in Section 6.1 of this file (version 1.1, 13 October 2026) and runnable with plain `javac`. The module leader adopted it as the lab tool. The module descriptor mentions a real library container; the book records that as a known difference and does not pin one. The feasibility note below is background for a team that wants to try a library container, and nothing in it is adopted.

---

## From `Chapter_06_Code_Explanations_and_Solutions.md`: Section 13, Real-container feasibility paragraph (Spring Framework 7.0.9 experiment)

**Real-container feasibility (background; not adopted and not part of the chapter).** A candidate walkthrough using Spring Framework 7.0.9 was compiled and run against the real Chapter 6 classes, using jars already in the author's local Maven cache. Configuration classes registered the formatter, a recording sender, the policy map and the coordinator. Spring resolved the coordinator's three constructor arguments by type. The container produced the same reservation result, returned the same coordinator on repeated lookup (default singleton lifetime), and failed with a `BeanCreationException` when the sender registration was missing. It needed eight jars (`spring-context`, `spring-core`, `spring-beans`, `spring-aop`, `spring-expression`, `micrometer-observation`, `micrometer-commons` and `commons-logging`), and failed with `NoClassDefFoundError` until `commons-logging` was added. Adopting a real container therefore needs dependency management that the plain-`javac` gate does not provide. Nothing was downloaded, and no library container has been adopted.

---

## From `Chapter_06_Code_Explanations_and_Solutions.md`: Section 13, Sources paragraph (sources opened, Martin 2000 PDF, Spring wording)

**Sources.** The Chapter 6 sources were opened on 12 and 13 October 2026 and support the claims made about them, with two exceptions. The Martin (2000) PDF is a scanned image whose text could not be machine-checked. A web search confirmed its existence and publication details, and the chapter cites the module's required Martin text for the same material. The Spring page does not say the container “configures” objects, so the chapter's wording was corrected.

---

## From `Chapter_06_Interfaces_Dependencies_and_Composition.md`: Manuscript line 35

checks, solutions and verification evidence.

---

## From `Chapter_06_Interfaces_Dependencies_and_Composition.md`: Manuscript line 334

 (version 1.1 of the companion, 13 October 2026), isolated

---

