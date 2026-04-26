# Lab Action Guide – Angular Security Lab

Follow these lean steps using the **Critique-then-Create** methodology with the **RIFCC** prompting framework. This lab focuses on identifying and remediating security vulnerabilities in Angular services.

## RIFCC Framework Quick Reference

| Component | Description | Example |
|-----------|-------------|---------|
| **R**ole | Define AI's expertise | "Act as a senior security engineer..." |
| **I**nstructions | Clear task description | "Analyze this service for OWASP Top 10 vulnerabilities" |
| **F**ormat | Desired output structure | "Return findings as a markdown table" |
| **C**ontext | Relevant background | "This is an Angular 17 authentication service" |
| **C**onstraints | Limitations/requirements | "Focus only on client-side vulnerabilities" |

---

## Quick Reference

| Stage | Focus Area | Core Artifacts / Commands |
|-------|------------|---------------------------|
| 0 | Environment Setup | `npm install`, `npm test`, `npm run test:ci` |
| 1 | Security Audit (CRITIQUE) | `docs/SECURITY_AUDIT.md`, vulnerability identification |
| 2 | AuthService Critique (CRITIQUE) | `docs/AUTH_SERVICE_CRITIQUE.md`, top 5 issues |
| 3 | Refactoring (CREATE) | Fixed `auth.service.ts`, secure implementation |
| 4 | Test Coverage (CREATE) | `auth.service.spec.ts`, >70% coverage |
| 5 | Final Validation | All tests pass, documentation complete |

---

## Stage 0 – Environment Setup

**Objective**: Verify the project builds and tests run successfully.

### Commands
```bash
# Navigate to project
cd cgse-lab1-angular

# Install dependencies
npm install

# Run tests to verify setup
npm test

# Run tests with coverage (establish baseline)
npm run test:ci
```

### Verification Checklist
- [ ] `npm install` completes without errors
- [ ] `npm test` launches Karma and tests pass
- [ ] Coverage report generates in `coverage/cgse-lab1-angular/`
- [ ] Note baseline coverage percentage: ____%

### Expected Baseline
- Tests: 4 passing (minimal starter tests)
- Coverage: ~29% (starter code only)

---

## Stage 1 – Security Audit (CRITIQUE Phase)

**Objective**: Identify security vulnerabilities in `user.service.ts` using AI assistance.

### Step 1.1 – Craft Your RIFCC Prompt

Open GitHub Copilot Chat and use this structured prompt:

```
Role: Act as a senior application security engineer specializing in Angular and OWASP Top 10 vulnerabilities.

Instructions: Analyze the UserService file for security vulnerabilities. For each vulnerability found:
1. Identify the line number
2. Classify by OWASP category
3. Assess severity (Critical/High/Medium/Low)
4. Explain the risk
5. Provide a remediation recommendation

Format: Return findings as a markdown table with columns: Line, OWASP Category, Severity, Description, Suggested Fix

Context: This is an Angular 17+ service that handles user data operations including CRUD and search functionality. It communicates with a REST API.

Constraints: Focus on client-side vulnerabilities. Do not modify the code yet - only analyze and document.
```

### Step 1.2 – Analyze the File

Reference the file in your prompt:
- Use `#file:src/app/services/user.service.ts` in Copilot Chat

### Step 1.3 – Document Findings

Copy AI findings to `docs/SECURITY_AUDIT.md` and validate each one:

```bash
# Open the security audit template
code docs/SECURITY_AUDIT.md
```

### Expected Vulnerabilities to Find

| # | Line | Type | Severity |
|---|------|------|----------|
| 1 | ~38 | A03:2021 Injection | High |
| 2 | ~44 | A09:2021 Logging | Medium |
| 3 | ~50 | A09:2021 Logging | High |
| 4 | ~55 | A01:2021 Broken Access Control | High |
| 5 | ~65 | A01:2021 User Enumeration | Medium |

### Verification
- [ ] Minimum 3 vulnerabilities documented
- [ ] Each has OWASP classification
- [ ] Each has severity rating
- [ ] Each has suggested fix

---

## Stage 2 – AuthService Deep Critique (CRITIQUE Phase)

**Objective**: Perform detailed analysis of `auth.service.ts` - the PRIMARY FOCUS of this lab.

### Step 2.1 – Craft Your RIFCC Prompt

