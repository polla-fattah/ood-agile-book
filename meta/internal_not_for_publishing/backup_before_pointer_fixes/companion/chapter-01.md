---
title: "Chapter 1 Companion: Code, Explanations and Solutions"
weight: 10
---

*Companion to Chapter 1: Developing Software That Can Change*  
*OO Development and Agile Practices*

This file brings together the chapter's Java code, explanations, suggested solutions and teaching notes. All code is included directly below; no archive or separate source files are needed to read it. To run an example, copy each complete listing into the filename shown above it.

The solutions are intended for the instructor or for students after attempting the activities. They support the existing chapter and do not introduce a new assessment. The Java examples are small orientation exercises, not the complete Campus Equipment Lending System.

## 1 Java code and explanations

### 1.1 The reservation rule

**Filename: `ReservationRules.java`**

```java
public final class ReservationRules {
    public boolean mayRequest(int activeReservations, int requestedDays) {
        return activeReservations >= 0
                && activeReservations < 3
                && requestedDays >= 1
                && requestedDays <= 7;
    }
}
```

The method answers whether two supplied numbers satisfy the initial student policy. The count is measured before adding a proposed reservation. A maximum of three active reservations therefore requires the existing count to be less than three.

| Expression or declaration | Meaning |
|---|---|
| `public final class ReservationRules` | Declares an accessible class that cannot be subclassed; `final` does not itself make a class's instances immutable |
| `public boolean mayRequest(...)` | Declares an accessible method that returns `true` or `false` |
| `int activeReservations` | Receives the existing count; it does not retrieve or update that count |
| `int requestedDays` | Receives the requested integer duration in days |
| `activeReservations >= 0` | Rejects an invalid negative count |
| `activeReservations < 3` | Allows another reservation only when the current count is below the limit |
| `requestedDays >= 1` | Rejects zero and negative durations |
| `requestedDays <= 7` | Includes the seven-day boundary in the permitted range |
| `&&` | Requires every condition to be true; evaluation stops when a condition is false |

For `mayRequest(2, 7)`, all four conditions hold. For `mayRequest(3, 7)`, the second condition fails. The method has no fields to modify and makes no database or service calls. It does not identify a borrower, check equipment availability or record a reservation.

### 1.2 Calling the rule

**Filename: `Chapter01Demo.java`**

```java
public class Chapter01Demo {
    public static void main(String[] args) {
        ReservationRules rules = new ReservationRules();
        System.out.println(rules.mayRequest(2, 7));
        System.out.println(rules.mayRequest(3, 7));
    }
}
```

`new ReservationRules()` creates the object on which the method is called. The first call uses a permitted count and the maximum permitted duration. The second call uses an existing count that has already reached the limit. Printing the returned values makes the difference visible without building a user interface.

From a directory containing both files, use a Java Development Kit:

```sh
javac ReservationRules.java Chapter01Demo.java
java Chapter01Demo
```

Expected output:

```text
true
false
```

The first call does not increase any count. Each call evaluates only its own supplied arguments. Consequently, calling `mayRequest(2, 7)` repeatedly returns the same result; the complete application would have to update its reservation records separately.

### 1.3 Repeatable checks

**Filename: `Chapter01Checks.java`**

This instructor example makes the expected results explicit. It needs no testing library and is not intended to teach the full testing approach introduced in Chapter 7.

```java
public class Chapter01Checks {
    public static void main(String[] args) {
        ReservationRules rules = new ReservationRules();
        // Explicit expected results derived from the chapter's initial rules.
        int[][] cases = {
            {0, 1, 1},
            {2, 7, 1},
            {3, 1, 0},
            {1, 8, 0},
            {-1, 1, 0},
            {1, 0, 0},
            {3, 7, 0},
            {0, 7, 1},
            {2, 1, 1},
            {4, 2, 0},
            {1, -1, 0},
            {0, 14, 0}
        };
        for (int[] example : cases) {
            boolean expected = example[2] == 1;
            boolean actual = rules.mayRequest(example[0], example[1]);
            if (actual != expected) {
                throw new AssertionError(
                    "mayRequest(" + example[0] + ", " + example[1]
                    + ") expected " + expected + " but got " + actual);
            }
        }
        System.out.println("All " + cases.length + " chapter checks passed.");
    }
}
```

Each row contains an existing count, a requested duration and an expected result. In this small data table, `1` means expected `true` and `0` means expected `false`. The last value is converted to a Boolean before comparison; this is a convenience for the example, not a general domain-modelling recommendation.

The loop calls the rule for each row and compares the actual result with the expectation. If they differ, it throws an `AssertionError` with the input and both results. This explicit exception works without enabling Java's optional `assert` statements. The runner stops at the first mismatch.

