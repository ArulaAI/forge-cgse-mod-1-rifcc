---
agent: 'agent'
description: 'Grade a CGSE Module 1 lab submission against the 100-point rubric with detailed feedback and letter grade.'
tools: ['search/codebase', 'edit/editFiles', 'read/problems', 'search']
---

# Grade Lab Submission

Grade the current lab submission for **${input:ProjectType:Angular,Java}** against the CGSE Module 1 success criteria.

## Grading Instructions

Evaluate this submission using the 100-point rubric:

### 1. Documentation Review (25 points)

Examine the `docs/` folder and score each file:

**SECURITY_AUDIT.md (10 points)**
- Contains 3+ vulnerabilities?
- Each has OWASP category (e.g., A03:2021)?
- Each has severity rating?
- Each has specific line numbers?
- Each has remediation suggestions?

**AUTH_SERVICE_CRITIQUE.md (10 points)**
- Contains 5 documented issues?
- Each has line number reference?
- Each has category (Security/Quality/Performance)?
- Each has recommended fix?

**AI_USAGE_LOG.md (5 points)**
- At least 3 prompts documented?
- RIFCC components noted for each?
- Quality ratings provided?

### 2. Security Remediation Review (40 points)

Examine the AuthService file:
- **Angular:** `src/app/services/auth.service.ts`
- **Java:** `src/main/java/com/arula/lab1/service/AuthService.java`

**Check for these fixes:**

| Fix | Angular | Java | Points |
|-----|---------|------|--------|
| Token/Password Storage | No localStorage for tokens | BCrypt for passwords | 10 |
| No Sensitive Logging | No console.log(token/password) | No System.out.println(sensitive) | 10 |
| Auth Logic | Token expiry in isAuthenticated() | Constant-time comparison | 10 |
| Input Validation | Email/password validation | Bean validation or manual | 5 |
| Type Safety | No `any` types | Proper exception handling | 5 |

### 3. Test Coverage Review (25 points)

Examine the test file:
- **Angular:** `src/app/services/auth.service.spec.ts`
- **Java:** `src/test/java/com/arula/lab1/service/AuthServiceTest.java`

**Coverage (15 points):**
- 70%+ = 15 pts | 60-69% = 12 pts | 50-59% = 9 pts | 40-49% = 6 pts | <40% = 3 pts

**Required Scenarios (10 points):**
- [ ] Login success
- [ ] Login failure (invalid credentials)
- [ ] Logout state cleanup
- [ ] Token validation (valid)
- [ ] Token validation (invalid/expired)
- [ ] Error handling

### 4. Code Quality (10 points)

- **Builds (5 points):** No compilation errors
- **Tests Pass (5 points):** All tests green

## Output Requirements

Generate a complete grading report with:

1. **Score Summary Table** - Points for each category
2. **Letter Grade** - A (90+), B (80-89), C (70-79), D (60-69), F (<60)
3. **Detailed Feedback** - Specific findings with line references
4. **Recommendations** - 3 actionable improvements
5. **Commendations** - What the student did well

Use the exact format specified in the Lab Grader agent.
