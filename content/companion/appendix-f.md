---
title: "Appendix F Companion: The Risk Lab"
weight: 260
description: "Code explanations and solutions for Appendix F Companion: The Risk Lab."
---

*Software Engineering for AI and Data Components*  
*OO Development and Agile Practices*

## 1. Scope and use

This file accompanies Appendix F, Software Engineering for AI and Data Components. It contains the **risk lab**, a small stand-alone Maven project, in two halves: the starting class and the acceptance tests for the exercise (Sections 2 and 3), and a model solution (Section 4). Attempt the exercise before you read Section 4.

The lab is an **isolated Book example**. It does not depend on the lending project and does not change it. It holds one question, “how risky is it to lend this item to this borrower?”, and puts a model behind it. There is no real model: the model is a local stub service, so that every test is deterministic.

Use a full Java 17 JDK and Maven 3.9.11. The lab uses only JUnit Jupiter 5.13.4, with the Compiler plugin 3.14.1 and the Surefire plugin 3.5.4, as in Appendix B. Save each listing at its path inside one new folder, for example `risk-lab`, and note that the two starter files and the tests are listed before the solution. From that folder:

```bash
bash scripts/check.sh
```

The script builds, runs every test, then runs the tests again without the `integration` group, so that the two counts can be reported separately. It accepts the same optional variables as the Appendix B starter: `CHAPTER_MVN` (the Maven command), `CHAPTER_M2` (a local repository folder) and `CHAPTER_OFFLINE=1`.

The starting class and its probe need no Maven. From the folder `starter`:

```bash
javac --release 17 -d out UnsafeRiskScorer.java StarterProbe.java
java -cp out StarterProbe
```

The starter's expected output, apart from the time, which varies:

```text
good day            : true
confidence of 1.7   : true
service that is slow: true after 1502 ms
service that is down: false
```

## 2. The starting point

### 2.1 `starter/UnsafeRiskScorer.java`

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URI;

/**
 * The starting point of the exercise. It works on a good day. Do not copy its habits: read it and
 * list what can go wrong before you run StarterProbe.
 */
public class UnsafeRiskScorer {
    private final String serviceUrl;

    public UnsafeRiskScorer(String serviceUrl) {
        this.serviceUrl = serviceUrl;
    }

    public boolean approve(String borrowerId, String itemId) {
        try {
            HttpURLConnection connection = (HttpURLConnection)
                    URI.create(serviceUrl + "/risk?borrower=" + borrowerId + "&item=" + itemId).toURL().openConnection();
            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            String line = in.readLine();
            String[] parts = line.split(" ");
            float score = Float.parseFloat(parts[1]);
            if (parts[0].equals("LOW")) {
                return score > 0.8f;
            }
            return false;
        } catch (Exception anything) {
            return false;
        }
    }
}
```

### 2.2 `starter/StarterProbe.java`

```java
import com.sun.net.httpserver.HttpServer;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;

/** Runs UnsafeRiskScorer against a small local service and prints what it does. */
public class StarterProbe {
    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0), 0);
        server.createContext("/risk", exchange -> {
            String query = exchange.getRequestURI().getQuery();
            String body = "LOW 0.95";
            if (query.contains("borrower=BADSCORE")) {
                body = "LOW 1.7";
            } else if (query.contains("borrower=SLOW")) {
                try {
                    Thread.sleep(1500);
                } catch (InterruptedException ignored) {
                    Thread.currentThread().interrupt();
                }
            }
            byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
            exchange.sendResponseHeaders(200, bytes.length);
            exchange.getResponseBody().write(bytes);
            exchange.close();
        });
        server.start();
        String url = "http://127.0.0.1:" + server.getAddress().getPort();
        UnsafeRiskScorer scorer = new UnsafeRiskScorer(url);

        System.out.println("good day            : " + scorer.approve("B1", "CAM1"));
        System.out.println("confidence of 1.7   : " + scorer.approve("BADSCORE", "CAM1"));
        long began = System.nanoTime();
        System.out.println("service that is slow: " + scorer.approve("SLOW", "CAM1")
                + " after " + (System.nanoTime() - began) / 1_000_000 + " ms");
        server.stop(0);
        System.out.println("service that is down: " + scorer.approve("B1", "CAM1"));
    }
}
```

## 3. The acceptance tests

These are the tests the exercise must pass. `Fixtures`, `FakeItemRiskAssessor` and `StubRiskService` are test support. The tests will not compile until you write the main code that Appendix F, Section F.7, describes.

### 3.1 `src/test/java/risk/support/Fixtures.java`

```java
package risk.support;

import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;
import risk.domain.RiskAssessment;
import risk.domain.RiskLevel;

/** Small shared test values. The clock is fixed so that no test depends on the time of day. */
public final class Fixtures {
    public static final Instant NOW = Instant.parse("2026-10-13T12:00:00Z");
    public static final Clock CLOCK = Clock.fixed(NOW, ZoneOffset.UTC);

    private Fixtures() {
    }

    public static RiskAssessment assessment(RiskLevel level, double confidence) {
        return new RiskAssessment(level, confidence, NOW);
    }
}
```

### 3.2 `src/test/java/risk/support/FakeItemRiskAssessor.java`

```java
package risk.support;

import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.atomic.AtomicInteger;
import risk.domain.ItemRiskAssessor;
import risk.domain.RiskAssessment;
import risk.domain.RiskAssessmentException;
import risk.domain.RiskLevel;

/** A deterministic, hand-written assessor for tests: no network, no model, and it counts its calls. */
public final class FakeItemRiskAssessor implements ItemRiskAssessor {
    private final Map<String, RiskAssessment> answers = new HashMap<>();
    private RiskAssessment defaultAnswer = Fixtures.assessment(RiskLevel.LOW, 0.95);
    private boolean failing;
    private final AtomicInteger calls = new AtomicInteger();

    public FakeItemRiskAssessor answer(String borrowerId, RiskAssessment assessment) {
        answers.put(borrowerId, Objects.requireNonNull(assessment));
        return this;
    }

    public FakeItemRiskAssessor defaultAnswer(RiskAssessment assessment) {
        this.defaultAnswer = Objects.requireNonNull(assessment);
        return this;
    }

    public FakeItemRiskAssessor failing() {
        this.failing = true;
        return this;
    }

    public int calls() {
        return calls.get();
    }

    @Override
    public RiskAssessment assessRisk(String borrowerId, String itemId) {
        calls.incrementAndGet();
        if (failing) {
            throw new RiskAssessmentException("The fake was told to fail.");
        }
        return answers.getOrDefault(borrowerId, defaultAnswer);
    }
}
```

### 3.3 `src/test/java/risk/support/StubRiskService.java`

```java
package risk.support;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/**
 * A controlled local risk service for tests: the JDK's own HTTP server on the loopback address and a
 * free port. Borrower LOWB answers {@code LOW 0.93}, MODB {@code MODERATE 0.70} and HIGHB
 * {@code HIGH 0.88}. BADSCORE answers a confidence of 1.7, BADLEVEL an unknown level, GARBAGE one field
 * and BROKEN status 500. SLOW sends nothing until the stub is closed, and SLOWBODY sends its headers and
 * the first byte and then holds the rest until the stub is closed. Everything else is 404. It is a
 * stand-in for a real service, not the service.
 */
