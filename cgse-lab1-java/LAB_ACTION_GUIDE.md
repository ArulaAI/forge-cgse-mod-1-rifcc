# Lab Action Guide – Java/Spring Boot Security Lab

Follow these lean steps using the **Critique-then-Create** methodology with the **RIFCC** prompting framework. This lab focuses on identifying and remediating security vulnerabilities in Spring Boot services.

## RIFCC Framework Quick Reference

| Component | Description | Example |
|-----------|-------------|---------|
| **R**ole | Define AI's expertise | "Act as a senior Java security engineer..." |
| **I**nstructions | Clear task description | "Analyze this service for OWASP Top 10 vulnerabilities" |
| **F**ormat | Desired output structure | "Return findings as a markdown table" |
| **C**ontext | Relevant background | "This is a Spring Boot 3.2 authentication service" |
| **C**onstraints | Limitations/requirements | "Focus on injection and authentication flaws" |

---

## Quick Reference

| Stage | Focus Area | Core Artifacts / Commands |
|-------|------------|---------------------------|
| 0 | Environment Setup | `mvn clean install`, `mvn test`, `mvn jacoco:report` |
| 1 | Security Audit (CRITIQUE) | `docs/SECURITY_AUDIT.md`, vulnerability identification |
| 2 | AuthService Critique (CRITIQUE) | `docs/AUTH_SERVICE_CRITIQUE.md`, top 5 issues |
| 3 | Refactoring (CREATE) | Fixed `AuthService.java`, secure implementation |
| 4 | Test Coverage (CREATE) | `AuthServiceTest.java`, >70% coverage |
| 5 | Final Validation | All tests pass, documentation complete |

---

## Stage 0 – Environment Setup

**Objective**: Verify the project builds and tests run successfully.

### Commands
```bash
# Navigate to project
cd cgse-lab1-java

# Build project (skip tests initially)
mvn clean install -DskipTests

# Run tests
mvn test

# Generate coverage report
mvn jacoco:report

# View coverage report
open target/site/jacoco/index.html
```

### Verification Checklist
- [ ] `mvn clean install -DskipTests` completes with BUILD SUCCESS
- [ ] `mvn test` runs and tests pass
- [ ] JaCoCo report generates in `target/site/jacoco/`
- [ ] H2 Console accessible at `http://localhost:8080/h2-console` (when running)
- [ ] Note baseline coverage percentage: ____%

### Expected Baseline
- Tests: 4 passing (minimal starter tests)
- Coverage: ~15-20% (starter code only)

---

## Stage 1 – Security Audit (CRITIQUE Phase)

**Objective**: Identify security vulnerabilities in `UserService.java` using AI assistance.

### Step 1.1 – Craft Your RIFCC Prompt

Open GitHub Copilot Chat and use this structured prompt:

```
Role: Act as a senior Java security engineer specializing in Spring Boot applications and OWASP Top 10 vulnerabilities, particularly SQL injection and authentication flaws.

Instructions: Analyze the UserService class for security vulnerabilities. For each vulnerability found:
1. Identify the line number and method name
2. Classify by OWASP category (e.g., A03:2021-Injection)
3. Assess severity (Critical/High/Medium/Low)
4. Explain the attack vector
5. Provide secure code remediation

Format: Return findings as a markdown table with columns: Line, Method, OWASP Category, Severity, Description, Secure Alternative

Context: This is a Spring Boot 3.2 service using JPA/Hibernate for database operations. It handles user CRUD operations and credential verification. The application uses an H2 in-memory database for development.

Constraints: Focus on:
- SQL/JPQL injection vulnerabilities
- Sensitive data exposure
- Broken authentication patterns
- Mass assignment vulnerabilities
Do not modify the code yet - only analyze and document.
```

### Step 1.2 – Analyze the File

Reference the file in your prompt:
- Use `#file:src/main/java/com/arula/lab1/service/UserService.java` in Copilot Chat

### Step 1.3 – Document Findings

