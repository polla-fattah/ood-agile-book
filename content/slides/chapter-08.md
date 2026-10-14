---
title: "Chapter 8: Creating and Connecting Objects"
description: "Object Oriented Development and Agile Practices (SE506)"
weight: 80
type: slides
layout: page
---

# Chapter 8: Creating and Connecting Objects
### SE506: Object Oriented Development and Agile Practices
**Dr. Polla Abdulhamid Fattah**  
*Department of Computer Science & Artificial Intelligence*  
*University of Kurdistan Hewlêr (UKH)*

---

## Chapter Roadmap (1 of 3)

* **8.1 When does creating an object become a design problem?**
  * Creation, compatibility and added behaviour are different problems.
* **8.2 Factory Method: letting subclasses choose what to create**
  * An overridable creation hook inside an inherited workflow.
* **8.3 Abstract Factory: products that must belong together**
  * Related product roles that must vary together.
* **8.4 Builder: configuring a value you can trust**
  * Configure, validate, publish an immutable value.

---

## Chapter Roadmap (2 of 3)

* **8.5 Adapter: translating an outside system into your own terms**
  * The one pattern wired into the project: a directory adapter.
* **8.6 Decorator: adding behaviour around an operation**
  * Optional behaviour around an operation; order and failure matter.
* **8.7 When the simpler option is the better one**
  * A decision another developer can challenge.
* **8.8 Classifying an AI's pattern suggestions before accepting them** classify before accepting.

---

## Chapter Roadmap (3 of 3)

* **8.9 Pattern habits that mislead**
* **8.10 Try it yourself: the directory boundary and pattern exercises**
  * Nine steps; step 9 is on your team's project.
* **8.11 Questions to think with, and a transfer challenge**
  * A library application with numeric category codes.
* **What to take away, and what comes next**
  * Chapter 9: changing behaviour with behavioural patterns.

---

## Learning Outcomes (1 of 2)

By the end of this chapter, you should be able to:

1. **Identify a concrete construction or interface-compatibility problem.**
2. **Distinguish Factory Method, a simple factory and Abstract Factory** by their responsibilities.
3. **Build a validated immutable request** through a staged construction interface.

---

## Learning Outcomes (2 of 2)

4. **Adapt provider records, absence and failures** into an application-owned contract.
5. **Compose decorators** and predict the effects of order and exception handling.
6. **Justify adopting or declining a pattern** using tests and change costs.

---

## Module Connection and Prerequisites

* Supports **LO2**. The **midterm remains on Chapters 2 to 7**: these patterns are **not added** to that scope.
* **Prerequisites:** Chapters 5 to 7: contracts, interfaces, constructor injection, composition, meaningful tests. Java 17 and the Chapter 7 Maven/JUnit setup.
* Readings: the Factory and Adapter chapters of Martin, and the creational and structural patterns in Gamma et al.
* All provider records are **synthetic**. No real directory, network service or personal data.

---

## How to Use This Chapter

* **Core reading:** 8.1, 8.2, 8.5 and 8.7. **Factory Method** and **Adapter** are the two suggested live demonstrations.
* **Working-knowledge reading:** 8.3 (Abstract Factory), 8.4 (Builder), 8.6 (Decorator). Read each, run its example and, for the decorator, **predict both audit histories before you run the tests**. Working knowledge is not optional, but asks for understanding, not independent implementation.
* **Minimum lab:** steps 1 to 3, 5 and 9. This is midterm week: **do the minimum lab first**.
* **If you want more:** steps 4 and 6 to 8.

---

## Opening Problem

* The office wants borrower categories to come **from a university directory**, not supplied by the calling code.
* The proposed directory returns records containing **`S`, `T`, `Y` and `N`**.
* It **returns null** when a person is missing and **throws its own exception** when lookup fails.

---

## Two Proposals, Neither Argued

* **Proposal 1:** put these details inside `ReservationCoordinator`. It spreads **external conventions into reservation behaviour**.
* **Proposal 2:** a factory, builder, adapter and decorator **around every class**. It introduces structures **before identifying what must vary**.
* The useful question: **which responsibility needs a boundary, and what is the smallest design that makes that boundary clear?**
* The answer adds **one justified Adapter** to the running project.

---

# 8.1 When Does Creating an Object Become a Design Problem?
### Three problems that all get called "factory"

---

## Start With the Ordinary Constructor

* Creating a `LoanPeriod` with two required dates is clear: the constructor validates a small invariant.
* Replacing it with a hierarchy of factories **would not improve the rule**.
* Chapter 6's `ReservationApplication.create(sender)` is a useful **assembly function**: it connects known policies, a formatter and a supplied sender.

---

## When Construction Becomes Troublesome

* The decision about **which object**, **which compatible group**, or **which configuration** is **repeated across places that should not own it**.
* A caller needs only an export operation yet **inspects an output-format flag** each time.
* Another picks a heading renderer and a body renderer **independently** and combines incompatible formats.
* A third passes **six positional arguments** whose meanings are hard to review.

---

## Different Problems, One Misleading Name

* Giving all three solutions the name "factory" **conceals which responsibility changed**.
* A pattern name should **shorten a precise explanation after the problem is understood**. It should not replace that explanation.

---

## Creation, Compatibility, Added Behaviour

| Pattern | Concerned with |
|---|---|
| Factory Method, Abstract Factory, Builder | Construction decisions |
| Adapter | Connecting an existing interface to the one a client needs |
| Decorator | Attaching an optional responsibility while keeping the component interface |

* These categories organise discussion. **Actual code must still be examined for intent and consequences.**

---

## The Directory Request Is a Translation Problem

* The awkwardness is **not** that constructing a directory object needs many arguments.
* It is that its **data and failure meanings differ from the application's**.
* A builder would not answer **what `T` means** or **whether an outage is a missing borrower**. Those are translation decisions.
* Similarly, an audit wrapper around a sender adds behaviour **without choosing the sender's class**. Calling it a factory distracts from **call order and errors**.

---

## State the Change Pressure Before the Structure

A useful design note names:

1. the **current simple solution**,
2. the **change it handles poorly**,
3. the **selected boundary**,
4. the **cost** of adding it.

* Here: passing a trusted category worked for local examples; provider codes now need **central translation**; an **application-owned directory interface** isolates it; additional types and mapping tests are the cost.

---

## Do Not Predict Every Future Directory

* There is **already one incompatible interface**.
* Inventing five hypothetical provider families is **not evidence that an Abstract Factory is needed today**.
* Keep construction **visible at the composition point**: hiding it in a global registry can make dependencies harder to discover.
* The goal is **understandable ownership**, not a ban on constructors.

---

# 8.2 Factory Method
### Letting subclasses choose what to create

---

## A Simple Factory Is Often Enough

* The isolated export example: validate an input, obtain an exporter, execute it.
* A **simple factory** can choose a plain-text or HTML exporter from a flag. That is often enough **when one assembly location owns the choice**.
* The Factory Method scenario assumes **subclasses must specialise product creation** while keeping the workflow inherited from a common creator.
* The pressure is an **extension point in the workflow**, not merely two product classes.

---

## The Structure

```java
public abstract static class ExportJob {
    protected abstract Exporter createExporter();

    public final String run(String value) {
        Objects.requireNonNull(value, "value");
        return createExporter().export(value);
    }
}
```

* `run` owns the workflow and **is `final`**. The protected hook is the **deliberate variation point**.

