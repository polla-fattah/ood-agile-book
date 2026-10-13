from cleanup_lib import *

R = "Unresolved_Items_Chapters_1-3.md"

replace_once(R,
 "- [ ] **Appendix A** (Programming readiness and notation): cited in Chapters 1 and 2. Must include the Java idioms allowed (D2) and the class-diagram notation the midterm assesses (G5).",
 "- [x] **Appendix A** (Programming readiness and notation): drafted 13 October 2026 and cleaned for first draft. It has the Java idioms allowed (D2, adopted as the recommended table: working knowledge of lambdas, streams, records and `Optional`; reading knowledge of `var` and arrow `switch`; awareness only of sealed types, which no chapter declares) and the class-diagram notation the midterm assesses (G5). Still for the module leader: confirm the D2 list, and the midterm diagram format (below).")
replace_once(R,
 "Confirm this is how you want the UML coverage delivered, or move the sampler to Appendix A.",
 "**Decided 13 October 2026 (recommendation adopted):** Chapter 2 keeps teaching the notation with its worked example and exercises; Appendix A holds the look-up reference for all diagram kinds the book draws. Nothing moved out of Chapter 2.")
replace_once(R,
 "- [ ] **Appendix A: write the UML reference** (class diagram notation, plus the sequence, state and component notations below) so chapters can point to it.",
 "- [x] **Appendix A: write the UML reference.** Done 13 October 2026 (A.8): class diagrams with a hand-drawing column for each relationship; new subsections for sequence diagrams, state diagrams and flowcharts and dependency views (Figures A.2 to A.5), and a reading-practice table in the companion. The book draws no UML component diagrams (Chapter 10's package view is a flowchart); A.8 says so and describes formal UML package and component notation in one paragraph. All six Appendix A diagrams were rendered with Mermaid 10.9.1 in the browser pane.")
replace_once(R,
 "What remains is **Appendix A** (the written UML reference) and **Chapter 10**'s component and package notation.",
 "The written UML reference is now in **Appendix A** (A.8), including the dependency view that Chapter 10 uses.")
replace_once(R,
 "If the module leader confirms a format (hand-drawn or tool-based), adapt the practice and consider a printable blank-diagram worksheet.",
 "If the module leader confirms a format (hand-drawn or tool-based), adapt the practice and consider a printable blank-diagram worksheet. **Interim (13 October 2026):** Appendix A A.8 is written to work for both: every symbol is given as Mermaid source and with a plain description of how to draw it by hand. No blank worksheet has been added; add it only if hand-drawing is confirmed.")
print("register updated")