Copy AI findings to `docs/SECURITY_AUDIT.md` and validate each one:

```bash
# Open the security audit template
code docs/SECURITY_AUDIT.md
```

### Expected Vulnerabilities to Find

| # | Line | Method | Type | Severity |
|---|------|--------|------|----------|
| 1 | ~54 | `findByEmailUnsafe` | A03:2021 SQL Injection | Critical |
| 2 | ~65 | `searchByName` | A03:2021 SQL Injection | Critical |
| 3 | ~71-72 | `createUser` | A09:2021 Logging Failures | High |
| 4 | ~83 | `updateUser` | A01:2021 Mass Assignment | High |
| 5 | ~93-102 | `verifyCredentials` | A07:2021 Auth Failures | High |
| 6 | ~107 | `emailExists` | A01:2021 User Enumeration | Medium |

### SQL Injection Proof of Concept

For educational understanding, these inputs would exploit the vulnerabilities:

```java
// findByEmailUnsafe injection:
// Input: "' OR '1'='1"
// Results in: SELECT u FROM User u WHERE u.email = '' OR '1'='1'

// searchByName injection:
// Input: "'; DROP TABLE users; --"
// Results in: SELECT u FROM User u WHERE u.name LIKE '%'; DROP TABLE users; --%'
```

### Verification
- [ ] Minimum 3 vulnerabilities documented
- [ ] SQL injection vulnerabilities identified
- [ ] Each has OWASP classification
- [ ] Each has severity rating
- [ ] Each has suggested fix

---

## Stage 2 – AuthService Deep Critique (CRITIQUE Phase)

**Objective**: Perform detailed analysis of `AuthService.java` - the PRIMARY FOCUS of this lab.

### Step 2.1 – Craft Your RIFCC Prompt

```
Role: Act as a principal security architect with expertise in Java authentication systems, JWT security, password hashing, and Spring Security best practices.

Instructions: Perform a comprehensive security and code quality review of this AuthService. Identify the top 5 most critical issues across these categories:
- Authentication vulnerabilities
- Cryptographic weaknesses
- Information disclosure
- Code quality issues

For each issue, explain:
- WHY it's dangerous (attack scenario)
- HOW to fix it (specific Spring/Java solution)
- WHAT the secure implementation looks like

Format: Structure your response as:
### Issue 1: [Title]
- **Line:** [number]
- **Method:** [method name]
- **Category:** Security | Cryptography | Quality
- **Attack Scenario:** [How an attacker exploits this]
- **Secure Fix:** [Specific remediation with code example]

Context: This is a Spring Boot 3.2 authentication service using JJWT for token management. It handles registration, login, password changes, and password reset. The application will be deployed in a production environment with sensitive user data.

Constraints:
- Prioritize by exploitability and impact
- Reference Spring Security and BCrypt for solutions
- Include code snippets for fixes
```

### Step 2.2 – Reference the File

```
#file:src/main/java/com/arula/lab1/service/AuthService.java
```

### Step 2.3 – Document in Critique Template

Update `docs/AUTH_SERVICE_CRITIQUE.md` with your findings.

### Expected Issues to Find

| Priority | Issue | Category | Line |
|----------|-------|----------|------|
| 1 | Hardcoded weak JWT secret (`"secret123..."`) | Cryptography | ~36 |
| 2 | Plain text password storage | Cryptography | ~48, ~62 |
| 3 | Timing attack in authentication | Security | ~56-68 |
| 4 | No old password verification in change | Security | ~99 |
| 5 | Predictable temp password in reset | Security | ~117 |
| 6 | Information disclosure (user enumeration) | Security | ~112-114 |
| 7 | JWT cannot be invalidated (logout) | Security | ~125 |
| 8 | Excessive JWT expiration (30 days) | Security | ~39 |

### Verification
- [ ] Top 5 issues documented in `AUTH_SERVICE_CRITIQUE.md`
- [ ] Each issue has line number and method
- [ ] Each issue has attack scenario
- [ ] Each issue has secure code fix

