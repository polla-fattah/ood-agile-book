# Appendix A: verification and working evidence (NOT FOR PUBLISHING)

Text removed verbatim from the published appendix files during the first-draft cleanup of 13 October 2026. The originals are in `../backup_before_cleanup/`.

## From `Appendix_A_Programming_Readiness_and_Notation.md`: manuscript header version line

*Designing, Testing and Evolving Software with AI Assistance*  
Version 1.0 • 13 October 2026

---

## From `Appendix_A_Code_Explanations_and_Solutions.md`: companion header version line

*OO Development and Agile Practices*  
Version 1.0 • 13 October 2026

---

## From `Appendix_A_Code_Explanations_and_Solutions.md`: Section 7, Verification record (environment, OpenJDK 17.0.20, results table, limits)

## 7. Verification record

The four source files were extracted from the printed Markdown listings into a fresh directory and checked on 13 October 2026 using OpenJDK 17.0.20. This environment exposes the JDK compiler through `java com.sun.tools.javac.Main`; it was invoked with the printed `--release 17 -Xlint:all -d out` options and all four source paths. The ordinary `javac` launcher command printed for readers was not invoked in this environment.

| Check | Observed result |
|---|---|
| Compilation from the four extracted listings | Exit 0; no compiler warnings. |
| `java -cp out ReadinessLab` | Exit 0; 27 checks passed; six output lines matched Section 1. |
| Deliberate `count <= 3` fault in a separate copy | Compilation succeeded; execution exited 1 with `AssertionError: fourth reservation rejected`. |
| Original lab source after fault experiment | Unchanged; the faulty comparison existed only in the scratch copy. |
| Mermaid diagrams | Source and relationship meanings reviewed. Visual rendering was not completed because the browser runtime could not be installed in this environment; inspect rendered layout before print/PDF publication. |

These are focused Java-readiness checks, not JUnit invocation counts for the lending project. They establish the selected observations on Java 17, not all possible inputs or the correctness of a cumulative checkpoint. The notation diagnostic is checked against its written scenario and still requires human interpretation.

---

