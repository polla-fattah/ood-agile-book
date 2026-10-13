from cleanup_lib import *

edits = [
 (3, "Chapter_03_Code_Explanations_and_Solutions.md",
  "Martin (2002) and Rubin (2012) are cited with the publication details given in the module descriptor and were not independently looked up.",
  "Martin (2002) and Rubin (2012) are cited in the student chapter; this book treats Agile practices and Scrum in Chapter 3 and sprint planning in Chapter 4."),
 (4, "Chapter_04_Code_Explanations_and_Solutions.md",
  "Martin (2002) and Rubin (2012) use the publication details given in the module descriptor and were not independently looked up.",
  "Martin (2002) and Rubin (2012) are cited in the student chapter; this book treats sprint planning and iteration evidence in Chapter 4, and Scrum in Chapter 3."),
 (8, "Chapter_08_Creating_and_Connecting_Objects.md",
  "The classic book is a bibliographic foundation; the linked publisher excerpts are the portions inspected online, not a claim to have accessed the entire book in this session.",
  "The design patterns used here are treated in this chapter and, for the behavioural patterns, in Chapter 9."),
 (9, "Chapter_09_Designing_Changing_Behaviour.md",
  "The classic book is a bibliographic foundation, not a claim that its complete text was accessed in this session.",
  "The behavioural patterns used here are treated in this chapter."),
 (10, "Chapter_10_Code_Explanations_and_Solutions.md",
  "Not opened for this chapter; publication details are from the module descriptor.",
  "This book treats package design in Section 10.4 of Chapter 10."),
 (10, "Chapter_10_From_Classes_to_Application_Structure.md",
  "The book itself was not opened for this chapter, and its publication details come from the module descriptor.",
  "This chapter treats package design in Section 10.4."),
 (11, "Chapter_11_Refactoring_and_Legacy_Code.md",
  "the Week 10 reading is its refactoring chapter. Not opened for this chapter; publication details come from the module descriptor.",
  "the Week 10 reading is its refactoring chapter. This chapter treats refactoring in Sections 11.5 and 11.6."),
 (11, "Chapter_11_Refactoring_and_Legacy_Code.md",
  "Not opened; the working definition of legacy code and of a seam are Feathers's, and the characterisation-testing description was checked against source 3.",
  "The working definition of legacy code and of a seam are Feathers's, and the characterisation-testing description was checked against source 3. This chapter treats legacy code, characterisation tests and seams in Sections 11.1, 11.3 and 11.4."),
 (13, "Chapter_13_Integration_Delivery_and_Feedback.md",
  "Not re-opened for this chapter; the features were exercised by the project's own build.",
  "This book treats JUnit tests in Chapter 7 and the use of test tags in Section 13.4."),
 (13, "Chapter_13_Integration_Delivery_and_Feedback.md",
  "Not opened for this chapter; publication details come from the module descriptor.",
  "This book treats testing in Chapter 7 and integration and end-to-end testing in Sections 13.1 to 13.3."),
 (13, "Chapter_13_Integration_Delivery_and_Feedback.md",
  "The module's recommended reading for Week 12 (selected chapters). Not opened.",
  "The module's recommended reading for Week 12 (selected chapters). This chapter treats pipelines, delivery and deployment in Sections 13.4 and 13.5."),
 (13, "Chapter_13_Code_Explanations_and_Solutions.md",
  " Sources 10–12 are not re-opened here.",
  ""),
 (14, "Chapter_14_Responding_to_Change_and_Handing_Over.md",
  "The handbook itself was not opened.",
  "This chapter treats retrospectives in Section 14.5."),
 (14, "Chapter_14_Responding_to_Change_and_Handing_Over.md",
  "Not opened for this chapter; publication details come from the module descriptor.",
  "Chapters 2 to 13 of this book cover the material to review, and this chapter shows how to evidence it."),
 (14, "Chapter_14_Code_Explanations_and_Solutions.md",
  " Source 10 is not re-opened here.",
  ""),
 (15, "Chapter_15_AI_as_a_Software_Engineering_Assistant.md",
  "Only the abstract page was read.",
  "This chapter treats dependencies in Section 15.7."),
]
done = []
for chapter, name, old, new in edits:
    replace_once(name, old, new, chapter, "Source note ('not opened' wording)", evidence=True)
    done.append((chapter, name, old, new))

with LOG.open("a", encoding="utf8", newline="\n") as handle:
    handle.write("## 'Not opened' source notes: decision (b), remove and point to this book's chapters\n\n")
    handle.write("- Decided by the module leader after the first cleanup: remove the `not opened` notes and put a pointer to this book's own chapters in their place. The removed wording is in each chapter's evidence file.\n")
    for chapter, name, old, new in done:
        handle.write(f"- Chapter {chapter}, `{name}`: `{old.strip()[:90]}...` became `{new.strip()[:110] or '(removed)'}`\n")
    handle.write("- Not changed: the lines that only say `Publication details as listed in the module descriptor` (Chapters 2-9) because they do not say that the book was not read. Chapter 12 was not edited.\n\n")
print(len(done), "notes changed")