Compile and run all three files:

```sh
javac ReservationRules.java Chapter01Demo.java Chapter01Checks.java
java Chapter01Demo
java Chapter01Checks
```

The check runner's successful output is:

```text
All 12 chapter checks passed.
```

These checks cover the diagnostic cases and several nearby boundaries. They do not prove that the larger application is correct, and they do not test the future staff policy, which the original class does not implement.

## 2 A deliberate fault and its correction

Make a temporary copy of the source before trying this example. Inside `mayRequest`, change only the final comparison:

```java
// Deliberately faulty replacement expression, not a complete class.
&& requestedDays < 7;
```

The modified class still compiles, but it rejects a seven-day request. For an existing count of two and a requested duration of seven, the original returns `true` while the faulty version returns `false`.

Recompile the temporary copy and run `Chapter01Checks`. Its first failing case reports:

```text
mayRequest(2, 7) expected true but got false
```

The correction is to restore `requestedDays <= 7`. The requirement includes seven days, so the expectation comes from the stated policy. A check using only a two-day request would not distinguish the two versions.

### An additional count-boundary example

Consider a different edit: replacing `activeReservations < 3` with `activeReservations <= 3`. A borrower who already has three active reservations would then be permitted to request another. Running `Chapter01Checks` against this version stops at the first affected row:

```text
mayRequest(3, 1) expected false but got true
```

The case `mayRequest(3, 7)` would also fail, but the runner stops at the first mismatch, and `(3, 1)` appears earlier in the table. This illustrates why we test the point where a new request would exceed the total allowance.

## 3 Suggested solutions and teaching notes

### Suggested facilitation

Start by asking students to explain what “the program works” means in the opening scenario. Ask for one successful case, then one case that should be rejected. Reveal the staff change and let students identify what information is missing from the method.

Use paper tracing or a short live demonstration for the code. Give students time to predict the output before running it. Ask a second student to review the reason for the answer rather than merely announce agreement.

Complete the AI critique using the supplied teaching response, which is constructed for the exercise and labelled as such in the chapter. Live AI access is optional and unnecessary. Do not present the fixture as evidence about a real model's measured performance. Finish by asking each student for one specific next learning action.

Use the Common mistakes table in Section 1.8 of the chapter as a debrief: ask students which row they were closest to making during the diagnostic.

### Diagnostic answers

### Task A

| Call | Expected result | Reason |
|---|---|---|
| `mayRequest(0, 1)` | `true` | Count and duration are within the permitted ranges |
| `mayRequest(2, 7)` | `true` | Two existing reservations permit one more; seven days is inclusive |
| `mayRequest(3, 1)` | `false` | Three existing reservations already reach the limit |
| `mayRequest(1, 8)` | `false` | Eight days exceeds the student duration limit |
| `mayRequest(-1, 1)` | `false` | A negative count is explicitly rejected |
| `mayRequest(1, 0)` | `false` | The duration must be at least one day |

The class is `ReservationRules`; the method is `mayRequest`; both parameters are `int`; the return type is `boolean`. There are no fields, assignments to shared state, storage calls or reservation creation operations. Calling the method neither increments a count nor reserves equipment. Its returned value is narrower than overall eligibility or confirmation.

Avoid teaching that `final` makes all Java objects immutable. Here it prevents subclassing. The absence of mutable state and the body of the method explain the relevant absence of state changes.

### Task B

`mayRequest(2, 7)` distinguishes the implementations. The original returns `true`; the faulty `< 7` implementation returns `false`. The original agrees with the explicit inclusive maximum of seven days. Any input using seven days and a valid count from zero to two is an acceptable counterexample.

The supplied checks also catch an accidental `< 3` to `<= 3` change, through the cases with three existing reservations. A passing check suite is evidence for these selected cases, not proof of every aspect of a future reservation application.

### Task C

Students should preserve a maximum of three active reservations and seven requested days for students, while supporting five and fourteen for staff. Counts are measured before the new reservation is added. Some trustworthy representation of borrower category is required; an additional Boolean or category parameter can demonstrate the idea, but real callers must not grant privileges merely because a user claims a category.

Suitable unresolved questions include the treatment of unknown categories, how category is obtained, or whether someone holding both roles uses one particular policy. Do not require students to guess the institution's policy.

Useful acceptance examples for the changed rule include:

| Category | Existing count | Days | Numeric-rule decision |
|---|---:|---:|---|
| Student | 2 | 7 | Allow |
| Student | 3 | 1 | Reject |
| Student | 0 | 8 | Reject |
| Staff | 4 | 14 | Allow |
| Staff | 5 | 1 | Reject |
| Staff | 0 | 15 | Reject |