---

## The Two Creators

```java
public static final class PlainJob extends ExportJob {
    @Override protected Exporter createExporter() { return value -> "TEXT: " + value; }
}
public static final class HtmlJob extends ExportJob {
    @Override protected Exporter createExporter() { return value -> "<p>" + escape(value) + "</p>"; }
}
```

* The products are lambdas in this compact example. They **still implement the product interface**.

---

## Figure 8.1: Factory Method

<!--svg:ch08-fig81-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 255" role="img" aria-label="Figure 8.1, Factory Method: the abstract ExportJob owns the workflow run and declares the protected createExporter hook. PlainJob and HtmlJob extend it and override the hook. ExportJob creates and uses an Exporter." style="display:block;width:100%;height:calc(var(--u) * 25.50);margin:0 auto">
<defs><marker id="ch08-fig81-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-fig81-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-fig81-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-fig81-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-fig81-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="40.0" y="10.0" width="330.0" height="114.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M42.0,66.0 L42.0,16.0 Q42.0,12.0 46.0,12.0 L364.0,12.0 Q368.0,12.0 368.0,16.0 L368.0,66.0 Z" fill="#e6eef6"/>
<text x="205.0" y="29.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">«abstract»</text>
<text x="205.0" y="51.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">ExportJob</text>
<line x1="40.0" y1="66.0" x2="370.0" y2="66.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="52.0" y="88.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+run(value) String</text>
<text x="52.0" y="111.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">#createExporter() Exporter</text>
<rect x="10.0" y="195.0" width="170.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,231.0 L12.0,201.0 Q12.0,197.0 16.0,197.0 L174.0,197.0 Q178.0,197.0 178.0,201.0 L178.0,231.0 Z" fill="#e6eef6"/>
<text x="95.0" y="220.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">PlainJob</text>
<rect x="230.0" y="195.0" width="170.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M232.0,231.0 L232.0,201.0 Q232.0,197.0 236.0,197.0 L394.0,197.0 Q398.0,197.0 398.0,201.0 L398.0,231.0 Z" fill="#e6eef6"/>
<text x="315.0" y="220.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">HtmlJob</text>
<rect x="580.0" y="10.0" width="270.0" height="91.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M582.0,66.0 L582.0,16.0 Q582.0,12.0 586.0,12.0 L844.0,12.0 Q848.0,12.0 848.0,16.0 L848.0,66.0 Z" fill="#e6eef6"/>
<text x="715.0" y="29.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">«interface»</text>
<text x="715.0" y="51.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Exporter</text>
<line x1="580.0" y1="66.0" x2="850.0" y2="66.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="592.0" y="88.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+export(value) String</text>
<path d="M95.0,195.0 L95.0,124.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch08-fig81-tri)"/>
<path d="M315.0,195.0 L315.0,124.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch08-fig81-tri)"/>
<path d="M370.0,62.0 L580.0,62.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch08-fig81-open)"/>
<text x="475.0" y="48.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">creates and uses</text>
<text x="75.0" y="164.0" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">extends</text>
</svg>
</div>
<!--/svg-->

---

## Reading the Notation

* `#` marks a **protected** member: subclasses can override `createExporter`, outside callers cannot call it.
* `<<abstract>>` marks a class that **cannot be instantiated** on its own.
* A solid line with a hollow triangle is **inheritance**.
* The dashed arrow is a **dependency**: `ExportJob` creates and uses exporters without keeping one in a field.
* It is Factory Method **because subclasses vary creation inside an inherited workflow**.

---

## Compare With a Simple Factory Honestly

```java
public static Exporter simpleExporter(boolean html) {
    return html ? value -> "<p>" + escape(value) + "</p>"
                : value -> "TEXT: " + value;
}
```

* An ordinary selection expression. A **simple factory**, not Factory Method.
* A static method named `create` is **not sufficient evidence** of the pattern.

---

## Same Output, Different Mechanism

```java
new PatternExamples.PlainJob().run("R1");
PatternExamples.simpleExporter(false).export("R1");
```

* Both can produce `TEXT: R1`. Identical output **does not make their extension mechanisms identical**.
* One central selection function **changes when an option is added**; the other **introduces a concrete creator subclass**.
* Code structure and change requirements **settle the classification**.

---

## Factory Method: Test, Trade-Off and Non-Use

* Tests exercise both concrete jobs and an **instrumented creator** whose hook returns a distinctive exporter: the inherited workflow uses the chosen product; null input is rejected before export.
* The hook-count assertion documents this tiny example. It is **not advice to verify private call counts** throughout the application.
* Factory Method gives an explicit extension point but creates **inheritance coupling**: readers follow the inherited workflow and its override.

---

## When to Decline It

* A constructor accepting an `Exporter` can be **simpler** when callers already know the product and need no creation hook.
* So the running project **keeps `ReservationApplication.create(sender)`** as a simple assembly function.
* We do not convert it into a creator hierarchy **solely to display the pattern**.
* The separate example demonstrates the mechanism; the design decision **explains when to decline it**.

---

# 8.3 Abstract Factory
### Products that must belong together

---

## The Problem

* A receipt has two product roles: a **heading renderer** and a **body renderer**.
* Plain text needs plain versions of both; an HTML fragment needs HTML versions of both.
* **Independent format flags** can accidentally select an HTML heading and a plain body.
* A simple attempt is **one renderer that switches format for every part**: for two tiny operations that may remain the best implementation.

---

## The Structure

* `ReceiptFamily` exposes `heading()` and `body()`.
* `PlainFamily` supplies plain implementations of both roles; `HtmlFamily` supplies HTML ones.
* The `receipt` function obtains both products from the supplied family and combines them. **No format switch.**
* The essential distinction is **the related set of product roles**. Abstract Factory is not just a factory declared with Java's `abstract` keyword.

---

## The Family