public final class StubRiskService implements AutoCloseable {
    private final HttpServer server;
    private final CountDownLatch release = new CountDownLatch(1);
    private volatile String lastQuery = "";

    public StubRiskService() throws IOException {
        server = HttpServer.create(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0), 0);
        server.createContext("/risk", this::handle);
        server.start();
    }

    public URI baseUri() {
        return URI.create("http://127.0.0.1:" + server.getAddress().getPort());
    }

    /** The raw query of the last request, so a test can check what was sent. */
    public String lastQuery() {
        return lastQuery;
    }

    private void handle(HttpExchange exchange) throws IOException {
        String query = exchange.getRequestURI().getRawQuery();
        lastQuery = query == null ? "" : query;
        String borrower = "";
        for (String pair : lastQuery.split("&")) {
            if (pair.startsWith("borrower=")) {
                borrower = URLDecoder.decode(pair.substring("borrower=".length()), StandardCharsets.UTF_8);
            }
        }
        int status = 200;
        boolean stallBody = false;
        String body;
        switch (borrower) {
            case "LOWB" -> body = "LOW 0.93";
            case "MODB" -> body = "MODERATE 0.70";
            case "HIGHB" -> body = "HIGH 0.88";
            case "BADSCORE" -> body = "LOW 1.7";
            case "BADLEVEL" -> body = "EXTREME 0.50";
            case "GARBAGE" -> body = "only-one-field";
            case "BROKEN" -> { status = 500; body = "server error"; }
            case "SLOW" -> {
                awaitRelease();
                body = "LOW 0.93";
            }
            case "SLOWBODY" -> {
                stallBody = true;
                body = "LOW 0.93";
            }
            case "A B&C" -> body = "MODERATE 0.60";
            default -> { status = 404; body = "none"; }
        }
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        try {
            exchange.sendResponseHeaders(status, bytes.length);
            if (stallBody) {
                exchange.getResponseBody().write(bytes, 0, 1);
                exchange.getResponseBody().flush();
                awaitRelease();
                exchange.getResponseBody().write(bytes, 1, bytes.length - 1);
            } else {
                exchange.getResponseBody().write(bytes);
            }
        } catch (IOException clientGone) {
            // the client gave up (a timeout test); nothing more to send
        } finally {
            exchange.close();
        }
    }

    private void awaitRelease() {
        try {
            release.await(30, TimeUnit.SECONDS);
        } catch (InterruptedException interrupted) {
            Thread.currentThread().interrupt();
        }
    }

    @Override
    public void close() {
        release.countDown();
        server.stop(0);
    }
}
```

### 3.4 `src/test/java/risk/domain/RiskAssessmentTest.java`

```java
package risk.domain;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Instant;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import risk.support.Fixtures;

class RiskAssessmentTest {

    @ParameterizedTest
    @ValueSource(doubles = {-0.01, 1.01, Double.NaN, Double.POSITIVE_INFINITY})
    void confidenceOutsideZeroToOneIsRejected(double confidence) {
        assertThrows(IllegalArgumentException.class,
                () -> new RiskAssessment(RiskLevel.LOW, confidence, Fixtures.NOW));
    }

    @ParameterizedTest
    @ValueSource(doubles = {0.0, 0.5, 1.0})
    void confidenceAtTheEdgesIsAccepted(double confidence) {
        assertEquals(confidence, new RiskAssessment(RiskLevel.LOW, confidence, Fixtures.NOW).confidence());
    }

    @Test
    void aMissingLevelOrTimeIsRejected() {
        assertThrows(NullPointerException.class, () -> new RiskAssessment(null, 0.5, Fixtures.NOW));
        assertThrows(NullPointerException.class, () -> new RiskAssessment(RiskLevel.LOW, 0.5, (Instant) null));
    }

    @Test
    void automaticApprovalNeedsLowAndAtLeastTheThreshold() {
        assertTrue(Fixtures.assessment(RiskLevel.LOW, 0.80).permitsAutomaticApproval());
        assertFalse(Fixtures.assessment(RiskLevel.LOW, 0.79).permitsAutomaticApproval());
    }

    @ParameterizedTest
    @ValueSource(strings = {"MODERATE", "HIGH", "UNKNOWN"})
    void aLevelOtherThanLowNeverApprovesAutomatically(String level) {
        assertFalse(Fixtures.assessment(RiskLevel.valueOf(level), 1.0).permitsAutomaticApproval());
    }
}
```

### 3.5 `src/test/java/risk/domain/ReservationScreenTest.java`

```java
package risk.domain;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import risk.support.FakeItemRiskAssessor;
import risk.support.Fixtures;

class ReservationScreenTest {

    @ParameterizedTest
    @CsvSource({
            "LOW,    0.95, AUTO_APPROVE",
            "LOW,    0.80, AUTO_APPROVE",
            "LOW,    0.79, SUPERVISOR_REVIEW",
            "MODERATE, 0.99, SUPERVISOR_REVIEW",
            "UNKNOWN, 1.00, SUPERVISOR_REVIEW",
            "HIGH,   0.10, REJECT",
            "HIGH,   0.99, REJECT"})
    void eachAssessmentIsRoutedByTheDomainsRules(String level, double confidence, String expected) {
        FakeItemRiskAssessor fake = new FakeItemRiskAssessor()
                .defaultAnswer(Fixtures.assessment(RiskLevel.valueOf(level), confidence));
        assertEquals(Route.valueOf(expected), new ReservationScreen(fake).route("B1", "CAM1"));
    }

    @Test
    void aFailedAssessmentIsNeverTurnedIntoAnApproval() {
        ReservationScreen screen = new ReservationScreen(new FakeItemRiskAssessor().failing());
        assertThrows(RiskAssessmentException.class, () -> screen.route("B1", "CAM1"));
    }

    @Test
    void eachBorrowerIsAssessedOnTheirOwn() {
        FakeItemRiskAssessor fake = new FakeItemRiskAssessor()
                .answer("RISKY", Fixtures.assessment(RiskLevel.HIGH, 0.9));
        ReservationScreen screen = new ReservationScreen(fake);
        assertEquals(Route.REJECT, screen.route("RISKY", "CAM1"));
        assertEquals(Route.AUTO_APPROVE, screen.route("B1", "CAM1"));
    }

    @Test
    void blankOrMissingIdentifiersAreRejectedBeforeAnyAssessment() {
        FakeItemRiskAssessor fake = new FakeItemRiskAssessor();
        ReservationScreen screen = new ReservationScreen(fake);
        assertThrows(IllegalArgumentException.class, () -> screen.route(" ", "CAM1"));
        assertThrows(IllegalArgumentException.class, () -> screen.route("B1", null));
        assertEquals(0, fake.calls());
    }
}
```

### 3.6 `src/test/java/risk/adapter/RuleBasedRiskAssessorTest.java`

```java
package risk.adapter;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import risk.domain.RiskAssessment;
import risk.domain.RiskAssessmentException;
import risk.domain.RiskLevel;
import risk.support.Fixtures;