```
Role: Act as a principal security architect with expertise in authentication systems, JWT security, and Angular best practices.

Instructions: Perform a comprehensive security and code quality review of this AuthService. Identify the top 5 most critical issues across these categories:
- Security vulnerabilities
- Code quality issues
- Performance concerns
- Testability problems

For each issue, explain WHY it's problematic and HOW to fix it.

Format: Structure your response as:
### Issue 1: [Title]
- **Line:** [number]
- **Category:** Security | Quality | Performance | Testability
- **Risk:** [Explain the danger]
- **Fix:** [Specific remediation steps]

Context: This is an Angular 17+ authentication service using JWT tokens. It handles login, logout, registration, and token management. The application will be deployed in a production environment.

Constraints: Prioritize by severity. Include code examples for fixes where helpful.
```

### Step 2.2 – Reference the File

```
#file:src/app/services/auth.service.ts
```

### Step 2.3 – Document in Critique Template

Update `docs/AUTH_SERVICE_CRITIQUE.md` with your findings.

### Expected Issues to Find

| Priority | Issue | Category |
|----------|-------|----------|
| 1 | localStorage token storage (XSS risk) | Security |
| 2 | Sensitive data logged to console | Security |
| 3 | JWT parsed without signature verification | Security |
| 4 | Using `any` type for user object | Quality |
| 5 | No token expiration validation in `isAuthenticated()` | Security |
| 6 | Incomplete logout (no server invalidation) | Security |
| 7 | Magic number for token expiry | Quality |
| 8 | No input validation on register/login | Security |

### Verification
- [ ] Top 5 issues documented in `AUTH_SERVICE_CRITIQUE.md`
- [ ] Each issue has line number
- [ ] Each issue has category
- [ ] Each issue has recommended fix

---

## Stage 3 – Secure Refactoring (CREATE Phase)

**Objective**: Refactor `auth.service.ts` to address identified vulnerabilities.

### Step 3.1 – Plan Your Refactoring

Create a refactoring checklist based on your critique:

```
Priority fixes for auth.service.ts:
1. [ ] Replace localStorage with secure alternatives
2. [ ] Remove all console.log statements with sensitive data
3. [ ] Add proper TypeScript interfaces (remove 'any')
4. [ ] Implement proper token validation
5. [ ] Add input validation for email/password
6. [ ] Implement proper logout with server notification
```

### Step 3.2 – Craft Your CREATE Prompt

```
Role: Act as a senior Angular developer with security expertise.

Instructions: Refactor the AuthService to fix the security vulnerabilities I identified. Implement these specific changes:

1. Replace localStorage with sessionStorage (or explain httpOnly cookie approach)
2. Remove all console.log statements that expose sensitive data
3. Create a proper User interface to replace 'any' types
4. Add token expiration check in isAuthenticated()
5. Add basic email format and password length validation
6. Add server-side logout call

Format: Provide the complete refactored service file with comments explaining each security improvement.

Context: This is the existing auth.service.ts with known vulnerabilities:
#file:src/app/services/auth.service.ts

Reference my critique:
#file:docs/AUTH_SERVICE_CRITIQUE.md

Constraints:
- Maintain the same public API (method signatures)
- Ensure backward compatibility
- Add JSDoc comments for security-relevant methods
```

### Step 3.3 – Implement Changes

Apply the AI-generated refactoring, reviewing each change:

```bash
# After making changes, verify the app still compiles
npm run build 2>&1 | head -20
```

### Key Refactoring Targets

| Original | Refactored |
|----------|------------|
| `localStorage.setItem('auth_token', ...)` | `sessionStorage` or secure cookie |
| `console.log('Token:', response.token)` | Remove entirely |
| `currentUser: any` | `currentUser: User \| null` |
| `return !!token` | Check token + expiration |
| No validation | Email regex + password length check |

### Verification
- [ ] No `localStorage` for sensitive data
- [ ] No `console.log` with tokens/passwords
- [ ] No `any` types for user data
- [ ] `isAuthenticated()` checks token expiry
- [ ] App compiles without errors

---

## Stage 4 – Test Coverage (CREATE Phase)

**Objective**: Achieve >70% test coverage on AuthService.

### Step 4.1 – Review Current Tests

```bash
# Check current test file
cat src/app/services/auth.service.spec.ts

# Run tests with coverage
npm run test:ci
```

### Step 4.2 – Generate Tests with AI