<!--svg:ch08-family-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 265" role="img" aria-label="Abstract Factory: the ReceiptFamily interface creates a Heading and a Body. PlainFamily and HtmlFamily realise it and supply matching renderers for both roles." style="display:block;width:100%;height:calc(var(--u) * 26.50);margin:0 auto">
<defs><marker id="ch08-family-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-family-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-family-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-family-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-family-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="290.0" y="10.0" width="290.0" height="114.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M292.0,66.0 L292.0,16.0 Q292.0,12.0 296.0,12.0 L574.0,12.0 Q578.0,12.0 578.0,16.0 L578.0,66.0 Z" fill="#e6eef6"/>
<text x="435.0" y="29.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">«interface»</text>
<text x="435.0" y="51.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">ReceiptFamily</text>
<line x1="290.0" y1="66.0" x2="580.0" y2="66.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="302.0" y="88.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+heading() Heading</text>
<text x="302.0" y="111.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+body() Body</text>
<rect x="10.0" y="10.0" width="200.0" height="91.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M12.0,66.0 L12.0,16.0 Q12.0,12.0 16.0,12.0 L204.0,12.0 Q208.0,12.0 208.0,16.0 L208.0,66.0 Z" fill="#e6eef6"/>
<text x="110.0" y="29.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">«interface»</text>
<text x="110.0" y="51.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Heading</text>
<line x1="10.0" y1="66.0" x2="210.0" y2="66.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="22.0" y="88.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+render(text) String</text>
<rect x="660.0" y="10.0" width="200.0" height="91.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M662.0,66.0 L662.0,16.0 Q662.0,12.0 666.0,12.0 L854.0,12.0 Q858.0,12.0 858.0,16.0 L858.0,66.0 Z" fill="#e6eef6"/>
<text x="760.0" y="29.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">«interface»</text>
<text x="760.0" y="51.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">Body</text>
<line x1="660.0" y1="66.0" x2="860.0" y2="66.0" stroke="#1d588c" stroke-width="1.6"/>
<text x="672.0" y="88.0" font-size="15" font-family="'Plex Mono', ui-monospace, monospace" font-weight="400" fill="#172a42" text-anchor="start">+render(text) String</text>
<rect x="110.0" y="175.0" width="240.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M112.0,211.0 L112.0,181.0 Q112.0,177.0 116.0,177.0 L344.0,177.0 Q348.0,177.0 348.0,181.0 L348.0,211.0 Z" fill="#e6eef6"/>
<text x="230.0" y="200.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">PlainFamily</text>
<rect x="520.0" y="175.0" width="240.0" height="36.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2.2"/>
<path d="M522.0,211.0 L522.0,181.0 Q522.0,177.0 526.0,177.0 L754.0,177.0 Q758.0,177.0 758.0,181.0 L758.0,211.0 Z" fill="#e6eef6"/>
<text x="640.0" y="200.0" font-size="19" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">HtmlFamily</text>
<path d="M290.0,62.0 L210.0,62.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch08-family-open)"/>
<text x="250.0" y="84.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">creates</text>
<path d="M580.0,62.0 L660.0,62.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch08-family-open)"/>
<text x="620.0" y="48.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">creates</text>
<path d="M230.0,175.0 L230.0,124.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch08-family-tri)"/>
<path d="M640.0,175.0 L640.0,124.0" fill="none" stroke="#1d588c" stroke-width="2.2" stroke-dasharray="7 5" marker-end="url(#ch08-family-tri)"/>
<text x="435.0" y="250.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">receipt(family, title, detail) uses only the interfaces: it holds no format switch.</text>
</svg>
</div>
<!--/svg-->

---

## Family Consistency Is Encouraged, Not Proven

* Our types encourage consistency by accepting **one factory for a receipt**.
* They do **not** prevent someone writing a defective factory that returns a **mixed pair**.
* Tests and review still establish that the concrete family **fulfils its promise**.

---

## Test the Relationship

* Render a complete receipt with each family: `Loan` and `R1` as separate text lines in one; an HTML heading and paragraph in the other.
* An angle-bracket input checks the **HTML text-node escaping** (`&`, `<`, `>`). These are fragments, not a website or a general sanitiser.
* A test that merely asserts both product references are **non-null** would miss a mixed-format family.
* The expected **complete result** observes the relationship that motivated the design.

---

## Trade-Off: Which Axis Becomes Easy?

* Adding **another family** (say Markdown) can leave the client workflow unchanged: one new implementation supplying both roles.
* Adding a **new product role** (a footer) changes the factory contract: **every family must supply it**.
* One axis of extension becomes convenient by making another **more coordinated**.

---

## Do Not Infer a Family From Proximity

* A **clock** and a **borrower directory** constructed near each other do not form a compatible product family.
* One sender with two implementations does not justify **two product roles invented for the diagram**.
* In the lending version, the small assembly function remains sufficient.
* If the real receipt stays this small, **one formatter per output style** is a reasonable conclusion.

---

# 8.4 Builder
### Configuring a value you can trust

---

## The Problem: Configuration Hard to Read

* A report request: a **required borrower identifier**, an **optional date interval**, a **returned-loan option**, an **ordered list of column labels**.
* A positional constructor works, but calls with nulls, a boolean and a list become **hard to review** as options grow.
* A sequence of **setters on the final request** lets clients observe an incomplete request and **change it after submission**.

---

## The Structure

```java
var request = ReportRequest.forBorrower("B1")
        .during(start, start.plusDays(7))
        .includeReturned(true)
        .column("item")
        .column("date")
        .build();
```

* Named operations configure a **mutable builder**; `build()` produces an **immutable request**.

---

## Configure, Validate, Publish

<!--svg:ch08-builder-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 270" role="img" aria-label="A fluent builder collects settings (forBorrower, during, includeReturned, column) and build() validates them and copies the column list to publish an immutable ReportRequest." style="display:block;width:100%;height:calc(var(--u) * 27.00);margin:0 auto">
<defs><marker id="ch08-builder-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-builder-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-builder-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-builder-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-builder-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="15.0" width="430.0" height="235.0" rx="12" fill="#f5f7fa" stroke="#b4762e" stroke-width="2" stroke-dasharray="9 6"/>
<text x="28.0" y="45.0" font-size="17" font-family="Inter, system-ui, sans-serif" font-weight="700" fill="#b4762e" text-anchor="start">Builder (mutable, one construction sequence)</text>
<rect x="28.0" y="62.0" width="394.0" height="28.0" rx="5" fill="#ffffff" stroke="#c3cfdd" stroke-width="1.6"/>
<text x="40.0" y="82.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="start">forBorrower("B1")</text>
<rect x="28.0" y="96.0" width="394.0" height="28.0" rx="5" fill="#ffffff" stroke="#c3cfdd" stroke-width="1.6"/>
<text x="40.0" y="116.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="start">.during(start, start.plusDays(7))</text>
<rect x="28.0" y="130.0" width="394.0" height="28.0" rx="5" fill="#ffffff" stroke="#c3cfdd" stroke-width="1.6"/>
<text x="40.0" y="150.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="start">.includeReturned(true)</text>
<rect x="28.0" y="164.0" width="394.0" height="28.0" rx="5" fill="#ffffff" stroke="#c3cfdd" stroke-width="1.6"/>
<text x="40.0" y="184.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="start">.column("item")</text>
<rect x="28.0" y="198.0" width="394.0" height="28.0" rx="5" fill="#ffffff" stroke="#c3cfdd" stroke-width="1.6"/>
<text x="40.0" y="218.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="start">.column("date")</text>
<path d="M440.0,132.0 L530.0,132.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch08-builder-arr)"/>
<text x="485.0" y="118.0" font-size="18" font-family="'Plex Mono', monospace" font-weight="700" fill="#1d588c" text-anchor="middle">build()</text>
<text x="485.0" y="158.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">validate,</text>
<text x="485.0" y="176.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">copy lists</text>
<rect x="530.0" y="40.0" width="330.0" height="190.0" rx="10" fill="#e6eef6" stroke="#1d588c" stroke-width="2.4"/>
<text x="695.0" y="74.0" font-size="20" font-family="'Chakra Petch', sans-serif" font-weight="700" fill="#1d588c" text-anchor="middle">ReportRequest</text>
<text x="695.0" y="98.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="middle" font-style="italic">immutable</text>
<text x="552.0" y="130.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="start">borrowerId</text>
<text x="552.0" y="155.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="start">from / toExclusive</text>
<text x="552.0" y="180.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="start">includeReturned</text>
<text x="552.0" y="205.0" font-size="16" font-family="'Plex Mono', monospace" font-weight="400" fill="#172a42" text-anchor="start">columns = List.copyOf(...)</text>
</svg>
</div>
<!--/svg-->

---

## What Kind of Builder This Is