Four well-chosen examples are enough for the student task; they should cover both categories and meaningful limits. Negative counts and non-positive durations remain invalid for both. These decisions still do not establish availability.

The evidence statement should name checks that could fail, not only reassurance. A strong answer might read: “I would need the six acceptance examples to give the expected results, the original student checks to still pass unchanged, and a reviewer to confirm from the diff that student limits were not edited. This would not show that the category is trustworthy, that availability is checked, or that the examples match the equipment officer’s intent.” Weak answers say only that the code works or that all tests pass.

A small conditional with an explicit category is an acceptable initial approach. Its advantage is directness; a cost is that repeated category conditions may spread if more policy decisions appear. Passing limits into a shared calculation can also be reasonable, but moves the obligation to select and validate those limits to a caller. Accept either with a coherent rationale. Do not reward early creation of an interface hierarchy just for using patterns.

### AI activity answers

The numeric comparisons and Boolean result in the supplied explanation are supported by the code. The database claim is false as a claim about this method: its body has only comparisons and a return expression. It receives neither an item identifier nor a period, and performs no call to any database or availability service.

The larger application's availability behaviour is unknown from this class. Strong answers distinguish “this method does not query a database” from “the whole application never queries a database.”

An acceptable corrected explanation is: “The method returns true when the supplied count is non-negative and below three, and the requested duration is from one to seven days inclusive. It does not change state or create a reservation. Availability and the accuracy of the supplied count must be handled elsewhere.”

### Review-question guidance

1. A rule duplicated across several screens and services may pass today's examples but require coordinated edits tomorrow. Name the risk of inconsistent copies rather than simply calling the code ugly.
2. An iteration is a repeated period of development and feedback. An increment adds usable capability, such as a reservation flow. One iteration might refine that flow without adding a new feature, so the terms are not interchangeable.
3. Tests cover selected expectations. A test that incorrectly expects students to borrow for fourteen days could pass alongside an equally incorrect implementation. Compare expectations with the clarified policy.
4. Allowing staff fourteen days adds behaviour. Reorganising the same rule without changing its observable outcomes is refactoring. Knowing the intention helps a reviewer decide whether a changed result is a defect or an intended feature.
5. A student with zero active reservations requesting eight days should still be rejected. Replacing all limits with staff limits would accept that request. Staff-only checks do not protect student behaviour.
6. Tests and implementation may share the same misunderstood requirement. Review expected results independently against agreed examples, especially category distinctions and boundaries, then execute the relevant checks.

### Transfer-challenge guidance

One acceptable assumption is that durations are supplied as positive whole hours and counts refer to active confirmed bookings before adding another. Other clearly stated duration models are acceptable. Students should raise the policy for unknown groups and define what “active” means.

A society with two active bookings requesting one hour must be rejected; a department with the same count and duration may be allowed under the numeric rules. A society with zero bookings requesting three hours provides another useful distinction. Checks of room availability need a room identity and a requested time interval; count and duration alone cannot establish that a room is free.

### Readiness and feedback

Do not convert the checklist into an unannounced assessment. A syntax gap suggests focused Java revision. Correct tracing with weak explanations suggests peer walkthroughs. A tendency to infer database behaviour from a name suggests more exercises separating local behaviour from system assumptions.

Useful feedback names the reasoning gap: “You used the staff limit for the student case” is more actionable than “Your answer lacks understanding.” Ask students to revise one answer after feedback so the chapter's feedback loop becomes an experienced practice.

### Scope and continuity checks

- The orientation example is intentionally smaller than the complete project. It introduces no full reservation storage or date model.
- The student edition contains no unseen assessment change variant. The staff variation is an introductory worked teaching case.
- Full TDD belongs in Chapter 7, SOLID in Chapters 5–6, and systematic refactoring in Chapter 11.
- The chapter refers to later chapters and to Appendices A, B and E as navigation. Those appendices must exist before the book is published; until then, treat the references as open dependencies.
- The chapter labels its activity as Book project work, keeps the orientation example outside the cumulative codebase, and points to Chapter 15 (Section 15.1) before the AI activity, as Blueprint v0.3 requires.
- The critical review remains governed by the current module brief. No new AI-use policy or grading rubric is introduced.

## 4 Use in later chapters

Chapter 1 asks students to plan the staff change, not implement a complete redesign. Suggested acceptance examples and design alternatives therefore appear in the solutions without adding a premature implementation. Later chapters will develop the running system, introduce more explicit responsibilities, and test the resulting changes.