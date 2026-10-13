from cleanup_lib import *

R = "Unresolved_Items_Chapters_1-3.md"
T = "Remaining_Chapters_Todo.md"

# --- chapter pointers: from 'is planned' to the present tense
replace_once("Chapter_01_Developing_Software_That_Can_Change.md",
 "Appendix B is planned to give a full, reproducible development setup; until it is available, a Java Development Kit and the commands shown above are all this exercise needs,",
 "Appendix B gives a full, reproducible development setup; a Java Development Kit and the commands shown above are all this exercise needs,")
replace_once("Chapter_02_Object_Oriented_Development_Beyond_Syntax.md",
 "Appendix B is planned to collect the Git commands and the pull-request workflow used in this book; the Pro Git readings",
 "Appendix B collects the Git commands and the pull-request workflow used in this book (B.8); the Pro Git readings")
replace_once("Chapter_07_Testing_as_a_Design_Practice.md",
 "Appendix B is planned to record the Maven, JUnit and Mockito setup; until then, the companion's `pom.xml` and commands are the setup reference.",
 "Appendix B records the Maven, JUnit and Mockito setup (B.4 and B.5); the companion's `pom.xml` and commands are the exact reference for this chapter.")

# --- register
replace_once(R,
 "- [ ] **Appendix B** (Tools and reproducible setup): cited in Chapters 1 and 2. Must cover Git commands, the pull-request workflow, and the pinned toolchain.",
 "- [x] **Appendix B** (Tools and reproducible setup): drafted 13 October 2026 (manuscript and companion). It covers the Git commands and pull-request routine (B.8), the pinned toolchain (B.1), Maven (B.4), JUnit and Mockito (B.5), PMD (B.6), the starter hosted check (B.9) and a troubleshooting table (B.11). Open items are listed in the section `Appendix B` below.")
replace_once(R,
 "(Appendix B must pin the version)",
 "(Appendix B pins the version: PMD 7.28.0, with the same digest)")
replace_once(R,
 "The module leader must decide and state it in the exam brief and Appendix B.",
 "The module leader must decide and state it in the exam brief. Appendix B (B.5) records only how Mockito is configured and says that it grants no permission.")
replace_once(R,
 "- [ ] **Appendix B** must describe the Maven setup (install, `mvn verify`, offline cache, proxy notes), since the chapter now points to it.",
 "- [x] **Appendix B** describes the Maven setup (install, `mvn verify`, offline cache, proxy settings), and Chapter 7 now points to it in the present tense. The proxy snippet is not given; B.4 points to the Maven settings reference and says to ask the institution for proxy details.")
replace_once(R,
 "| Ch 5 | The static-analysis lab will add a named analyser to the manual-review comparison | Appendix B (D5) |",
 "| Ch 5 | The static-analysis lab will add a named analyser to the manual-review comparison | Appendix B (D5): done, B.6 pins PMD 7.28.0 |")

APPB = """## Appendix B: Tools and reproducible setup (drafted 13 October 2026)

- [ ] **Files:** `Appendix_B_Tools_and_Reproducible_Setup.md` and `Appendix_B_Code_Explanations_and_Solutions.md`. The companion holds a complete small starter project (11 files) and a scripted Git walk-through. Both were rebuilt from the finished companion and matched the working copy byte for byte.
- [ ] **Not run, and said so in the text where it matters:** a hosted run of the workflow file; the GitHub or GitLab pull-request steps (B.8 steps 5 to 8); a proxy configuration; any Java 17 runtime (everything ran on JDK 24.0.2 with `--release 17`); macOS or Linux (the scripts avoid GNU-only options, but only Git Bash on Windows was used); the WSL-bash and CRLF failure (taken from Chapter 4, not repeated).
- [ ] **Newer Maven exists.** The Maven installation page lists 3.10.0 as the current stable release on 13 October 2026. The book stays on 3.9.11 and says so in B.1. Whether the POMs run unchanged under 3.10.0 was not tried.
- [ ] **Decisions still the module leader's:** D4 (whether a mocking framework is allowed in the midterm; B.5 says the appendix grants no permission) and D9 (the agreed repository-metrics method; B.10 defers to Chapter 12's RM-12 until the module states one).
- [ ] **Check once:** the `mvn.cmd`/`CHAPTER_MVN` wording in B.2, the Windows `bash` paragraph (which program runs first depends on the machine's path), and the AI activity in B.12 (constructed, two of its four claims were demonstrated by experiment: skipping tests and ignoring failures both give `BUILD SUCCESS` with a failing test).
- [ ] **Sources:** 18 listed; all opened on 13 October 2026 and the specific claim checked (Maven installation, settings and lifecycle pages; Surefire pages; JEP 451; Git manuals; gitattributes; setup-java and checkout READMEs; PMD installation; Mockito `MockMakers`; the Maven 3.9.11 archive and SHA-512 and the PMD 7.28.0 digest, both compared with the local files).
- [ ] **Pointers updated:** Chapter 1 (line 352), Chapter 2 (line 510) and Chapter 7 (line 36) no longer say Appendix B is planned. Chapter 2 line 30 already used the present tense.
- [ ] **Not changed on purpose:** Chapter 5 and Chapter 6 do not point to Appendix B by name; their own setup steps stay in their companions. Appendix A still says Appendix B covers installation and the wider toolchain, which is now true.

"""
replace_once(R, "## UML coverage gaps (raised in review of Chapter 2)", APPB + "## UML coverage gaps (raised in review of Chapter 2)")

# --- the todo list
text = read(T)
old = [l for l in text.split("\n") if l.startswith("- [ ] **Appendix B: Tools and reproducible setup**")]
assert len(old) == 1
replace_once(T, old[0], old[0].replace("- [ ]", "- [x]", 1) + " (drafted 13 October 2026; see its section in the register)")
print("pointers, register and todo updated")