* A **fluent builder with one product representation**.
* The classical Builder discussion also separates construction steps from representations and, when useful, a **director** controlling the steps. This example does **not** claim that.
* Chaining methods alone is insufficient: what matters is **staged construction followed by a validated, independent product**.

---

## Defaults and Invariants

* The required identifier must be **nonblank**.
* Omitting dates means **no date restriction**; supplying dates requires a **positive half-open interval**.
* Returned loans are **excluded by default**.
* Column labels form an **ordered list**, empty by default. The example stores labels but implements **no report generation**.

---

## Validation Before Publication

* `build()` checks the interval; the constructor copies the builder's column list with `List.copyOf`.
* Further builder changes **cannot change a previously built request**.
* The builder is **mutable and used for one sequence at a time**. An immutable product does not make its builder thread-safe.
* Settings **remain until changed** if the builder is reused.

---

## The Constructor's Checks

```java
if ((builder.from == null) != (builder.toExclusive == null)) {
    throw new IllegalArgumentException("Both dates or neither are required");
}
if (builder.from != null && !builder.from.isBefore(builder.toExclusive)) {
    throw new IllegalArgumentException("Positive interval required");
}
columns = List.copyOf(builder.columns);
```

* No partially valid request is ever returned.

---

## Builder: Test, Trade-Off and Non-Use

* Tests check defaults, explicit options, invalid dates, and the **independence of two products** built before and after another column is added. Attempting to modify a product's columns must **fail**.
* Checking only that chained calls compile **would not detect an alias to mutable builder state**.
* Costs: another type, more methods, a distinction between temporary state and a valid value.
* A small constructor with two meaningful required parameters is often clearer: **`LoanPeriod(start, endExclusive)` remains a constructor call**.

---

# 8.5 Adapter
### Translating an outside system into your own terms

---

## The Problem

* The provider exposes `lookup(key)` and returns `Person(key, kind, status)`.
* The application wants `find(borrowerId)` returning a domain `Borrower` **when an eligible record exists**.
* The mismatch includes **data meaning and failure behaviour**, not only method names.
* Provider codes inside the coordinator would make reservation logic **depend on their spelling**; repeating translation in callers risks **inconsistent defaults**.

---

## An Object Adapter

* It **implements the application interface** while **holding the incompatible provider** collaborator.
* The provider interface here is a **local model of an external contract**, not an HTTP client. A map-backed example makes every case reproducible.
* A real client later needs **provider-specific integration tests**.

---

## Agree the Translation Contract First (1 of 2)

| Provider outcome | Application outcome |
|---|---|
| Same identifier, kind `S`, status `Y` | Present student borrower |
| Same identifier, kind `T`, status `Y` | Present staff borrower |
| Null row | Empty result: borrower absent |
| Recognised kind, same identifier, status `N` | Empty result: borrower inactive |

---

## Agree the Translation Contract First (2 of 2)

| Provider outcome | Application outcome |
|---|---|
| Unknown or null kind or status; mismatched identifier | `DirectoryException`: invalid provider data |
| Provider's declared `Failure` | `DirectoryException` retaining the cause |
| Unexpected programming exception | Propagates; never converted into absence |

* Codes are **exact and case-sensitive**. `T` means staff only because **this teaching contract says so**. No trimming, normalising or defaulting.

---

## Error Precedence Is Part of the Contract

* The adapter validates the returned **identifier and category before interpreting inactivity**.
* So an **inactive row with an unknown kind is still malformed**: `Person("B1", "X", "N")` is an error, not an empty result.
* Covered by a test; **another policy would need an explicit decision**.

---

## The Application-Owned Contract

* `BorrowerDirectory` belongs to the **application's vocabulary**; `LegacyDirectoryAdapter` implements it and delegates to `LegacyDirectoryClient`.
* `Borrower` is an **immutable** identifier/category value.
* `Optional<Borrower>` expresses a **legitimate empty lookup**; an **exception** expresses **inability to obtain a trustworthy result**.
* `Optional` represents presence or absence. It does **not** define which failures should become absence.

---

## The Adapter's `find` (1 of 2)

```java
LegacyDirectoryClient.Person row;
try {
    row = client.lookup(borrowerId);
} catch (LegacyDirectoryClient.Failure failure) {
    throw new DirectoryException("Borrower directory unavailable", failure);
}
if (row == null) return Optional.empty();
if (!borrowerId.equals(row.key())) throw new DirectoryException("Mismatched borrower id");
```

---

## The Adapter's `find` (2 of 2)

```java
BorrowerCategory category;
if ("S".equals(row.kind())) category = BorrowerCategory.STUDENT;
else if ("T".equals(row.kind())) category = BorrowerCategory.STAFF;
else throw new DirectoryException("Unsupported borrower category");
if ("N".equals(row.status())) return Optional.empty();
if (!"Y".equals(row.status())) throw new DirectoryException("Unsupported borrower status");
return Optional.of(new Borrower(row.key(), category));
```

---

## The New Entry Point

* `DirectoryReservationService` validates the local identifier, item and date, **looks up the borrower**, and calls the existing coordinator **only after obtaining a valid domain borrower**.
* The caller supplies **no category** to this entry point.
* The coordinator still owns borrowing limits, interval conflicts, storage and notification.

---

## The Service's `reserve`

```java
Objects.requireNonNull(start, "start");
var found = directory.find(borrowerId);
if (found.isEmpty()) return "Rejected: borrower not found or inactive.";
Borrower borrower = found.get();
if (!borrowerId.equals(borrower.id())) {
    throw new DirectoryException("Directory returned a different borrower");
}
return coordinator.reserve(borrower.id(), itemId, start, days, borrower.category());
```

---

## Reading a Sequence Diagram

* A class diagram shows **what exists**; a sequence diagram shows **what happens**, in time order from top to bottom.
* Each box at the top is a **participant**; the vertical line below it is its **lifeline**.
* A **solid arrow is a call**; a **dashed arrow is a return**.
* A frame labelled `alt`, split by `else`, shows **alternative paths**: exactly one happens in a given run.
* A note spans the participants it concerns.

---

## Figure 8.2: An Active Borrower

<!--svg:ch08-seq-ok-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 262" role="img" aria-label="Sequence for an active valid borrower: the service asks the adapter, the adapter asks the provider, the provider returns a record, the adapter returns a domain borrower, and the service calls the coordinator with the mapped category." style="display:block;width:100%;height:calc(var(--u) * 26.20);margin:0 auto">
<defs><marker id="ch08-seq-ok-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-seq-ok-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-seq-ok-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-seq-ok-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-seq-ok-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="25.0" y="6.0" width="160.0" height="50.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="105.0" y="26.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">Reservation</text>
<text x="105.0" y="46.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">service</text>
<path d="M105.0,56.0 L105.0,254.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<rect x="260.0" y="6.0" width="160.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="340.0" y="26.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Directory</text>
<text x="340.0" y="46.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">adapter</text>
<path d="M340.0,56.0 L340.0,254.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<rect x="495.0" y="6.0" width="160.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="575.0" y="26.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Provider</text>
<text x="575.0" y="46.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">client</text>
<path d="M575.0,56.0 L575.0,254.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<rect x="700.0" y="6.0" width="160.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="780.0" y="36.3" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Coordinator</text>
<path d="M780.0,56.0 L780.0,254.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<path d="M109.0,88.0 L336.0,88.0" fill="none" stroke="#1d588c" stroke-width="2" marker-end="url(#ch08-seq-ok-arr)"/>
<text x="222.5" y="81.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">find(borrowerId)</text>
<path d="M344.0,118.0 L571.0,118.0" fill="none" stroke="#1d588c" stroke-width="2" marker-end="url(#ch08-seq-ok-arr)"/>
<text x="457.5" y="111.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">lookup(borrowerId)</text>
<path d="M571.0,148.0 L344.0,148.0" fill="none" stroke="#1d588c" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#ch08-seq-ok-arr)"/>
<text x="457.5" y="141.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">Person(B2, T, Y)</text>
<path d="M336.0,178.0 L109.0,178.0" fill="none" stroke="#1d588c" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#ch08-seq-ok-arr)"/>
<text x="222.5" y="171.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">Borrower(B2, STAFF)</text>
<path d="M109.0,208.0 L776.0,208.0" fill="none" stroke="#1d588c" stroke-width="2" marker-end="url(#ch08-seq-ok-arr)"/>
<text x="442.5" y="201.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">reserve(..., STAFF)</text>
<path d="M776.0,238.0 L109.0,238.0" fill="none" stroke="#1d588c" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#ch08-seq-ok-arr)"/>
<text x="442.5" y="231.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">existing reservation outcome</text>
</svg>
</div>
<!--/svg-->