class RuleBasedRiskAssessorTest {

    private static RiskAssessment assess(int violations) {
        return new RuleBasedRiskAssessor(borrower -> violations, Fixtures.CLOCK).assessRisk("B1", "CAM1");
    }

    @ParameterizedTest
    @CsvSource({"0, LOW", "1, MODERATE", "2, MODERATE", "3, HIGH", "9, HIGH"})
    void theLevelFollowsTheNumberOfViolations(int violations, String expected) {
        assertEquals(RiskLevel.valueOf(expected), assess(violations).level());
    }

    @ParameterizedTest
    @CsvSource({"0, 1", "0, 3", "1, 2", "2, 3", "0, 8", "3, 4", "2, 9"})
    void moreViolationsNeverLowerTheRisk(int fewer, int more) {
        // a metamorphic property: it does not say what the level is, only how two answers relate
        assertTrue(assess(more).level().compareTo(assess(fewer).level()) >= 0);
    }

    @ParameterizedTest
    @CsvSource({"0", "1", "5"})
    void theCautiousFallbackNeverApprovesWithoutAPerson(int violations) {
        assertFalse(assess(violations).permitsAutomaticApproval());
    }

    @Test
    void aNegativeCountIsAFailureAndNotALowRisk() {
        assertThrows(RiskAssessmentException.class, () -> assess(-1));
    }
}
```

### 3.7 `src/test/java/risk/adapter/HttpRiskPredictionAdapterContractTest.java`

```java
package risk.adapter;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.net.URI;
import java.time.Duration;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import risk.domain.RiskAssessment;
import risk.domain.RiskAssessmentException;
import risk.domain.RiskLevel;
import risk.support.Fixtures;
import risk.support.StubRiskService;

/** The adapter against a real HTTP client and a service under our control: one test per outcome. */
@Tag("integration")
class HttpRiskPredictionAdapterContractTest {
    private static final Duration BOUND = Duration.ofMillis(300);

    private StubRiskService stub;
    private HttpRiskPredictionAdapter adapter;

    @BeforeEach
    void startStub() throws Exception {
        stub = new StubRiskService();
        adapter = new HttpRiskPredictionAdapter(stub.baseUri(), Duration.ofSeconds(1), BOUND, Fixtures.CLOCK);
    }

    @AfterEach
    void stopStub() {
        stub.close();
    }

    @Test
    void aGoodAnswerBecomesATypedAssessment() {
        RiskAssessment answer = adapter.assessRisk("LOWB", "CAM1");
        assertEquals(RiskLevel.LOW, answer.level());
        assertEquals(0.93, answer.confidence());
        assertEquals(Fixtures.NOW, answer.assessedAt());
    }

    @Test
    void theLevelAndConfidenceOfEachAnswerAreKept() {
        assertEquals(RiskLevel.MODERATE, adapter.assessRisk("MODB", "CAM1").level());
        assertEquals(RiskLevel.HIGH, adapter.assessRisk("HIGHB", "CAM1").level());
    }

    @Test
    void identifiersAreEncodedInTheRequest() {
        assertEquals(RiskLevel.MODERATE, adapter.assessRisk("A B&C", "CAM 1").level());
        assertTrue(stub.lastQuery().contains("borrower=A+B%26C"), stub.lastQuery());
        assertTrue(stub.lastQuery().contains("item=CAM+1"), stub.lastQuery());
    }

    @ParameterizedTest
    @ValueSource(strings = {"BADSCORE", "BADLEVEL", "GARBAGE", "BROKEN", "UNKNOWN-PERSON"})
    void everythingExceptAGoodAnswerIsAFailureAndNeverADefault(String borrower) {
        assertThrows(RiskAssessmentException.class, () -> adapter.assessRisk(borrower, "CAM1"));
    }

    @Test
    @Timeout(5)
    void aServiceThatSendsNothingIsGivenUpOnWithinTheBound() {
        long began = System.nanoTime();
        assertThrows(RiskAssessmentException.class, () -> adapter.assessRisk("SLOW", "CAM1"));
        assertTrue(elapsedMillis(began) < BOUND.toMillis() * 4, "waited too long");
    }

    @Test
    @Timeout(5)
    void aServiceThatStallsInTheMiddleOfTheBodyIsAlsoBounded() {
        long began = System.nanoTime();
        assertThrows(RiskAssessmentException.class, () -> adapter.assessRisk("SLOWBODY", "CAM1"));
        assertTrue(elapsedMillis(began) < BOUND.toMillis() * 4, "waited too long");
    }

    @Test
    void aServiceThatIsNotThereIsAFailure() {
        HttpRiskPredictionAdapter nobody = new HttpRiskPredictionAdapter(
                URI.create("http://127.0.0.1:1"), Duration.ofMillis(300), BOUND, Fixtures.CLOCK);
        assertThrows(RiskAssessmentException.class, () -> nobody.assessRisk("LOWB", "CAM1"));
    }

    private static long elapsedMillis(long beganNanos) {
        return (System.nanoTime() - beganNanos) / 1_000_000;
    }
}
```

### 3.8 `src/test/java/risk/adapter/ResilientRiskAssessorTest.java`

```java
package risk.adapter;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;
import risk.domain.ItemRiskAssessor;
import risk.domain.RiskAssessment;
import risk.domain.RiskAssessmentException;
import risk.domain.RiskLevel;
import risk.support.FakeItemRiskAssessor;
import risk.support.Fixtures;

class ResilientRiskAssessorTest {
    private static final Duration LIMIT = Duration.ofMillis(200);
    private static final RiskAssessment PRIMARY = Fixtures.assessment(RiskLevel.LOW, 0.95);
    private static final RiskAssessment CAUTIOUS = Fixtures.assessment(RiskLevel.MODERATE, 0.50);

    private static ItemRiskAssessor stalled(CountDownLatch release) {
        return (borrower, item) -> {
            try {
                release.await();
            } catch (InterruptedException interrupted) {
                Thread.currentThread().interrupt();
            }
            return PRIMARY;
        };
    }

    @Test
    void aTimelyPrimaryAnswerIsUsedAndTheFallbackIsNotTouched() {
        FakeItemRiskAssessor fallback = new FakeItemRiskAssessor().defaultAnswer(CAUTIOUS);
        try (ResilientRiskAssessor assessor = new ResilientRiskAssessor(
                new FakeItemRiskAssessor().defaultAnswer(PRIMARY), fallback, LIMIT)) {
            assertSame(PRIMARY, assessor.assessRisk("B1", "CAM1"));
            assertEquals(0, fallback.calls());
            assertEquals(0, assessor.fallbackCount());
        }
    }

