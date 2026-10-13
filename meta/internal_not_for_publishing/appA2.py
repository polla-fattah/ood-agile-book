from cleanup_lib import *

M = "Appendix_A_Programming_Readiness_and_Notation.md"
C = "Appendix_A_Code_Explanations_and_Solutions.md"
C1 = "Chapter_01_Developing_Software_That_Can_Change.md"
C2 = "Chapter_02_Object_Oriented_Development_Beyond_Syntax.md"

# 5. pointers in Chapters 1 and 2
replace_once(C1, "Appendix A is planned to add a short Java refresher.",
             "Appendix A has a short Java refresher and a readiness diagnostic.")
replace_once(C1, "(Appendix A will add a refresher)", "(Appendix A has a refresher)")
replace_once(C2, "Appendix A is planned to add a short refresher.", "Appendix A has a short refresher.")

# 6. small fixes in Appendix A
replace_once(M, "It neither changes the project nor depends on a particular Chapter 11 baseline.",
             "It neither changes the project nor depends on any of its checkpoints.")
replace_once(M, "A dependency need not mean “no field exists”: an association also implies reliance on another type. The diagram normally shows the more informative structural relationship rather than duplicating it with a second line. Navigation expresses a modelling decision and can be implemented in more than one way.",
             "A class that holds another type in a field depends on that type too, but the diagram normally shows only the more informative association and not a second dependency line for the same pair. Use a dependency arrow for a weaker link, such as a method that only uses the type as a parameter or a local variable. Navigation expresses a modelling decision and can be implemented in more than one way.")
replace_once(C, "2. The official Java, UML and Mermaid references listed in the main appendix support the corresponding syntax explanations.",
             "The Java, UML and Mermaid references that support the syntax explanations are listed in the main appendix.")

with LOG.open("a", encoding="utf8", newline="\n") as handle:
    handle.write("## Appendix A follow-up (pointers and small fixes)\n\n")
    for entry in [
        "Chapter 1: `Appendix A is planned to add a short Java refresher.` is now `Appendix A has a short Java refresher and a readiness diagnostic.`; `(Appendix A will add a refresher)` is now `(Appendix A has a refresher)`.",
        "Chapter 2: `Appendix A is planned to add a short refresher.` is now `Appendix A has a short refresher.`",
        "Appendix A manuscript: `a particular Chapter 11 baseline` is now `any of its checkpoints`; the dependency sentence in A.8 was rewritten (a field implies a dependency, but the diagram shows only the association; a dependency arrow is for a weaker link such as a parameter or local variable).",
        "Appendix A companion: References item 2 (not a reference) became a plain sentence that the supporting references are listed in the main appendix.",
    ]:
        handle.write("- " + entry + "\n")
    handle.write("\n")
print("done")