```
Role: Act as an Angular testing expert specializing in Jasmine/Karma and security testing.

Instructions: Generate comprehensive unit tests for the AuthService to achieve >70% code coverage. Include tests for:

1. login() - success and failure scenarios
2. logout() - verify state cleanup
3. isAuthenticated() - token present/absent/expired
4. register() - with validation
5. Token handling - storage, retrieval, expiration
6. Error scenarios - network failures, invalid responses

Format: Provide complete test file using Angular TestBed and HttpClientTestingModule.

Context:
- Current test file: #file:src/app/services/auth.service.spec.ts
- Service under test: #file:src/app/services/auth.service.ts
- Using Jasmine/Karma test framework
- Angular 17+ with standalone components

Constraints:
- Use HttpClientTestingModule for HTTP mocking
- Clear localStorage/sessionStorage in beforeEach/afterEach
- Test both happy path and error scenarios
- Include security-focused tests (e.g., verify no sensitive data logged)
```

### Step 4.3 – Implement and Verify Tests

```bash
# Run specific service tests
npm test -- --include="**/auth.service.spec.ts"

# Run with coverage
npm run test:ci

# Check coverage report
open coverage/cgse-lab1-angular/index.html
```

### Test Scenarios Checklist

| Scenario | Test Name |
|----------|-----------|
| Login success | `should login and store token` |
| Login failure | `should handle invalid credentials` |
| Logout | `should clear token and user on logout` |
| isAuthenticated true | `should return true when valid token exists` |
| isAuthenticated false | `should return false when no token` |
| Token expired | `should return false when token expired` |
| Register success | `should register new user` |
| Register validation | `should validate email format` |

### Verification
- [ ] All tests pass: `npm test`
- [ ] Coverage >70% on AuthService
- [ ] Security scenarios covered

---

## Stage 5 – Final Validation & Documentation

**Objective**: Complete all documentation and verify success criteria.

### Step 5.1 – Complete AI Usage Log

Update `docs/AI_USAGE_LOG.md` with your prompts:

```bash
code docs/AI_USAGE_LOG.md
```

Document for each prompt:
- Purpose
- RIFCC components used
- AI output quality (1-5)
- Modifications you made

### Step 5.2 – Final Verification Commands

```bash
# All tests pass
npm test

# Coverage meets threshold
npm run test:ci

# No lint errors (if configured)
npm run lint 2>/dev/null || echo "Lint not configured"

# Build succeeds
npm run build
```

### Step 5.3 – Success Criteria Checklist

| Criterion | Status |
|-----------|--------|
| 3+ vulnerabilities documented in `SECURITY_AUDIT.md` | [ ] |
| Top 5 issues documented in `AUTH_SERVICE_CRITIQUE.md` | [ ] |
| AuthService refactored (no localStorage for tokens) | [ ] |
| No sensitive data in console.log | [ ] |
| No `any` types for user data | [ ] |
| >70% test coverage on AuthService | [ ] |
| All tests passing | [ ] |
| `AI_USAGE_LOG.md` completed | [ ] |

---

## RIFCC Prompt Templates

### Security Audit Prompt
```
Role: Senior security engineer, OWASP expertise
Instructions: Find vulnerabilities, classify by OWASP
Format: Markdown table (Line, Category, Severity, Description, Fix)
Context: Angular service, REST API communication
Constraints: Client-side only, document don't fix
```

### Code Critique Prompt
```
Role: Principal security architect
Instructions: Top 5 critical issues with explanations
Format: Numbered issues with Line, Category, Risk, Fix
Context: Auth service, JWT, production deployment
Constraints: Prioritize by severity
```

### Refactoring Prompt
```
Role: Senior Angular developer, security focus
Instructions: Fix specific vulnerabilities listed
Format: Complete refactored file with comments
Context: Reference original file and critique
Constraints: Maintain API compatibility
```

### Test Generation Prompt
```
Role: Angular testing expert
Instructions: Generate tests for >70% coverage
Format: Complete spec file with TestBed
Context: Jasmine/Karma, HttpClientTestingModule
Constraints: Cover happy path and error scenarios
```

---

## Workflow Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                    CRITIQUE PHASE                                │
├─────────────────────────────────────────────────────────────────┤
│  Stage 1: Security Audit    →  docs/SECURITY_AUDIT.md           │
│  Stage 2: AuthService Deep  →  docs/AUTH_SERVICE_CRITIQUE.md    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    CREATE PHASE                                  │
├─────────────────────────────────────────────────────────────────┤
│  Stage 3: Refactoring       →  Secure auth.service.ts           │
│  Stage 4: Test Coverage     →  auth.service.spec.ts (>70%)      │
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

## Resources

- [Angular Security Guide](https://angular.io/guide/security)
- [OWASP Top 10 2021](https://owasp.org/www-project-top-ten/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [JWT Security Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