    @Test
    @Timeout(5)
    void aStalledPrimaryIsGivenUpOnWithinTheLimitAndTheFallbackAnswers() {
        CountDownLatch never = new CountDownLatch(1);
        try (ResilientRiskAssessor assessor = new ResilientRiskAssessor(
                stalled(never), new FakeItemRiskAssessor().defaultAnswer(CAUTIOUS), LIMIT)) {
            long began = System.nanoTime();
            RiskAssessment answer = assessor.assessRisk("B1", "CAM1");
            long millis = (System.nanoTime() - began) / 1_000_000;
            assertSame(CAUTIOUS, answer);
            assertTrue(millis < LIMIT.toMillis() * 4, "waited " + millis + " ms");
            assertEquals(1, assessor.fallbackCount());
        } finally {
            never.countDown();
        }
    }

    @Test
    @Timeout(5)
    void aStalledPrimaryIsAskedToStop() throws InterruptedException {
        CountDownLatch askedToStop = new CountDownLatch(1);
        CountDownLatch never = new CountDownLatch(1);
        ItemRiskAssessor primary = (borrower, item) -> {
            try {
                never.await();
            } catch (InterruptedException interrupted) {
                askedToStop.countDown();
            }
            return PRIMARY;
        };
        try (ResilientRiskAssessor assessor = new ResilientRiskAssessor(
                primary, new FakeItemRiskAssessor().defaultAnswer(CAUTIOUS), LIMIT)) {
            assessor.assessRisk("B1", "CAM1");
            assertTrue(askedToStop.await(2, TimeUnit.SECONDS), "the stalled call was not asked to stop");
        } finally {
            never.countDown();
        }
    }

    @Test
    void anExpectedFailureOfThePrimaryLeadsToTheFallback() {
        try (ResilientRiskAssessor assessor = new ResilientRiskAssessor(
                new FakeItemRiskAssessor().failing(), new FakeItemRiskAssessor().defaultAnswer(CAUTIOUS), LIMIT)) {
            assertSame(CAUTIOUS, assessor.assessRisk("B1", "CAM1"));
            assertEquals(1, assessor.fallbackCount());
        }
    }

    @Test
    void aProgrammingErrorInThePrimaryIsNotHiddenByTheFallback() {
        ItemRiskAssessor buggy = (borrower, item) -> {
            throw new IllegalStateException("bug");
        };
        FakeItemRiskAssessor fallback = new FakeItemRiskAssessor().defaultAnswer(CAUTIOUS);
        try (ResilientRiskAssessor assessor = new ResilientRiskAssessor(buggy, fallback, LIMIT)) {
            assertThrows(IllegalStateException.class, () -> assessor.assessRisk("B1", "CAM1"));
            assertEquals(0, fallback.calls());
        }
    }

    @Test
    void ifTheFallbackAlsoFailsTheCallerSeesTheFailureAndNotAnApproval() {
        try (ResilientRiskAssessor assessor = new ResilientRiskAssessor(
                new FakeItemRiskAssessor().failing(), new FakeItemRiskAssessor().failing(), LIMIT)) {
            assertThrows(RiskAssessmentException.class, () -> assessor.assessRisk("B1", "CAM1"));
        }
    }

    @Test
    void aPrimaryThatReturnsNullIsABugAndIsReportedAsOne() {
        ItemRiskAssessor returnsNull = (borrower, item) -> null;
        try (ResilientRiskAssessor assessor = new ResilientRiskAssessor(
                returnsNull, new FakeItemRiskAssessor().defaultAnswer(CAUTIOUS), LIMIT)) {
            assertThrows(NullPointerException.class, () -> assessor.assessRisk("B1", "CAM1"));
        }
    }

    @Test
    @Timeout(5)
    void anInterruptedCallerKeepsItsInterruptFlagAndGetsAFailure() {
        CountDownLatch never = new CountDownLatch(1);
        try (ResilientRiskAssessor assessor = new ResilientRiskAssessor(
                stalled(never), new FakeItemRiskAssessor().defaultAnswer(CAUTIOUS), Duration.ofSeconds(5))) {
            Thread.currentThread().interrupt();
            assertThrows(RiskAssessmentException.class, () -> assessor.assessRisk("B1", "CAM1"));
            assertTrue(Thread.interrupted(), "the interrupt flag must be restored");
        } finally {
            never.countDown();
        }
    }
}
```

### 3.9 `src/test/java/risk/rollout/RolloutAssessorTest.java`

```java
package risk.rollout;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import risk.domain.RiskAssessment;
import risk.domain.RiskLevel;
import risk.support.FakeItemRiskAssessor;
import risk.support.Fixtures;

class RolloutAssessorTest {
    private static final RiskAssessment BASE = Fixtures.assessment(RiskLevel.MODERATE, 0.50);
    private static final RiskAssessment MODEL = Fixtures.assessment(RiskLevel.LOW, 0.95);

    private final List<ProvenanceRecord> records = new ArrayList<>();
    private final FakeItemRiskAssessor baseline = new FakeItemRiskAssessor().defaultAnswer(BASE);
    private final FakeItemRiskAssessor model = new FakeItemRiskAssessor().defaultAnswer(MODEL);

    private RolloutAssessor assessor(RolloutMode mode, int percent) {
        return new RolloutAssessor(baseline, model, mode, percent, "model-7", records::add);
    }

    @Test
    void whenOffTheBaselineDecidesAndTheModelIsNeverCalled() {
        assertSame(BASE, assessor(RolloutMode.OFF, 100).assessRisk("B1", "CAM1"));
        assertEquals(0, model.calls());
        assertTrue(records.isEmpty());
    }

    @Test
    void inShadowTheBaselineDecidesAndTheModelsAnswerIsOnlyRecorded() {
        assertSame(BASE, assessor(RolloutMode.SHADOW, 0).assessRisk("B1", "CAM1"));
        assertEquals(1, model.calls());
        ProvenanceRecord record = records.get(0);
        assertSame(MODEL, record.modelAnswer());
        assertSame(BASE, record.decision());
        assertFalse(record.modelDecided());
        assertEquals("model-7", record.modelVersion());
    }

    @Test
    void aShadowFailureNeverChangesTheDecisionAndIsRecordedAsNoAnswer() {
        FakeItemRiskAssessor broken = new FakeItemRiskAssessor().failing();
        RolloutAssessor shadow = new RolloutAssessor(baseline, broken, RolloutMode.SHADOW, 0, "model-7", records::add);
        assertSame(BASE, shadow.assessRisk("B1", "CAM1"));
        assertNull(records.get(0).modelAnswer());
    }

    @Test
    void whenOnTheModelDecidesAndTheRecordSaysSo() {
        assertSame(MODEL, assessor(RolloutMode.ON, 0).assessRisk("B1", "CAM1"));
        assertEquals(0, baseline.calls());
        assertTrue(records.get(0).modelDecided());
        assertSame(MODEL, records.get(0).decision());
    }

    @Test
    void aCanaryUsesTheModelForTheSameBorrowersEveryTime() {
        RolloutAssessor canary = assessor(RolloutMode.CANARY, 30);
        for (int i = 0; i < 200; i++) {
            String borrower = "B" + i;
            RiskAssessment expected = canary.inCanary(borrower) ? MODEL : BASE;
            assertSame(expected, canary.assessRisk(borrower, "CAM1"));
            assertSame(expected, canary.assessRisk(borrower, "CAM1"));
        }
    }