---

## Figure 8.2: Missing, Inactive, or Failed

<!--svg:ch08-seq-fail-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 346" role="img" aria-label="Sequence for a missing or inactive borrower, or a declared provider failure: in both cases no reservation and no notification happen. Absence returns an empty result; a failure becomes a DirectoryException that keeps its cause." style="display:block;width:100%;height:calc(var(--u) * 34.60);margin:0 auto">
<defs><marker id="ch08-seq-fail-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-seq-fail-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-seq-fail-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-seq-fail-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-seq-fail-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="25.0" y="6.0" width="160.0" height="50.0" rx="8" fill="#0c2238" stroke="#0c2238" stroke-width="2"/>
<text x="105.0" y="26.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">Reservation</text>
<text x="105.0" y="46.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#ffffff" text-anchor="middle">service</text>
<path d="M105.0,56.0 L105.0,338.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<rect x="260.0" y="6.0" width="160.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="340.0" y="26.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Directory</text>
<text x="340.0" y="46.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">adapter</text>
<path d="M340.0,56.0 L340.0,338.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<rect x="495.0" y="6.0" width="160.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="575.0" y="26.6" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Provider</text>
<text x="575.0" y="46.0" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">client</text>
<path d="M575.0,56.0 L575.0,338.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<rect x="700.0" y="6.0" width="160.0" height="50.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="780.0" y="36.3" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">Coordinator</text>
<path d="M780.0,56.0 L780.0,338.0" fill="none" stroke="#c3cfdd" stroke-width="2" stroke-dasharray="6 6"/>
<path d="M109.0,86.0 L336.0,86.0" fill="none" stroke="#1d588c" stroke-width="2" marker-end="url(#ch08-seq-fail-arr)"/>
<text x="222.5" y="79.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">find(borrowerId)</text>
<path d="M344.0,112.0 L571.0,112.0" fill="none" stroke="#1d588c" stroke-width="2" marker-end="url(#ch08-seq-fail-arr)"/>
<text x="457.5" y="105.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">lookup(borrowerId)</text>
<rect x="14.0" y="126.0" width="842.0" height="206.0" rx="6" fill="none" stroke="#b4762e" stroke-width="1.8"/>
<text x="24.0" y="144.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="700" fill="#b4762e" text-anchor="start">alt</text>
<path d="M571.0,160.0 L344.0,160.0" fill="none" stroke="#1d588c" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#ch08-seq-fail-arr)"/>
<text x="457.5" y="153.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">null, or status N</text>
<path d="M336.0,186.0 L109.0,186.0" fill="none" stroke="#1d588c" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#ch08-seq-fail-arr)"/>
<text x="222.5" y="179.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">Optional.empty()</text>
<rect x="35.0" y="196.0" width="815.0" height="28.0" rx="5" fill="#f6ead9" stroke="#b4762e" stroke-width="1.6"/>
<text x="442.5" y="216.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle" font-style="italic">no reservation, no notification</text>
<path d="M14.0,232.0 L856.0,232.0" fill="none" stroke="#b4762e" stroke-width="1.6" stroke-dasharray="7 5"/>
<text x="24.0" y="249.0" font-size="14.5" font-family="'Plex Mono', monospace" font-weight="700" fill="#b4762e" text-anchor="start">else  declared Failure</text>
<path d="M571.0,268.0 L344.0,268.0" fill="none" stroke="#1d588c" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#ch08-seq-fail-arr)"/>
<text x="457.5" y="261.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">Failure</text>
<path d="M336.0,294.0 L109.0,294.0" fill="none" stroke="#1d588c" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#ch08-seq-fail-arr)"/>
<text x="222.5" y="287.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle">DirectoryException (cause kept)</text>
<rect x="35.0" y="304.0" width="815.0" height="28.0" rx="5" fill="#f6ead9" stroke="#b4762e" stroke-width="1.6"/>
<text x="442.5" y="324.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#172a42" text-anchor="middle" font-style="italic">no reservation, no notification</text>
</svg>
</div>
<!--/svg-->

---

## What the Sequence Highlights

* The point **before which reservation state must remain untouched**.
* Malformed provider data follows the **same no-mutation boundary** as a provider failure, though its exception describes a different cause.
* Walk through `reserve("B2", "CAM1", 2026-10-20, 10)`: `lookup("B2")` returns `Person("B2", "T", "Y")`; `T` maps to `STAFF`; the unchanged coordinator applies the staff policy, stores **R1**, formats and makes its **one notification attempt**.

---

## The Demonstration Output

```text
Confirmed: R1 for B2 on CAM1 [2026-10-20, 2026-10-30).
Rejected: borrower limit or duration.
Rejected: borrower not found or inactive.
Reservations: 1
Notices: 1
```

* Staff B2 is allowed ten days; **student B1's ten-day request is rejected**; the missing identifier creates **no record**; only the accepted request creates a notice.

---

## A Data-Backed Collaborator

* **The directory is the book's data-backed collaborator**: the component that stands outside the application and answers from its own data.
* Chapter 1 promised it; Chapter 6 previewed its contract; Chapter 7 showed three doubles; **this chapter builds the adapter**; Chapter 10 places it in the application structure; Chapter 13 adds timeouts and an explicit **fallback-or-failure policy**.
* Here the provider is a **synthetic in-process example**: no transport, timeout or storage to fail.

---

## The Same Questions for a Model

* Any component returning **data or predictions** is in the same position, including one that calls a trained model.
* What does an **empty answer** mean? What counts as a **failure**? Which outputs will you **refuse to trust**? How will a test **substitute** the component?
* For an ML model-serving domain: your adapter sits between your service and the model runtime. Map its **label codes to your own types**; treat a **missing prediction and a timeout as different outcomes**; **reject values outside the documented range**.

---

## Rejection Is Not Failure

* A missing or inactive borrower produces the **explicit rejection string**.
* A directory outage throws **`DirectoryException`**.
* Returning "borrower not found" for both would **make an operational failure look like a valid eligibility decision**.
* **Defaulting to staff would be worse**: a longer loan without a trusted category.

---

## Order of Checks

