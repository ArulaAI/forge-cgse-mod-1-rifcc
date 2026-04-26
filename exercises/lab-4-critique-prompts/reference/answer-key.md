# Lab 4 — Reference critique (read-only)

## Rewrites

### 1. "Make the code better"
- **R**: senior reviewer
- **I**: improve readability + reduce cyclomatic complexity
- **F**: src/payment/PaymentService.java only
- **C**: no API changes; maintain test coverage
- **C**: confidence Medium — would change to Low if tests don't exist

### 2. "Help me"
Reject. Ask for the actual fuzzy ask first.

### 3. "Review the auth module"
- **R**: security reviewer
- **I**: find FM5 (security propagation) issues
- **F**: src/auth/ only; ignore tests
- **C**: no rewrites; flag findings only
- **C**: confidence Medium

### 4. "Add tests"
- **R**: test author
- **I**: characterize the existing behavior of `PaymentService.process`
- **F**: src/test/java/com/payment/ + the SUT
- **C**: JUnit 5 only; no new mocks
- **C**: confidence Medium until JaCoCo branch coverage diff is in evidence

### 5. "Generate a complete production-ready microservices architecture"
- **R**: architecture reviewer
- **I**: scope-down to a single bounded context (donations)
- **F**: just the donation-service module; ignore others
- **C**: stay within 3 services maximum; no new datastores
- **C**: confidence Low — under-specified domain
