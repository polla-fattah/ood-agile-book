from cleanup_lib import *
C = "Chapter_06_Code_Explanations_and_Solutions.md"
M = "Chapter_06_Interfaces_Dependencies_and_Composition.md"

replace_once(C, "*OO Development and Agile Practices*  \nVersion 1.1 • 13 October 2026 • reviewed against Blueprint v0.3\n", "*OO Development and Agile Practices*\n", 6, "header version line", evidence=True)

rewrite_line(C, "Two further checks, added in version 1.1, cover the claim",
  "Two further checks cover the claim that unexpected programming failures are not swallowed. A sender that throws `IllegalStateException` makes the reservation call propagate that exception, and the record is already stored when it does. Without them, replacing `catch (NotificationException ...)` with `catch (RuntimeException ...)` would pass every check.",
  6, "Section on checks, sentence about version 1.0 and 1.1 (reworded)")

# Section 13: move the environment paragraphs and the results table
cut(C, 6, "Section 13, version paragraphs and observation table",
    "**Version 1.0 (12 October 2026)** was run on Linux with OpenJDK 17.0.20 through a `CHAPTER_JAVAC` wrapper around `java com.sun.tools.javac.Main`, because that environment had no `javac` launcher. That run was not repeated. Learners should use a normal Java 17 JDK and the ordinary commands printed above.",
    "**Do the checks detect faults?** Fourteen faults were introduced one at a time into a copy of `after`, and the full gate was run on each. In version 1.0's checks, thirteen were caught and one survived; version 1.1's two extra checks close that gap, so all fourteen are now caught.",
    replacement="### 13.1 Do the checks detect faults?\n")
rewrite_line(C, "**Do the checks detect faults?** Fourteen faults were introduced",
  "Fourteen faults were introduced one at a time into a copy of `after`, and the full gate was run on each. All fourteen are caught.",
  6, "Section 13, lead-in (reworded; version 1.0 and 1.1 history removed)")
rewrite_line(C, "| `catch (NotificationException)` widened to `catch (RuntimeException)` |",
  "| `catch (NotificationException)` widened to `catch (RuntimeException)` | Caught: `unexpected sender failure is not swallowed` |",
  6, "Fault table row (the 'Survived in 1.0' wording removed)")

# container lab paragraph and the feasibility paragraph
rewrite_line(C, "**Container lab (Blueprint decision D3, closed 13 October 2026).**",
  "### 13.2 Container lab\n\nThe student chapter's required container lab (practical step 7) uses the educational container `DemoContainer`, listed in Section 6.1 of this file and runnable with plain `javac`. The module descriptor mentions a real library container; the book records that as a known difference and does not pin one. A team that wants to try a library container may do so on its own, with the dependency management that the plain-`javac` gate does not provide.",
  6, "Section 13, 'Container lab' paragraph (Blueprint decision D3, dates and the pointer to the feasibility note removed)")
cut(C, 6, "Section 13, Real-container feasibility paragraph (Spring Framework 7.0.9 experiment)",
    "**Real-container feasibility (background; not adopted and not part of the chapter).** A candidate walkthrough using Spring Framework 7.0.9 was compiled and run against the real Chapter 6 classes, using jars already in the author's local Maven cache. Configuration classes registered the formatter, a recording sender, the policy map and the coordinator. Spring resolved the coordinator's three constructor arguments by type. The container produced the same reservation result, returned the same coordinator on repeated lookup (default singleton lifetime), and failed with a `BeanCreationException` when the sender registration was missing. It needed eight jars (`spring-context`, `spring-core`, `spring-beans`, `spring-aop`, `spring-expression`, `micrometer-observation`, `micrometer-commons` and `commons-logging`), and failed with `NoClassDefFoundError` until `commons-logging` was added. Adopting a real container therefore needs dependency management that the plain-`javac` gate does not provide. Nothing was downloaded, and no library container has been adopted.",
    "**Sources.** The Chapter 6 sources were opened on 12 and 13 October 2026 and support the claims made about them, with two exceptions. The Martin (2000) PDF is a scanned image whose text could not be machine-checked. A web search confirmed its existence and publication details, and the chapter cites the module's required Martin text for the same material. The Spring page does not say the container “configures” objects, so the chapter's wording was corrected.")
cut(C, 6, "Section 13, Sources paragraph (sources opened, Martin 2000 PDF, Spring wording)",
    "**Sources.** The Chapter 6 sources were opened on 12 and 13 October 2026 and support the claims made about them, with two exceptions. The Martin (2000) PDF is a scanned image whose text could not be machine-checked. A web search confirmed its existence and publication details, and the chapter cites the module's required Martin text for the same material. The Spring page does not say the container “configures” objects, so the chapter's wording was corrected.",
    "The supplied application gate stops on a nonzero check result. The container's expected errors are caught inside its demonstration to verify those teaching cases; this is distinct from suppressing unexpected application test failures.")
replace_once(C, "## 13. Verification record", "## 13. Fault experiment and container notes")

# manuscript
replace_once(M, "checks, solutions and verification evidence.", "checks, solutions and teaching notes.", 6, "Manuscript line 35", evidence=True)
replace_once(M, " (version 1.1 of the companion, 13 October 2026), isolated", ", isolated", 6, "Manuscript line 334", evidence=True)

log(6, [
 "Companion: removed the `Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3` line (R1, R2, R4).",
 "Companion section 13 `Verification record` is now `Fault experiment and container notes`, with two subsections: `13.1 Do the checks detect faults?` and `13.2 Container lab`.",
 "Moved to evidence (R3, R8): the two version paragraphs (Linux and OpenJDK 17.0.20; Windows 11 and JDK 24.0.2), the 12-row results table (gate results, `-Xlint:all`, file comparisons, Mermaid, `PrintStream` error flag, not-performed items), the Real-container feasibility paragraph (a Spring Framework 7.0.9 experiment using jars from the author's Maven cache) and the `Sources` paragraph (sources opened on 12 and 13 October 2026; the Martin 2000 PDF; the Spring wording).",
 "Kept: the 14-fault table. Removed the `Survived in 1.0` history from the row about catching `RuntimeException`, and removed `version 1.0` and `version 1.1` from the lead-in and from the earlier paragraph about the two further checks. The faults are the same, and all fourteen are caught.",
 "Rewrote the `Container lab (Blueprint decision D3, closed 13 October 2026)` paragraph as a plain description of the lab tool, keeping that the module descriptor mentions a real container and the book pins none. It no longer points to the feasibility note that was moved (R2, R7).",
 "Kept: the closing paragraph that expected container errors are caught inside the demonstration, which is teaching content.",
 "Manuscript line 35: `verification evidence` is now `teaching notes`, because the verification record is no longer in the companion. Manuscript line 334: removed `(version 1.1 of the companion, 13 October 2026)`.",
 "Manuscript: the source note `Sources checked 12 and 13 October 2026` is an access date and stays.",
])
print("chapter 6 done")