* The service delegates **duration policy** to the coordinator, so lookup happens **before** deciding whether ten requested days are allowed.
* Local blank identifiers and a null start date **fail before lookup**.
* A deliberate, documented order, **not an accident of catch blocks**.

---

## An Entry Point, Not Authentication

* Knowing an identifier does **not** establish who the caller is or whether they may reserve for that person.
* The earlier coordinator APIs remain for trusted internal use, so callers **can bypass the directory**.
* A real exposed application needs a **controlled authenticated entry path** and reviewed authorisation rules.
* There is no caching, HTTP client, retry, persistence or cancellation in this increment.

---

## Test the Boundary and Its Cost

* Synthetic rows: both category mappings, absence, inactivity, unknown codes, null fields, identity mismatch, expected failure translation.
* A service test: a **staff** record permits ten days; a **student** record rejects ten days **using the same existing policies**.
* Failure tests inspect **state and notices**, then perform a valid request to show the failure **did not consume R1**.
* Unexpected exceptions are **not caught broadly**.

---

## The Cost of the Adapter

* A **mapping layer** and a contract that must evolve with provider changes.
* If two components already share the same interface and meaning, **direct injection is sufficient**.
* If they disagree on essential capabilities, **an adapter cannot supply them**.
* This implementation does not cache, retry, authenticate, persist or contact a real provider.

---

## Acceptance Mapping (1 of 2)

| Promise | Executable evidence |
|---|---|
| Known active codes map correctly | `mapsKnownActiveCategories` (two rows) |
| Missing and inactive rows yield absence | `absenceAndInactiveAreEmpty` |
| Unknown or differently cased codes are not defaulted | `unknownCodesAreErrors` (four rows) |
| Null fields, mismatch, malformed inactive rows are errors | `malformedRowsAreErrors` |

---

## Acceptance Mapping (2 of 2)

| Promise | Executable evidence |
|---|---|
| Invalid identifiers never reach the provider | `invalidIdentifierDoesNotReachProvider` (null, empty, blank) |
| Expected outage translated with its cause | `translatesExpectedFailureAndKeepsCause` |
| Unexpected failure remains visible | `unexpectedProgrammingFailureIsNotDisguisedAsAbsence` |
| Directory category selects the duration policy | `categoryFromDirectoryControlsReservationPolicy` |
| Absence and outage change nothing and keep R1 | `absenceAndOutageDoNotStoreNotifyOrConsumeId` |

---

# 8.6 Decorator
### Adding behaviour around an operation

---

## The Problem

* An isolated notification exercise needs **optional audit observations** and **a single retry after a declared delivery failure**.
* **Subclasses for every combination** multiply quickly. **Flags on one large sender** combine responsibilities and hide order.
* A Decorator **implements the same interface as its wrapped delegate** and adds behaviour around delegation.
* Java's `FilterInputStream` illustrates the wrapping mechanism: an input stream containing another input stream.

---

## The Two Decorators

```java
// AuditedSender.send
events.add("attempt");
try { delegate.send(message); }
catch (DeliveryFailure failure) { events.add("failed"); throw failure; }
events.add("sent");

// RetryOnceSender.send
try { delegate.send(message); }
catch (DeliveryFailure failure) { delegate.send(message); }
```

---

## Order Changes the Observations

<!--svg:ch08-decorators-->
<div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 870 300" role="img" aria-label="Two compositions of the same decorators around a delegate that fails once and then succeeds. Audit outside retry records attempt and sent. Retry outside audit records attempt, failed, attempt, sent. Both make two delegate calls." style="display:block;width:100%;height:calc(var(--u) * 30.00);margin:0 auto">
<defs><marker id="ch08-decorators-tri" viewBox="0 0 16 16" refX="15" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L15,8 L1,15 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-decorators-dia" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#f5f7fa" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-decorators-diaf" viewBox="0 0 22 14" refX="1" refY="7" markerWidth="22" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,7 L11,1 L21,7 L11,13 Z" fill="#1d588c" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-decorators-open" viewBox="0 0 16 16" refX="14" refY="8" markerWidth="16" markerHeight="16" markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L14,8 L2,14" fill="none" stroke="#1d588c" stroke-width="2"/></marker><marker id="ch08-decorators-arr" viewBox="0 0 14 14" refX="13" refY="7" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto"><path d="M0,1 L13,7 L0,13 Z" fill="#1d588c"/></marker></defs>
<rect x="10.0" y="25.0" width="150.0" height="70.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="85.0" y="65.3" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">AuditedSender</text>
<rect x="190.0" y="25.0" width="150.0" height="70.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="265.0" y="65.3" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">RetryOnceSender</text>
<rect x="370.0" y="25.0" width="150.0" height="70.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="445.0" y="46.8" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">delegate:</text>
<text x="445.0" y="64.9" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">fails once,</text>
<text x="445.0" y="83.1" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">then succeeds</text>
<path d="M160.0,60.0 L190.0,60.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch08-decorators-arr)"/>
<path d="M340.0,60.0 L370.0,60.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch08-decorators-arr)"/>
<text x="548.0" y="47.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">events:</text>
<text x="548.0" y="71.0" font-size="15" font-family="'Plex Mono', monospace" font-weight="600" fill="#172a42" text-anchor="start">attempt → sent</text>
<text x="548.0" y="93.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">one logical call · 2 delegate calls</text>
<rect x="10.0" y="160.0" width="150.0" height="70.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="85.0" y="200.3" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">RetryOnceSender</text>
<rect x="190.0" y="160.0" width="150.0" height="70.0" rx="6" fill="#ffffff" stroke="#1d588c" stroke-width="2"/>
<text x="265.0" y="200.3" font-size="15.5" font-family="Inter, system-ui, sans-serif" font-weight="600" fill="#172a42" text-anchor="middle">AuditedSender</text>
<rect x="370.0" y="160.0" width="150.0" height="70.0" rx="8" fill="#f6ead9" stroke="#b4762e" stroke-width="2"/>
<text x="445.0" y="181.8" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">delegate:</text>
<text x="445.0" y="199.9" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">fails once,</text>
<text x="445.0" y="218.1" font-size="14.5" font-family="Inter, system-ui, sans-serif" font-weight="500" fill="#172a42" text-anchor="middle">then succeeds</text>
<path d="M160.0,195.0 L190.0,195.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch08-decorators-arr)"/>
<path d="M340.0,195.0 L370.0,195.0" fill="none" stroke="#1d588c" stroke-width="2.2" marker-end="url(#ch08-decorators-arr)"/>
<text x="548.0" y="182.0" font-size="15" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">events:</text>
<text x="548.0" y="206.0" font-size="15" font-family="'Plex Mono', monospace" font-weight="600" fill="#172a42" text-anchor="start">attempt → failed → attempt → sent</text>
<text x="548.0" y="228.0" font-size="14" font-family="Inter, system-ui, sans-serif" font-weight="400" fill="#46586d" text-anchor="start" font-style="italic">every attempt audited · 2 delegate calls</text>
</svg>
</div>
<!--/svg-->

---

## Reading the Order

* **Audit outside retry:** audit observes **one logical call** whose internal retry succeeds.
* **Retry outside audit:** **each attempt passes through audit** separately.
* Neither event sequence is universally correct. Decide whether the audit requirement concerns **operations or individual attempts**.

---

## Failure Is Part of the Contract

