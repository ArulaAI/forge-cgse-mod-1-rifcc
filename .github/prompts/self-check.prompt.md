---
agent: 'agent'
description: 'Quick self-assessment of lab progress against success criteria with completion percentage and next steps.'
tools: ['search/codebase', 'search', 'read/problems']
---

# Self-Check Lab Progress

Quickly assess your current progress against the CGSE Module 1 lab success criteria.

## Assessment Areas

Review your submission and check each item:

### Documentation Checklist

```
docs/SECURITY_AUDIT.md
├── [ ] File exists
├── [ ] Contains 3+ vulnerabilities
├── [ ] Each has OWASP category
├── [ ] Each has severity rating
├── [ ] Each has line numbers
└── [ ] Each has remediation suggestion

docs/AUTH_SERVICE_CRITIQUE.md
├── [ ] File exists
├── [ ] Contains 5 documented issues
├── [ ] Each has line number
├── [ ] Each has category
└── [ ] Each has recommended fix

docs/AI_USAGE_LOG.md
├── [ ] File exists
├── [ ] 3+ prompts documented
├── [ ] RIFCC components marked
└── [ ] Quality ratings provided
```

### Security Fixes Checklist

**Angular (auth.service.ts):**
```
├── [ ] No localStorage for auth tokens
├── [ ] No console.log with tokens/passwords
├── [ ] No 'any' types for user data
├── [ ] isAuthenticated() checks token expiry
├── [ ] Email validation present
└── [ ] Password validation present
```

**Java (AuthService.java):**
```
├── [ ] BCrypt used for passwords
├── [ ] No System.out.println with sensitive data
├── [ ] JWT secret from configuration (not hardcoded)
├── [ ] Constant-time password comparison
├── [ ] Generic error messages (no enumeration)
└── [ ] Old password required for change
```

### Test Coverage Checklist

```
Test Scenarios Present:
├── [ ] Login success test
├── [ ] Login failure test
├── [ ] Logout test
├── [ ] Token validation (valid)
├── [ ] Token validation (invalid/expired)
└── [ ] Error handling test

Coverage Target:
└── [ ] >70% line coverage on AuthService
```

### Build Status Checklist

```
├── [ ] Code compiles without errors
└── [ ] All tests pass
```

## Quick Verification Commands

### Angular
```bash
# Check for security issues
grep -n "localStorage" src/app/services/auth.service.ts
grep -n "console.log" src/app/services/auth.service.ts
grep -n ": any" src/app/services/auth.service.ts

# Check documentation
ls -la docs/
wc -l docs/*.md

# Run tests
npm run test:ci
```

### Java
```bash
# Check for security issues
grep -n "System.out" src/main/java/com/arula/lab1/service/AuthService.java
grep -n "BCrypt\|passwordEncoder" src/main/java/com/arula/lab1/service/AuthService.java
grep -n "secret123" src/main/java/com/arula/lab1/service/AuthService.java

# Check documentation
ls -la docs/
wc -l docs/*.md

# Run tests
mvn test jacoco:report
```

## Output Format

Provide your assessment as:

```markdown
# Lab Progress Self-Check

**Project:** [Angular/Java]
**Timestamp:** [Current time]

---

## Completion Summary

| Category | Status | Progress |
|----------|--------|----------|
| Documentation | 🟢/🟡/🔴 | X/3 files |
| Security Fixes | 🟢/🟡/🔴 | X/6 items |
| Test Coverage | 🟢/🟡/🔴 | X% |
| Build Status | 🟢/🔴 | Pass/Fail |

**Overall Progress: X%**

---

## Completed Items ✅

- [List of completed items]

## In Progress 🔄

- [Items partially done with notes]

## Not Started ❌

- [Items not yet attempted]

---

## Priority Next Steps

1. **[Highest Priority]** - [Specific action]
   - Why: [Reason this is important]
   - How: [Brief guidance]

2. **[Second Priority]** - [Specific action]
   - Why: [Reason]
   - How: [Guidance]

3. **[Third Priority]** - [Specific action]
   - Why: [Reason]
   - How: [Guidance]

---

## Time Estimate

- **Remaining work:** ~X minutes
- **On track for completion:** Yes/No

---

## Tips

[1-2 specific tips based on what's missing]
```

## Status Indicators

| Icon | Meaning |
|------|---------|
| 🟢 | Complete (>80%) |
| 🟡 | In Progress (40-80%) |
| 🔴 | Not Started (<40%) |
| ✅ | Item complete |
| 🔄 | Item in progress |
| ❌ | Item not started |