    @Test
    void aCanaryOfThirtyPercentCoversRoughlyThirtyPercent() {
        RolloutAssessor canary = assessor(RolloutMode.CANARY, 30);
        long inside = java.util.stream.IntStream.range(0, 1000).filter(i -> canary.inCanary("B" + i)).count();
        assertTrue(inside > 230 && inside < 370, "inside = " + inside);
    }

    @Test
    void zeroPercentIsNobodyAndOneHundredPercentIsEverybody() {
        RolloutAssessor none = assessor(RolloutMode.CANARY, 0);
        RolloutAssessor all = assessor(RolloutMode.CANARY, 100);
        assertTrue(java.util.stream.IntStream.range(0, 1000).noneMatch(i -> none.inCanary("B" + i)));
        assertTrue(java.util.stream.IntStream.range(0, 1000).allMatch(i -> all.inCanary("B" + i)));
    }

    @ParameterizedTest
    @ValueSource(ints = {-1, 101})
    void aPercentageOutsideZeroToOneHundredIsRejected(int percent) {
        assertThrows(IllegalArgumentException.class, () -> assessor(RolloutMode.CANARY, percent));
    }

    @Test
    void whenTheModelDecidesAndFailsTheFailureIsNotHidden() {
        FakeItemRiskAssessor broken = new FakeItemRiskAssessor().failing();
        RolloutAssessor on = new RolloutAssessor(baseline, broken, RolloutMode.ON, 0, "model-7", records::add);
        assertThrows(risk.domain.RiskAssessmentException.class, () -> on.assessRisk("B1", "CAM1"));
        assertTrue(records.isEmpty());
    }
}
```

## 4. A model solution

### 4.1 `src/main/java/risk/domain/RiskLevel.java`

```java
package risk.domain;

/**
 * How cautious to be about a request. UNKNOWN means that no trustworthy assessment exists; it is
 * not a level between the others and it is never a reason to approve.
 */
public enum RiskLevel {
    LOW,
    MODERATE,
    HIGH,
    UNKNOWN
}
```

### 4.2 `src/main/java/risk/domain/RiskAssessment.java`

```java
package risk.domain;

import java.time.Instant;
import java.util.Objects;

/** One answer to the question “how risky is it to lend this item to this borrower?”. */
public record RiskAssessment(RiskLevel level, double confidence, Instant assessedAt) {

    /** The least confidence at which a LOW assessment may approve a request without a person. */
    public static final double AUTOMATIC_APPROVAL_CONFIDENCE = 0.80;

    public RiskAssessment {
        Objects.requireNonNull(level, "level");
        Objects.requireNonNull(assessedAt, "assessedAt");
        if (Double.isNaN(confidence) || confidence < 0.0 || confidence > 1.0) {
            throw new IllegalArgumentException("Confidence must be between 0.0 and 1.0: " + confidence);
        }
    }

    /** Only a LOW level held with enough confidence may skip a person. */
    public boolean permitsAutomaticApproval() {
        return level == RiskLevel.LOW && confidence >= AUTOMATIC_APPROVAL_CONFIDENCE;
    }
}
```

### 4.3 `src/main/java/risk/domain/RiskAssessmentException.java`

```java
package risk.domain;

/** There is no trustworthy assessment: the service failed, did not answer in time or answered nonsense. */
public class RiskAssessmentException extends RuntimeException {
    public RiskAssessmentException(String message) {
        super(message);
    }