* If both attempts fail, the **second failure propagates**; no third attempt.
* An unexpected `IllegalArgumentException` is **not retried**.
* Catching every exception would confuse **invalid input or programming defects** with the declared retryable condition.

---

## What the Stand-In Does Not Promise

* The audit list is an **in-memory observation example**, not durable audit storage.
* If a real audit sink can fail, decide whether to propagate that failure, preserve the original delivery failure, or report it separately.
* A real sender may deliver and then **lose the acknowledgement**: a retry can **duplicate the effect**. This toy has no idempotency key.
* "Sent" means only that **the delegate returned normally**.
* A same-signature wrapper is **not automatically behaviourally substitutable** under every error policy.

---

## Decorator: Test, Trade-Off and Non-Use

* Tests assert **both event sequences**, the **two-attempt bound**, and propagation of expected and unexpected failures.
* The decorators stay **isolated**. Chapter 6's notification contract says **one attempt, no automatic retry**: installing this retry there **would change that contract**. A pattern name does not authorise it.
* Use one straightforward sender when optional combinations are unnecessary. Decorators add **another path to trace** and can obscure which layer handles an error.

---

# 8.7 When the Simpler Option Is the Better One
### A decision aid, not a rule

---

## Compare by the Decision Isolated (1 of 2)

| Observed pressure | Candidate | Simpler alternative |
|---|---|---|
| Subclasses must create a workflow's product | Factory Method | Inject a ready product into the workflow |
| Related product roles must vary together | Abstract Factory | One formatter or one assembly function |
| Many named options configure an immutable value | Builder | A clear constructor or named creation method |

---

## Compare by the Decision Isolated (2 of 2)

| Observed pressure | Candidate | Simpler alternative |
|---|---|---|
| Provider interface and meanings differ | Adapter | Direct injection if the contracts already match |
| Optional responsibilities compose around one interface | Decorator | One explicit implementation with fixed behaviour |

* Explain **who owns the variation, how failures travel, and how the structure changes future edits**.

---

## What the Running Project Gained

* Chapter 8 adds the directory-backed reservation service, domain borrower and provider adapter.
* The Chapter 7 **coordinator, policies, availability query, loan service and notification implementations remain unchanged**. The original test suite stays in the build.
* New claims: a staff example can request ten days through a **category-free entry point**; a student cannot; missing or inactive borrowers are rejected **before storage**; provider failures are **identifiable** and leave state untouched.

---

## The Inherited Limits Remain

* Returned loans **do not remove reservations**, free their intervals or restore counted allowances.
* The project still runs **in memory within one process**.
* Pattern work does **not** resolve these separate requirements.
* The build executes **63 JUnit invocations**: 35 inherited, 17 directory-boundary cases and 11 pattern cases.

---

## Record a Decision Another Developer Can Challenge

> Provider codes and null/error conventions differ from the application. An object adapter translates them behind `BorrowerDirectory`. This keeps provider details out of reservation policy, at the cost of mapping tests and explicit provider-contract maintenance.

* Then **name what was declined**.

---

## What Was Declined

* The assembly function needs **no creator hierarchy**.
* No related provider **product family** is required.
* The core value objects **do not need builders**.
* Retry **would change the notification promise**.
* Declining those structures is **part of the design outcome**.
* If the only explanation is "this chapter teaches the pattern", keep it **in the teaching examples**, not the running system.

---

# 8.8 Classifying an AI's Pattern Suggestions Before Accepting Them
### Names do not make patterns

---

## Ground Rules for the Activity (1 of 2)

| | For this activity |
|---|---|
| Your goal | Classify each suggested structure by what it actually does, and decide which are justified |
| You start with | The isolated pattern examples, the directory contract in 8.5 and the Chapter 6 notification contract |
| What is in bounds | Classify, correct and decline; wire no pattern into the application without a requirement |

---

## Ground Rules for the Activity (2 of 2)

| | For this activity |
|---|---|
| How to check | The source (is there a subclass hook?), the mapping table, tests for unknown codes, outage, immutability and decorator order |
| How to decide | A verdict with a structural or behavioural reason for each claim |
| No AI account? | The ready-made example is enough |

---

## The Ready-Made Example (1 of 2)

**Author-written fictional AI output.**

> Rename the static `create` function to `FactoryMethod` and it becomes Factory Method. Add an Abstract Factory even though there is only one product role. The adapter should catch every exception and return a staff borrower to keep the system available.

---

## The Ready-Made Example (2 of 2)

> Wrap all senders in retry decorators; order does not matter. A builder means the finished object is immutable even if it retains the builder's mutable list.

* Identify the unsupported claims. For each, name the **missing requirement or structural evidence** and a **concrete test**.

---

## Solution (1 of 2)

| Fictional claim | Diagnosis and correction |
|---|---|
| Renaming static `create` makes Factory Method | Names do not create a subclass hook: compare `simpleExporter` with `ExportJob.createExporter` |
| One product role requires Abstract Factory | No related set has been established: keep simple assembly |
| Catch every exception and return staff | Hides failure and **grants an unsupported category** |

---

## Solution (2 of 2)

| Fictional claim | Diagnosis and correction |
|---|---|
| Wrap all senders with retry | Changes the one-attempt contract: keep retry isolated |
| Decorator order does not matter | Changes which layer observes each attempt: the two exact audit-history tests |
| A builder guarantees immutable products | Mutable aliases can remain after build: snapshot and unmodifiable-list tests |

* Pattern classification needs **source inspection as well as output tests**.

---

## Three Wrong Candidates to Diagnose

```java
// 1. an unfamiliar code silently acquires staff privileges
category = "S".equals(row.kind()) ? STUDENT : STAFF;

// 2. turns provider or programming failures into absence
catch (RuntimeException failure) { return Optional.empty(); }

// 3. the product shares the builder's mutable list
columns = builder.columns;
```

* Each was applied to a copy and **rejected by named tests**: `unknownCodesAreErrors`, `translatesExpectedFailureAndKeepsCause`, `builtValueIsIndependentOfReusableBuilder`.

---

# 8.9 Pattern Habits That Mislead
### Eight to avoid

---

## Mistakes 1 to 3

| Mistake | Consequence | Better question |
|---|---|---|
| Classify by names such as `create` or `Factory` | Misidentifies the extension mechanism | Which operation varies, and how? |
| Put provider codes inside borrowing policies | Couples business rules to provider representation | Where should translation live? |
| Treat absence and outage identically | Hides failure as an eligibility decision | Was a valid lookup completed? |

---

## Mistakes 4 to 6

| Mistake | Consequence | Better question |
|---|---|---|
| Assume a family interface prevents all mixing | Overstates guarantees | Do concrete factories return compatible products? |
| Keep the builder's mutable list | Previously built values can change | Does construction copy mutable state? |
| Assume decorator order is irrelevant | Changes audit meaning and failure visibility | Which calls pass through each layer? |

---

## Mistakes 7 and 8

| Mistake | Consequence | Better question |
|---|---|---|
| Install retries without revisiting the contract | Duplicate attempts or effects | What outcome does the existing promise allow? |
| Require all patterns in the semester project | Complexity without a problem | Which real change justifies this structure? |

---

# 8.10 Try It Yourself
### The directory boundary and pattern exercises

---

## Input and Demonstrations