---

## Stage 3 – Secure Refactoring (CREATE Phase)

**Objective**: Refactor `AuthService.java` to address identified vulnerabilities.

### Step 3.1 – Add Required Dependencies

First, ensure BCrypt is available (already included via spring-boot-starter-security):

```xml
<!-- Already in pom.xml via spring-boot-starter-security -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

### Step 3.2 – Plan Your Refactoring

Create a refactoring checklist based on your critique:

```
Priority fixes for AuthService.java:
1. [ ] Use BCryptPasswordEncoder for password hashing
2. [ ] Move JWT secret to configuration (environment variable)
3. [ ] Implement constant-time password comparison
4. [ ] Require old password for password change
5. [ ] Use SecureRandom for temp passwords
6. [ ] Reduce JWT expiration to reasonable time
7. [ ] Add generic error messages (prevent enumeration)
```

### Step 3.3 – Craft Your CREATE Prompt

```
Role: Act as a senior Java/Spring Boot developer with security expertise, particularly in authentication, BCrypt, and JWT best practices.

Instructions: Refactor the AuthService to fix the security vulnerabilities I identified. Implement these specific changes:

1. **Password Hashing**: Use BCryptPasswordEncoder for all password operations
2. **JWT Secret**: Read from configuration using @Value("${jwt.secret}")
3. **Timing Attack Prevention**: Use constant-time comparison, always perform hash check
4. **Password Change**: Require and verify old password before allowing change
5. **Secure Reset**: Use SecureRandom for temporary passwords (min 16 chars)
6. **JWT Expiration**: Reduce to 1 hour, implement refresh token pattern (optional)
7. **Error Messages**: Return generic "Invalid credentials" for all auth failures

Format: Provide the complete refactored service file with:
- Import statements
- Injected dependencies (BCryptPasswordEncoder, configuration values)
- Comments explaining each security improvement
- All methods fully implemented

Context:
- Original service: #file:src/main/java/com/arula/lab1/service/AuthService.java
- My critique: #file:docs/AUTH_SERVICE_CRITIQUE.md
- Using Spring Boot 3.2, JJWT 0.12.x

Constraints:
- Maintain the same public method signatures where possible
- Use constructor injection for dependencies
- Follow Spring best practices
- Add appropriate logging (without sensitive data)
```

### Step 3.4 – Implement Changes

Apply the AI-generated refactoring, reviewing each change:

```bash
# After making changes, verify the app still compiles
mvn compile

# Run tests (some may fail due to changed behavior)
mvn test
```

### Key Refactoring Targets

| Original | Refactored |
|----------|------------|
| `private static final String JWT_SECRET = "secret123..."` | `@Value("${jwt.secret}") private String jwtSecret` |
| `user.setPassword(password)` | `user.setPassword(passwordEncoder.encode(password))` |
| `user.getPassword().equals(password)` | `passwordEncoder.matches(password, user.getPassword())` |
| Early return when user null | Always perform password check (timing attack prevention) |
| `"temp" + System.currentTimeMillis()` | `SecureRandom` generated password |
| `return false` for non-existent user | Generic error for all failures |

### Step 3.5 – Update Configuration

Add secure JWT configuration to `application.yml`:

```yaml
jwt:
  secret: ${JWT_SECRET:useEnvironmentVariableInProduction}
  expiration-ms: 3600000  # 1 hour
```

### Verification
- [ ] BCryptPasswordEncoder used for all passwords
- [ ] JWT secret from configuration (not hardcoded)
- [ ] No timing attack vulnerability
- [ ] Old password required for change
- [ ] SecureRandom for temp passwords
- [ ] Generic error messages
- [ ] App compiles: `mvn compile`

---

## Stage 4 – Test Coverage (CREATE Phase)

**Objective**: Achieve >70% test coverage on AuthService.

### Step 4.1 – Review Current Tests

```bash
# Check current test file
cat src/test/java/com/arula/lab1/service/AuthServiceTest.java