    public RiskAssessmentException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

### 4.4 `src/main/java/risk/domain/ItemRiskAssessor.java`

```java
package risk.domain;

/**
 * The domain's question about risk, in the domain's words. An implementation may be a model, a table
 * of rules or a test fake. The contract: the result is never null; if there is no trustworthy answer
 * the call throws {@link RiskAssessmentException}. It never returns a default that looks like an answer.
 */
public interface ItemRiskAssessor {
    RiskAssessment assessRisk(String borrowerId, String itemId);
}
```

### 4.5 `src/main/java/risk/domain/Route.java`

```java
package risk.domain;

/** What happens to a request after it has been screened. */
public enum Route {
    AUTO_APPROVE,
    SUPERVISOR_REVIEW,
    REJECT
}
```

### 4.6 `src/main/java/risk/domain/ReservationScreen.java`

```java
package risk.domain;

import java.util.Objects;

/**
 * Decides how a reservation request is routed, using only the domain contract. It knows nothing about
 * models, HTTP or floating-point scores. A failed assessment is not handled here: it propagates, so an
 * outage can never be turned into an approval by accident.
 */
public final class ReservationScreen {
    private final ItemRiskAssessor assessor;

    public ReservationScreen(ItemRiskAssessor assessor) {
        this.assessor = Objects.requireNonNull(assessor, "assessor");
    }

    public Route route(String borrowerId, String itemId) {
        requireText(borrowerId, "borrowerId");
        requireText(itemId, "itemId");
        RiskAssessment assessment = assessor.assessRisk(borrowerId, itemId);
        if (assessment.level() == RiskLevel.HIGH) {
            return Route.REJECT;
        }
        return assessment.permitsAutomaticApproval() ? Route.AUTO_APPROVE : Route.SUPERVISOR_REVIEW;
    }

    private static void requireText(String value, String name) {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException(name + " must not be blank.");
        }
    }
}
```

### 4.7 `src/main/java/risk/adapter/ViolationHistory.java`

```java
package risk.adapter;

/** How many times a borrower has returned equipment late. */
public interface ViolationHistory {
    int overdueViolations(String borrowerId);
}
```

### 4.8 `src/main/java/risk/adapter/RuleBasedRiskAssessor.java`

```java
package risk.adapter;

import java.time.Clock;
import java.util.Objects;
import risk.domain.ItemRiskAssessor;
import risk.domain.RiskAssessment;
import risk.domain.RiskAssessmentException;
import risk.domain.RiskLevel;

/**
 * A deterministic, deliberately cautious assessor. It is the fallback when the model cannot answer.
 * Its confidence is fixed below the automatic-approval threshold, so it can never approve a request
 * without a person, whatever the borrower's history.
 */
public final class RuleBasedRiskAssessor implements ItemRiskAssessor {
    static final double CONFIDENCE = 0.50;

    private final ViolationHistory history;
    private final Clock clock;

    public RuleBasedRiskAssessor(ViolationHistory history, Clock clock) {
        this.history = Objects.requireNonNull(history, "history");
        this.clock = Objects.requireNonNull(clock, "clock");
    }

    @Override
    public RiskAssessment assessRisk(String borrowerId, String itemId) {
        int violations = history.overdueViolations(borrowerId);
        if (violations < 0) {
            throw new RiskAssessmentException("The history reported a negative number of violations.");
        }
        RiskLevel level = violations == 0 ? RiskLevel.LOW : violations < 3 ? RiskLevel.MODERATE : RiskLevel.HIGH;
        return new RiskAssessment(level, CONFIDENCE, clock.instant());
    }
}
```

### 4.9 `src/main/java/risk/adapter/HttpRiskPredictionAdapter.java`

```java
package risk.adapter;

import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Clock;
import java.time.Duration;
import java.util.Objects;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import risk.domain.ItemRiskAssessor;
import risk.domain.RiskAssessment;
import risk.domain.RiskAssessmentException;
import risk.domain.RiskLevel;

/**
 * Asks a risk service over HTTP: {@code GET <base>/risk?borrower=..&item=..}. A 200 answer carries one
 * line, a level and a confidence separated by a space, such as {@code LOW 0.93}. Everything else is a
 * failure: a timeout, a refused connection, any other status, a body that is not exactly two fields, an
 * unknown level and a confidence outside 0.0 to 1.0. One attempt, a bounded wait that covers the whole
 * answer including the body, no retry and no fallback: whether to fall back is the caller's policy.
 */
public final class HttpRiskPredictionAdapter implements ItemRiskAssessor {
    private final HttpClient http;
    private final URI base;
    private final Duration requestTimeout;
    private final Clock clock;

    public HttpRiskPredictionAdapter(URI base, Duration connectTimeout, Duration requestTimeout, Clock clock) {
        this.base = Objects.requireNonNull(base, "base");
        this.requestTimeout = Objects.requireNonNull(requestTimeout, "requestTimeout");
        this.clock = Objects.requireNonNull(clock, "clock");
        this.http = HttpClient.newBuilder()
                .connectTimeout(Objects.requireNonNull(connectTimeout, "connectTimeout"))
                .build();
    }

    @Override
    public RiskAssessment assessRisk(String borrowerId, String itemId) {
        URI uri = URI.create(base.toString().replaceAll("/+$", "") + "/risk?borrower="
                + URLEncoder.encode(borrowerId, StandardCharsets.UTF_8) + "&item="
                + URLEncoder.encode(itemId, StandardCharsets.UTF_8));
        HttpRequest request = HttpRequest.newBuilder(uri).timeout(requestTimeout).GET().build();
        CompletableFuture<HttpResponse<String>> pending =
                http.sendAsync(request, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
        HttpResponse<String> response;
        try {
            response = pending.get(requestTimeout.toNanos(), TimeUnit.NANOSECONDS);
        } catch (TimeoutException late) {
            pending.cancel(true);
            throw new RiskAssessmentException(
                    "The risk service did not answer within " + requestTimeout.toMillis() + " ms.", late);
        } catch (InterruptedException interrupted) {
            pending.cancel(true);
            Thread.currentThread().interrupt();
            throw new RiskAssessmentException("The risk request was interrupted.", interrupted);
        } catch (ExecutionException failed) {
            Throwable cause = failed.getCause() == null ? failed : failed.getCause();
            throw new RiskAssessmentException("The risk service is unavailable: " + cause.getClass().getSimpleName(), cause);
        }
        if (response.statusCode() != 200) {
            throw new RiskAssessmentException("The risk service answered with status " + response.statusCode() + ".");
        }
        return parse(response.body());
    }

    private RiskAssessment parse(String body) {
        String[] fields = body.strip().split(" ", -1);
        if (fields.length != 2) {
            throw new RiskAssessmentException("The risk service answered with a malformed line.");
        }
        try {
            return new RiskAssessment(RiskLevel.valueOf(fields[0]), Double.parseDouble(fields[1]), clock.instant());
        } catch (IllegalArgumentException invalid) {
            throw new RiskAssessmentException("The risk service answered with an invalid value.", invalid);
        }
    }
}
```

### 4.10 `src/main/java/risk/adapter/ResilientRiskAssessor.java`

```java
package risk.adapter;

import java.time.Duration;
import java.util.Objects;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.logging.Logger;
import risk.domain.ItemRiskAssessor;
import risk.domain.RiskAssessment;
import risk.domain.RiskAssessmentException;

/**
 * Wraps a primary assessor with a bounded wait and an explicit, cautious fallback. The wait is enforced:
 * the primary runs on its own thread and the caller waits for it for at most the limit. On a timeout the
 * wrapper asks the thread to stop and answers from the fallback. Asking is all it can do, because a
 * primary that ignores interruption keeps running; the caller does not depend on it, because the caller
 * has already stopped waiting. Only the expected failure, a {@link RiskAssessmentException}, leads to the
 * fallback. A programming error in the primary propagates, so that it is found and not hidden.
 */
public final class ResilientRiskAssessor implements ItemRiskAssessor, AutoCloseable {
    private static final Logger LOG = Logger.getLogger(ResilientRiskAssessor.class.getName());

    private final ItemRiskAssessor primary;
    private final ItemRiskAssessor fallback;
    private final Duration limit;
    private final ExecutorService executor;
    private final AtomicInteger fallbacks = new AtomicInteger();

    public ResilientRiskAssessor(ItemRiskAssessor primary, ItemRiskAssessor fallback, Duration limit) {
        this.primary = Objects.requireNonNull(primary, "primary");
        this.fallback = Objects.requireNonNull(fallback, "fallback");
        this.limit = Objects.requireNonNull(limit, "limit");
        this.executor = Executors.newCachedThreadPool(task -> {
            Thread thread = new Thread(task, "risk-primary");
            thread.setDaemon(true);
            return thread;
        });
    }

    /** How many times the fallback has answered; a monitor can watch this. */
    public int fallbackCount() {
        return fallbacks.get();
    }

    @Override
    public RiskAssessment assessRisk(String borrowerId, String itemId) {
        Future<RiskAssessment> pending = executor.submit(() -> primary.assessRisk(borrowerId, itemId));
        try {
            return Objects.requireNonNull(pending.get(limit.toNanos(), TimeUnit.NANOSECONDS),
                    "the primary assessor returned null");
        } catch (TimeoutException late) {
            pending.cancel(true);
            return fallBackBecause("no answer within " + limit.toMillis() + " ms", borrowerId, itemId);
        } catch (InterruptedException interrupted) {
            pending.cancel(true);
            Thread.currentThread().interrupt();
            throw new RiskAssessmentException("Interrupted while waiting for the risk service.", interrupted);
        } catch (ExecutionException failed) {
            Throwable cause = failed.getCause();
            if (cause instanceof RiskAssessmentException) {
                return fallBackBecause(cause.getMessage(), borrowerId, itemId);
            }
            if (cause instanceof RuntimeException runtime) {
                throw runtime;
            }
            if (cause instanceof Error error) {
                throw error;
            }
            throw new IllegalStateException("The primary assessor failed unexpectedly.", cause);
        }
    }

    private RiskAssessment fallBackBecause(String reason, String borrowerId, String itemId) {
        fallbacks.incrementAndGet();
        LOG.warning(() -> "Risk service unavailable (" + reason + "); using the cautious fallback.");
        return fallback.assessRisk(borrowerId, itemId);
    }

    @Override
    public void close() {
        executor.shutdownNow();
    }
}
```

### 4.11 `src/main/java/risk/rollout/RolloutMode.java`

```java
package risk.rollout;

/** How far a new model has been rolled out. */
public enum RolloutMode {
    /** The baseline decides; the model is never called. */
    OFF,
    /** The baseline decides; the model is also called and its answer is only recorded. */
    SHADOW,
    /** The model decides for a stable share of borrowers; the baseline decides for the rest. */
    CANARY,
    /** The model decides for everyone. */
    ON
}
```

### 4.12 `src/main/java/risk/rollout/ProvenanceRecord.java`

```java
package risk.rollout;

import java.util.Objects;
import risk.domain.RiskAssessment;

/**
 * What a decision rested on: the model version that was in use, the model's answer (null if it did not
 * answer), the assessment that was actually used, and whether the model decided.
 */
public record ProvenanceRecord(String borrowerId, String itemId, String modelVersion,
                               RiskAssessment modelAnswer, RiskAssessment decision, boolean modelDecided) {
    public ProvenanceRecord {
        Objects.requireNonNull(borrowerId, "borrowerId");
        Objects.requireNonNull(itemId, "itemId");
        Objects.requireNonNull(modelVersion, "modelVersion");
        Objects.requireNonNull(decision, "decision");
    }
}
```

### 4.13 `src/main/java/risk/rollout/ProvenanceLog.java`

```java
package risk.rollout;

/** Where provenance records go. An append-only store in production; a list in tests. */
public interface ProvenanceLog {
    void record(ProvenanceRecord record);
}
```

### 4.14 `src/main/java/risk/rollout/RolloutAssessor.java`

```java
package risk.rollout;

import java.util.Objects;
import risk.domain.ItemRiskAssessor;
import risk.domain.RiskAssessment;
import risk.domain.RiskAssessmentException;

/**
 * Decides, borrower by borrower, whether the model or the baseline answers, and records what each decision
 * rested on. The share of the canary is stable: a borrower is always in or always out for a given percentage.
 */
public final class RolloutAssessor implements ItemRiskAssessor {
    private final ItemRiskAssessor baseline;
    private final ItemRiskAssessor model;
    private final RolloutMode mode;
    private final int canaryPercent;
    private final String modelVersion;
    private final ProvenanceLog log;

    public RolloutAssessor(ItemRiskAssessor baseline, ItemRiskAssessor model, RolloutMode mode,
                           int canaryPercent, String modelVersion, ProvenanceLog log) {
        this.baseline = Objects.requireNonNull(baseline, "baseline");
        this.model = Objects.requireNonNull(model, "model");
        this.mode = Objects.requireNonNull(mode, "mode");
        this.modelVersion = Objects.requireNonNull(modelVersion, "modelVersion");
        this.log = Objects.requireNonNull(log, "log");
        if (canaryPercent < 0 || canaryPercent > 100) {
            throw new IllegalArgumentException("canaryPercent must be between 0 and 100: " + canaryPercent);
        }
        this.canaryPercent = canaryPercent;
    }

    /** A stable choice: the same borrower and percentage always give the same answer. */
    public boolean inCanary(String borrowerId) {
        return Math.floorMod(borrowerId.hashCode(), 100) < canaryPercent;
    }

    @Override
    public RiskAssessment assessRisk(String borrowerId, String itemId) {
        return switch (mode) {
            case OFF -> baseline.assessRisk(borrowerId, itemId);
            case SHADOW -> shadow(borrowerId, itemId);
            case CANARY -> inCanary(borrowerId) ? modelDecides(borrowerId, itemId) : baseline.assessRisk(borrowerId, itemId);
            case ON -> modelDecides(borrowerId, itemId);
        };
    }

    private RiskAssessment shadow(String borrowerId, String itemId) {
        RiskAssessment decision = baseline.assessRisk(borrowerId, itemId);
        RiskAssessment modelAnswer;
        try {
            modelAnswer = model.assessRisk(borrowerId, itemId);
        } catch (RiskAssessmentException unavailable) {
            modelAnswer = null;   // a shadow failure must never affect the decision
        }
        log.record(new ProvenanceRecord(borrowerId, itemId, modelVersion, modelAnswer, decision, false));
        return decision;
    }

    private RiskAssessment modelDecides(String borrowerId, String itemId) {
        RiskAssessment answer = model.assessRisk(borrowerId, itemId);
        log.record(new ProvenanceRecord(borrowerId, itemId, modelVersion, answer, answer, true));
        return answer;
    }
}
```

### 4.15 `pom.xml`

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>edu.se506</groupId>
  <artifactId>risk-lab</artifactId>
  <version>1.0.0</version>
  <properties>
    <maven.compiler.release>17</maven.compiler.release>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>
  <dependencies>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>5.13.4</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.14.1</version>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <version>3.5.4</version>
        <configuration><failIfNoTests>true</failIfNoTests></configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

### 4.16 `scripts/check.sh`

```bash
#!/usr/bin/env bash
# Builds the lab and runs every test, then the same tests without the integration group, so the two
# counts can be reported separately. CHAPTER_MVN names the Maven command (default: mvn). CHAPTER_M2
# optionally names a local Maven repository and CHAPTER_OFFLINE=1 stops Maven from contacting a remote one.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

MVN="${CHAPTER_MVN:-mvn}"
ARGS=(--batch-mode)
if [ -n "${CHAPTER_M2:-}" ]; then
  ARGS+=("-Dmaven.repo.local=${CHAPTER_M2}")
fi
if [ "${CHAPTER_OFFLINE:-0}" = "1" ]; then
  ARGS+=(--offline)
fi

echo "=== all tests"
"$MVN" "${ARGS[@]}" verify
echo "=== without the integration group"
"$MVN" "${ARGS[@]}" test -DexcludedGroups=integration
echo "RISK LAB PASSED"
```

### 4.17 `.gitignore`

```gitignore
/target/
/build/
*.class
```

### 4.18 `.gitattributes`

```gitattributes
*.sh text eol=lf
```

## 5. Worked explanation

**The contract.** `ItemRiskAssessor` and `RiskAssessment` are the only things the domain knows about risk. The constructor of `RiskAssessment` validates the confidence, so an out-of-range value cannot exist. `permitsAutomaticApproval()` is the one place that holds the threshold. `ReservationScreen` routes by the domain's rules and does not catch `RiskAssessmentException`, so an outage cannot become an approval.

**The adapter.** `HttpRiskPredictionAdapter` follows the pattern of Chapter 13's `HttpLegacyDirectoryClient`: it sends the request asynchronously, waits for at most the request timeout for the whole answer, and cancels on a timeout. Every outcome other than a good answer is a `RiskAssessmentException`. The adapter makes no decision about a fallback.

**The wrapper.** `ResilientRiskAssessor` is the one place that decides to fall back. It runs the primary on a daemon thread, so that an abandoned call cannot keep the JVM alive, and it uses the same wait-then-cancel pattern. It falls back only for a `RiskAssessmentException` or a timeout, never for a programming error. It counts its fallbacks. It is `AutoCloseable` because it owns a thread pool.

**The cautious fallback.** `RuleBasedRiskAssessor` fixes its confidence at 0.50, below the 0.80 threshold, so a fallback answer can never approve a request without a person. That is a property of the *fallback*, and it is tested (`theCautiousFallbackNeverApprovesWithoutAPerson`).

**The rollout.** `RolloutAssessor` implements the four modes. In `SHADOW` a failure of the model is swallowed and recorded as “no answer”, because a shadow must never affect the decision; in `ON` and `CANARY` it propagates, because there the model's answer is the decision. The canary's share uses `Math.floorMod(hashCode, 100)`, so that a negative hash code still gives a bucket from 0 to 99.

**The stub.** `StubRiskService` is the JDK's own HTTP server on the loopback address and a free port. Its scenarios are chosen by the borrower identifier. `SLOW` sends nothing until the stub is closed; `SLOWBODY` sends its headers and one byte and then stalls.

## 6. Expected output

```text
=== all tests
[INFO] Tests run: 67, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
=== without the integration group
[INFO] Tests run: 56, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
RISK LAB PASSED
```

The 67 invocations by class: `RiskAssessmentTest` 12, `ReservationScreenTest` 10, `RuleBasedRiskAssessorTest` 16, `ResilientRiskAssessorTest` 8, `RolloutAssessorTest` 10 and `HttpRiskPredictionAdapterContractTest` 11 (tagged `integration`). Parameterised tests count once for each value. Maven and the JDK may print warnings; the last lines decide.

## 7. A small fault experiment

In a separate copy of the lab, make one change at a time and run `mvn --batch-mode test`. Each experiment checks whether a particular test notices a particular fault.

| Fault | Change | What happens |
|---|---|---|
| E1 | the wrapper waits an hour instead of the limit | 2 invocation(s) end at the five-second deadline: `aStalledPrimaryIsAskedToStop`, `aStalledPrimaryIsGivenUpOnWithinTheLimitAndTheFallbackAnswers` |
| E2 | the wrapper does not ask a stalled call to stop | 1 invocation(s) fail: `aStalledPrimaryIsAskedToStop` |
| E3 | every runtime failure of the primary falls back | 1 invocation(s) fail: `aProgrammingErrorInThePrimaryIsNotHiddenByTheFallback` |
| E4 | the wrapper does not restore the caller's interrupt flag | 1 invocation(s) fail: `anInterruptedCallerKeepsItsInterruptFlagAndGetsAFailure` |
| E5 | automatic approval needs more than the threshold (`>` for `>=`) | 2 invocation(s) fail: `eachAssessmentIsRoutedByTheDomainsRules`, `automaticApprovalNeedsLowAndAtLeastTheThreshold` |
| E6 | a confidence of exactly 1.0 is rejected | 5 invocation(s) error: `eachAssessmentIsRoutedByTheDomainsRules`, `aLevelOtherThanLowNeverApprovesAutomatically`, `confidenceAtTheEdgesIsAccepted` |
| E7 | three violations stay MODERATE (`<=` for `<`) | 1 invocation(s) fail: `theLevelFollowsTheNumberOfViolations` |
| E8 | HIGH is no longer rejected | 4 invocation(s) fail: `eachAssessmentIsRoutedByTheDomainsRules`, `eachBorrowerIsAssessedOnTheirOwn` |
| E9 | an outage becomes an approval | 1 invocation(s) fail: `aFailedAssessmentIsNeverTurnedIntoAnApproval` |
| E10 | identifiers are not encoded in the request | 1 invocation(s) error: `identifiersAreEncodedInTheRequest` |
| E11 | the adapter waits an hour instead of the limit | 1 invocation(s) end at the five-second deadline: `aServiceThatStallsInTheMiddleOfTheBodyIsAlsoBounded` |
| E12 | in shadow mode the model's answer decides | 1 invocation(s) fail: `inShadowTheBaselineDecidesAndTheModelsAnswerIsOnlyRecorded` |
| E13 | a shadow failure escapes | 1 invocation(s) error: `aShadowFailureNeverChangesTheDecisionAndIsRecordedAsNoAnswer` |
| E14 | the canary includes one bucket too many (`<=` for `<`) | 1 invocation(s) fail: `zeroPercentIsNobodyAndOneHundredPercentIsEverybody` |
| E15 | a different but valid assignment of borrowers to the canary (`Math.abs(hash % 100)`) | No test fails. |

Fourteen of the fifteen faults are noticed. The survivor, E15, is a different but valid way to assign borrowers to the canary: the contract promises a **stable** share, not a particular one, so no test should fail, and none does. It is an equivalent change in the sense of Chapter 15. The experiment checks that these tests catch these faults; it does not show that the lab is correct for every input.

E1 and E11 deserve a second look. They replace the limit with one hour, so a missing bound is not a failed assertion; it is a hang. The tests carry an outer deadline of five seconds (`@Timeout(5)`), which turns the hang into a failure. The same deadline is why E11 catches what the client's own request timeout does not: only the stalled body is left unbounded, as Chapter 13 showed.

## 8. Answers to the exercise

**Part A.** The probe shows three failures: no limit on the wait, an outage that looks like a refusal and a nonsense score that is accepted. Reading the class finds more:

| Failure | Where | Why it matters |
|---|---|---|
| No timeout | `openConnection()` and `getInputStream()` | A stalled service holds the caller for as long as it likes (the probe: 1,502 ms) |
| An outage looks like a refusal | `catch (Exception anything) { return false; }` | The caller cannot tell “high risk” from “service down” |
| A nonsense score is accepted | `Float.parseFloat(parts[1])`, no range check | A confidence of 1.7 was approved |
| A magic number | `score > 0.8f` | No name and no owner; also `>` where the domain's rule is `>=` |
| A level compared as text | `parts[0].equals("LOW")` | A new level or a misspelling is silently “no” |
| Identifiers are not encoded | the string concatenation | A space or `&` in an identifier breaks or changes the request |
| Every exception is swallowed | the catch-all | A programming error (`NullPointerException` on a missing line) looks like a refusal |
| The reader and the connection are never closed | `in`, `connection` | A resource leak |
| No test is possible without the service | the constructor takes a URL | There is no seam |
| No record of what was decided | the whole method | Nothing says which answer a decision rested on |

**Part F.** Removing the limit (E1) makes `aStalledPrimaryIsGivenUpOnWithinTheLimitAndTheFallbackAnswers` and `aStalledPrimaryIsAskedToStop` fail at their deadline. It tells you that the bound is tested, and not only written.

**The closing note.** A good note lists at least eight failures from part A (the table has ten), gives the count that passes, names one fault and the test that caught it, and names a limit: for example that no test says the model is accurate, that the stub is not the real service, or that nothing was run on a Java 17 runtime.

## 9. Teaching and revision notes

The probe takes a minute and makes the case better than any argument. Ask learners to predict its four lines before they run it. The decision between failing and falling back (Appendix F, Section F.5) is worth a class discussion: ask learners when a fallback is safe, and have them name one case in the lending project where it would not be (the borrower's category).

Keep the lab separate from the lending project. Do not add its tests to the lending project's totals, and do not cite its counts as a measure of the quality of any model. The stub's response format (`LOW 0.93`) is the lab's own and is not a standard.

## References

Appendix F lists the sources for this file. The wait-then-cancel pattern is that of Chapter 13, Section 13.2.