* **You start with:** the Chapter 7 version, the synthetic provider contract and mapping table, and the Chapter 8 code file. Steps 1 to 8: the book's project; **step 9: your team's project.
* **Demonstrations:** first compare the **simple factory and the overridden creation hook**; then trace an **active borrower and a failed lookup** through the adapter boundary.
* **Guided practice:** add an independently chosen **malformed provider case** and explain why it produces failure, not absence. Run the decorator tests and **predict both audit histories first**.

---

## Independent Work: Steps 1 to 3

1. **Integrate the borrower-directory boundary** using the selected mapping contract.
2. Show **staff and student duration outcomes** without accepting a caller-supplied category at the new entry point.
3. Prove that **missing, malformed and failed lookups** create no reservations or notices.

---

## Independent Work: Steps 4 to 6 (Optional)

4. **Compare two designs** for a second scenario: injected exporter versus Factory Method, or constructor versus Builder.
5. Write a **problem-solution-consequence** decision, including a justified non-use case.
6. Inspect the **fictional AI answer** and retain independent verification of your corrections.

---

## Independent Work: Steps 7 to 9

7. **Builder exercise:** in the isolated `patterns` package, add an optional **maximum-row** setting. Absent by default; rejects zero and negative; does not change an already built request. **Write the tests first.**
8. **Decorator exercise:** add a third decorator that **counts attempts**. Predict the count for one failure then success when it sits **outside** the retry and **inside** it; check with tests.
9. On your team's project, find a place where your code uses an **external or mismatched interface directly**. Decide whether an adapter is justified using problem-solution-consequence, and say **what you would decline to build**.

---

## Builder Exercise: A Solution

```java
public Builder maximumRows(int value) {
    if (value <= 0) throw new IllegalArgumentException("Positive row limit required");
    maximumRows = OptionalInt.of(value);
    return this;
}
```

* `OptionalInt maximumRows = OptionalInt.empty();` in the builder; copied at construction.
* `OptionalInt` is immutable, so copying the reference **keeps a built request independent**.
* Absence is explicit. A sentinel such as `0` for "no limit" is **weaker**: it makes "zero rows" unrepresentable.

---

## Decorator Exercise: The Prediction

```java
public static final class CountingSender implements Sender {
    public void send(String message) {
        attempts.incrementAndGet();
        delegate.send(message);
    }
}
```

* One failure then success. A counter **outside** the retry sees one logical call: **1**. A counter **inside** sees both delegate attempts: **2**.
* The same order effect as the audit histories, **measured by a number**. With these three tests, `PatternExamplesTest` runs 14 tests.

---

## What You Should End Up With, and When You Are Done

* **What you should end up with:** runnable source and tests; a mapping table; a reproducible demonstration; a short design decision; the AI claims record; the two exercise solutions with tests; the step 9 note.
* **Accept when:** known codes map correctly; **unknown codes never grant a category**; provider outage is **distinct from absence**; legacy behaviour remains tested; the second comparison identifies **costs, not counts of classes**.
* **If you want more:** a changed provider code for staff, or a second provider. Do not add automatic fallback between providers without defining conflict, outage and identity semantics.

---

## An Example Decision Note

* **Problem:** the directory's `lookup`, raw codes, null absence and provider exception differ from the application's needs.
* **Solution:** an application-owned `BorrowerDirectory` and an object adapter; a service looks up a borrower **before** invoking the coordinator with the mapped category.
* **Consequences:** translation in **one tested boundary**; **several small types and mapping tests**; local examples cannot establish real-provider compatibility.
* **Revisit when:** a real SDK contract exists, an authenticated entry point is designed, or a requirement adds a **related family** of integration products.

---

# 8.11 Questions to Think with, and a Transfer Challenge
### Concept, diagnosis, transfer

---

## Concept Questions

1. What distinguishes the worked Factory Method from `simpleExporter`?
2. Why are two unrelated construction methods insufficient justification for Abstract Factory?
3. Which property makes the built report request independent of subsequent builder changes?
4. How do Adapter and Decorator differ even though both may contain another object?

---

## Diagnosis Questions

5. A directory adapter catches `RuntimeException` and returns an empty result. Describe at least two different failures this hides and the resulting problem for the application.
6. A team changes `Audit(Retry(sender))` to `Retry(Audit(sender))` because both satisfy `Sender`. Predict the audit histories for one failure followed by success and explain the requirement that selects between them.

---

## Guidance: Questions 1 and 2

1. `ExportJob` owns an **inherited workflow** and subclasses override a **creation hook**. `simpleExporter` **selects and returns a product in an ordinary function**. A method named `create` does not alone establish the former.
2. A genuine family needs **several product roles that must vary together for a compatibility reason** (heading and body share an output format). Constructing an unrelated clock and directory together does not.

---

## Guidance: Questions 3 and 4

3. The request **copies mutable builder state, validates before publication and exposes no mutation operation**. Returning a final reference to the builder's mutable list would not suffice.
4. **Adapter** translates one contract into the contract its client expects. **Decorator** keeps the component interface and adds optional responsibilities around delegation. **Holding another object is a mechanism, not a classification.**

---

## Guidance: Questions 5 and 6

5. It conceals **a legitimate provider outage** and **a programming defect** (say an unexpected illegal state). Both look like a completed lookup that found no borrower: a **misleading rejection**, and operators lose the cause.
6. Audit outside retry: `attempt, sent`. Retry outside audit: `attempt, failed, attempt, sent`. Choose the former when the record concerns **logical operations**, the latter when **every delivery attempt must be observed**.

---

## Transfer Challenge: A Library Application

A library application receives patron records from an external system using **numeric category codes** and a **separate inactive flag**.

* Design the **application-owned lookup contract**, an **adapter mapping** and **three failure cases**.
* Decide whether constructing its receipt output needs a **simple factory** or a **family factory**.
* Explain what **additional requirement would change your answer**.

---

## Transfer Guidance

* Obtain an **explicit provider mapping first**. Hypothetically: category 10 student, 20 staff, an inactive flag excludes an otherwise valid patron. Do not transplant the equipment example's string codes.
* An application-owned `PatronDirectory.find(id)`; immutable patron values; **eligibility policy stays outside the translation layer**.
* Failures: **unknown category**, **returned identifier differs**, **declared outage**: all prevent the borrowing operation before state changes; the outage keeps its cause.
* One renderer: direct injection or simple factory. **Several matching plain/HTML components: Abstract Factory** becomes a candidate.

---

# What to Take Away, and What Comes Next
### What to carry forward

---

## Summary

* **Factory Method** varies product creation through a subclass hook.
* **Abstract Factory** groups related product roles.
* **Builder** stages construction.
* **Adapter** translates incompatible contracts.
* **Decorator** composes optional responsibilities **whose order still matters**.
* Creation and connection patterns are useful **when they isolate a specific decision**.

---

## Where the Project Stands

* The running project now has a **tested directory-backed entry point**.
* The pattern examples stay **isolated** in the `patterns` package.
* Chapter 9 moves to **changing behaviour**, examining further patterns through concrete variation pressures and the same demand for evidence.

---

## Sources and Further Reading

1. **Gamma, Helm, Johnson, Vlissides:** *Design Patterns: Elements of Reusable Object-Oriented Software.*
2. **Gamma et al.:** the Abstract Factory and Adapter publisher excerpts.
3. **Oracle:** Java SE 17 `Optional` and `FilterInputStream`.
4. **JUnit Team:** JUnit 5.13.4 User Guide.
5. **Martin:** *Agile Software Development* (2002).

* Full references and links are in the chapter text.