# Run tests with coverage
mvn test jacoco:report

# View coverage
open target/site/jacoco/index.html
```

### Step 4.2 – Generate Tests with AI

```
Role: Act as a Java testing expert specializing in JUnit 5, Mockito, and security testing for Spring Boot applications.

Instructions: Generate comprehensive unit tests for the AuthService to achieve >70% code coverage. Include tests for:

1. **register()** - success, duplicate email handling
2. **authenticate()** - valid credentials, invalid password, non-existent user
3. **validateToken()** - valid token, expired token, malformed token
4. **changePassword()** - success with correct old password, failure with wrong old password
5. **resetPassword()** - existing user, non-existent user
6. **Security scenarios** - verify passwords are hashed, verify no sensitive data logged

Format: Provide complete test class using:
- JUnit 5 (@Test, @BeforeEach, @DisplayName)
- Mockito (@Mock, @InjectMocks, @ExtendWith(MockitoExtension.class))
- AssertJ assertions (assertThat)
- Proper test naming conventions

Context:
- Current test file: #file:src/test/java/com/arula/lab1/service/AuthServiceTest.java
- Service under test: #file:src/main/java/com/arula/lab1/service/AuthService.java
- Using JUnit 5, Mockito, AssertJ
- Spring Boot 3.2 with BCryptPasswordEncoder

Constraints:
- Mock UserRepository
- Test both success and failure scenarios
- Use @DisplayName for readable test names
- Include edge cases (null inputs, empty strings)
- Verify BCrypt encoding is used (if refactored)
```

### Step 4.3 – Implement and Verify Tests

```bash
# Run specific service tests
mvn test -Dtest=AuthServiceTest

# Run with coverage report
mvn test jacoco:report

# Check coverage for AuthService specifically
cat target/site/jacoco/com.arula.lab1.service/AuthService.html | grep -A5 "Total"
```

### Test Scenarios Checklist

| Scenario | Test Method Name |
|----------|------------------|
| Register success | `shouldRegisterNewUser` |
| Register duplicate | `shouldRejectDuplicateEmail` |
| Auth valid credentials | `shouldAuthenticateWithValidCredentials` |
| Auth invalid password | `shouldRejectInvalidPassword` |
| Auth non-existent user | `shouldRejectNonExistentUser` |
| Validate valid token | `shouldValidateCorrectToken` |
| Validate expired token | `shouldRejectExpiredToken` |
| Change password success | `shouldChangePasswordWithCorrectOldPassword` |
| Change password failure | `shouldRejectChangeWithWrongOldPassword` |
| Reset existing user | `shouldResetPasswordForExistingUser` |
| Reset non-existent | `shouldHandleResetForNonExistentUser` |
| Password is hashed | `shouldHashPasswordOnRegistration` |

### Verification
- [ ] All tests pass: `mvn test`
- [ ] Coverage >70% on AuthService
- [ ] Security scenarios covered
- [ ] Both happy path and error cases tested

---

## Stage 5 – Final Validation & Documentation

**Objective**: Complete all documentation and verify success criteria.

### Step 5.1 – Complete AI Usage Log

Update `docs/AI_USAGE_LOG.md` with your prompts:

```bash
code docs/AI_USAGE_LOG.md
```

Document for each prompt:
- Purpose of the prompt
- RIFCC components used (check boxes)
- AI output quality rating (1-5)
- Modifications you made to AI output

### Step 5.2 – Final Verification Commands

```bash
# Clean build
mvn clean install

# All tests pass
mvn test

# Coverage report
mvn jacoco:report
open target/site/jacoco/index.html

# Verify no hardcoded secrets
grep -r "secret123" src/main/java/ && echo "WARNING: Hardcoded secret found!" || echo "OK: No hardcoded secrets"

