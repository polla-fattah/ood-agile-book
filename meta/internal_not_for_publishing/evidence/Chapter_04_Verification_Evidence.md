# Chapter 4: verification and working evidence (NOT FOR PUBLISHING)

Text removed verbatim from the published chapter files during the first-draft cleanup of 13 October 2026. The originals of the chapter files are in `../backup_before_cleanup/`.

## From `Chapter_04_Code_Explanations_and_Solutions.md`: header version line

*OO Development and Agile Practices*  
Version 1.1 • 13 October 2026 • reviewed against Blueprint v0.3

---

## From `Chapter_04_Code_Explanations_and_Solutions.md`: Line 13: second sentence about the verification record removed

All people, workload figures and review scenarios in the model answers are fictional. The verification record in Section 10 distinguishes actual local observations from work that learners must perform in their hosted repository.

---

## From `Chapter_04_Code_Explanations_and_Solutions.md`: Line 549: the sentence about the author environment reworded

`CHAPTER_JAVAC` is an optional path to a compiler executable. Ordinary use leaves it unset, selecting `javac`. It is a single executable path, not a place to put a multiword shell command. The author environment used this override as explained in Section 10; learners with a normal JDK should not need it.

---

## From `Chapter_04_Code_Explanations_and_Solutions.md`: Section 10.1, Observed author verification (whole subsection)

### 10.1 Observed author verification

**Version 1.0 (12 October 2026)** was verified on Linux with OpenJDK 17.0.20. That environment lacked the ordinary `javac` launcher, so `CHAPTER_JAVAC` pointed to a wrapper around `java com.sun.tools.javac.Main`. That run was not repeated. The `CHAPTER_JAVAC` override stays in the script for such environments; a normal JDK does not need it.

**Version 1.1 (13 October 2026)** was re-verified on Windows 11 in Git Bash with JDK 24.0.2 and the ordinary `javac` launcher, compiling with `--release 17`. The twelve files were extracted programmatically from this document, so the files that ran are the files printed here. The four application classes and `Chapter02Checks` were confirmed identical to the Chapter 2 listings. `Chapter03AcceptanceExamples` was confirmed identical to the Chapter 3 version 1.1 listing; version 1.0 of this file still carried Chapter 3's earlier, narrower AC-03.

| Verification | Observed result |
|---|---|
| `bash scripts/check.sh` from the repository root | Exit 0; 34 checks, five acceptance groups and `BUILD AND CHECKS PASSED` |
| Same script invoked from a different working directory | Exit 0 |
| Scripted reservation journey | R1 confirmed; overlap rejected; R2 confirmed; two records |
| Wrong AC-01 count expectation in a separate copy | Exit 1; `AssertionError: AC-01 one record`; no final success marker; the 34 checks had passed first |
| Correct expectation restored | Exit 0; success marker present |
| Deliberate syntax error in `Reservation.java` | Exit 1; no success marker |
| Workflow YAML | Parsed as valid YAML (checked with Ruby): triggers `push`, `pull_request`, `workflow_dispatch`; steps `actions/checkout@v7`, `actions/setup-java@v6`, `bash scripts/check.sh` |
| Action versions | `actions/checkout` v7 (latest release v7.0.1) and `actions/setup-java` v6 (latest release v6.0.1) exist, and the setup-java README documents `temurin` with `distribution` and `java-version` inputs |
| Git workflow in Section 3.7 | Replayed in a scratch repository: one commit, no `build/` content tracked |
| Fresh clone with `core.autocrlf=true`, no `.gitattributes` | `check.sh` arrives with CRLF line endings. It still ran under Git Bash. Under WSL bash it failed on line 2 with `set: pipefail: invalid option name` |
| Same clone with `.gitattributes` (`*.sh text eol=lf`) | `check.sh` stays LF. Under WSL it passed line 2 and stopped at the first `java` call only because that WSL distribution has no JDK |
| Mermaid flowchart in the student chapter | Rendered without error with Mermaid 10.9.1 |
| Hosted GitHub Actions run | Not performed; learner/team evidence required |
| Independent team review | Not performed; actual review required |
| Full gate under WSL or native Linux with a JDK | Not performed in version 1.1; version 1.0's Linux run predates the AC-03 change |

The verification supports the executable starter, local failure propagation and the line-ending fix. It does not certify an entire milestone submission or a production lending system. The companion supplies a workflow template and instructions for collecting the remaining evidence.

The Scrum Guide, `javac` manual, GitHub Maven tutorial and the two action repositories cited in the student chapter were opened on 12 and 13 October 2026. Each supports the claim made about it. Martin (2002) and Rubin (2012) use the publication details given in the module descriptor and were not independently looked up.

---

## From `Chapter_04_Code_Explanations_and_Solutions.md`: Section 10.2, paragraph 'Blueprint v0.3 continuity' (checklist part removed)

Blueprint v0.3 continuity: the practical activity runs on the Team project with the lending starter as the model, the chapter gives Core reading, Minimum required lab and Optional extension entries, the starter test is introduced in Arrange–Act–Assert terms for Chapter 7, and the Chapter 2 flat directory is mapped onto the conventional source layout. Milestone 1 needs hosted CI evidence, which depends on a repository the whole team can use. Ask teams to create that repository in the first session, so a late access problem does not become the only gap in their evidence.

---

## From `Chapter_04_Code_Explanations_and_Solutions.md`: Source note ('not opened' wording)

Martin (2002) and Rubin (2012) use the publication details given in the module descriptor and were not independently looked up.

---