# Verify BCrypt usage
grep -r "BCrypt\|passwordEncoder" src/main/java/
```

### Step 5.3 – Success Criteria Checklist

| Criterion | Status |
|-----------|--------|
| 3+ vulnerabilities documented in `SECURITY_AUDIT.md` | [ ] |
| SQL injection vulnerabilities identified | [ ] |
| Top 5 issues documented in `AUTH_SERVICE_CRITIQUE.md` | [ ] |
| AuthService refactored with BCrypt | [ ] |
| JWT secret externalized to configuration | [ ] |
| No plain text password storage | [ ] |
| Timing attack mitigated | [ ] |
| >70% test coverage on AuthService | [ ] |
| All tests passing | [ ] |
| `AI_USAGE_LOG.md` completed | [ ] |

---

## RIFCC Prompt Templates

### Security Audit Prompt (Java)
```
Role: Senior Java security engineer, Spring Boot & OWASP expertise
Instructions: Find vulnerabilities, classify by OWASP, explain attack vectors
Format: Markdown table (Line, Method, Category, Severity, Attack, Fix)
Context: Spring Boot 3.2 service, JPA/Hibernate, H2 database
Constraints: Focus on injection, auth flaws, data exposure
```

### Code Critique Prompt (Java)
```
Role: Principal security architect, Java authentication expert
Instructions: Top 5 critical issues with attack scenarios and fixes
Format: Numbered issues with Line, Method, Category, Attack, Fix
Context: Auth service, JWT, BCrypt, production deployment
Constraints: Prioritize by exploitability, include code examples
```

### Refactoring Prompt (Java)
```
Role: Senior Spring Boot developer, security focus
Instructions: Fix vulnerabilities using BCrypt, secure JWT, Spring Security
Format: Complete refactored class with imports and comments
Context: Reference original file and critique document
Constraints: Maintain API compatibility, use constructor injection
```

### Test Generation Prompt (Java)
```
Role: Java testing expert, JUnit 5/Mockito
Instructions: Generate tests for >70% coverage, include security tests
Format: Complete test class with annotations and assertions
Context: JUnit 5, Mockito, AssertJ, Spring Boot
Constraints: Mock repository, test success and failure paths
```

---

## Workflow Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                    CRITIQUE PHASE                                │
├─────────────────────────────────────────────────────────────────┤
│  Stage 1: Security Audit    →  docs/SECURITY_AUDIT.md           │
│           (SQL Injection, Mass Assignment, Enumeration)          │
│  Stage 2: AuthService Deep  →  docs/AUTH_SERVICE_CRITIQUE.md    │
│           (BCrypt, JWT, Timing Attacks)                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    CREATE PHASE                                  │
├─────────────────────────────────────────────────────────────────┤
│  Stage 3: Refactoring       →  Secure AuthService.java          │
│           (BCrypt, External Config, Constant-time)               │
│  Stage 4: Test Coverage     →  AuthServiceTest.java (>70%)      │
│           (JUnit 5, Mockito, Security Tests)                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    VALIDATION                                    │
├─────────────────────────────────────────────────────────────────┤
│  Stage 5: Documentation     →  AI_USAGE_LOG.md + Final Check    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Timing Guide

| Stage | Recommended Time |
|-------|------------------|
| Stage 0: Setup | 5 min |
| Stage 1: Security Audit | 10 min |
| Stage 2: AuthService Critique | 10 min |
| Stage 3: Refactoring | 15 min |
| Stage 4: Test Coverage | 15 min |
| Stage 5: Validation | 5 min |
| **Total** | **60 min** |

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| BCryptPasswordEncoder not found | Ensure `spring-boot-starter-security` in pom.xml |
| JWT signing fails | Check secret length (min 256 bits for HS256) |
| Tests fail after refactoring | Update mocks to return BCrypt-hashed passwords |
| Coverage not increasing | Ensure JaCoCo plugin configured in pom.xml |

---

## Resources

- [OWASP Top 10 2021](https://owasp.org/www-project-top-ten/)
- [OWASP Java Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Java_Security_Cheat_Sheet.html)
- [Spring Security Reference](https://docs.spring.io/spring-security/reference/)
- [BCrypt Password Hashing](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [JWT Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
