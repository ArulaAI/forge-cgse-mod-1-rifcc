---
agent: 'agent'
description: 'Perform a comprehensive OWASP Top 10 security audit on a service file with detailed vulnerability documentation.'
tools: ['search/codebase', 'search', 'web/fetch']
---

# Security Audit

Perform a comprehensive security audit on **${input:ServiceFile}** following OWASP Top 10 (2021) guidelines.

## Audit Scope

Analyze the specified service for these vulnerability categories:

| OWASP ID | Category | What to Look For |
|----------|----------|------------------|
| A01:2021 | Broken Access Control | Mass assignment, IDOR, missing authorization |
| A02:2021 | Cryptographic Failures | Plain text passwords, weak secrets, hardcoded keys |
| A03:2021 | Injection | SQL/NoSQL injection, command injection, XSS |
| A04:2021 | Insecure Design | Missing security controls, business logic flaws |
| A05:2021 | Security Misconfiguration | Debug enabled, default credentials, verbose errors |
| A06:2021 | Vulnerable Components | Outdated dependencies with known CVEs |
| A07:2021 | Auth Failures | Weak auth, session issues, credential stuffing |
| A08:2021 | Data Integrity Failures | Insecure deserialization, unsigned data |
| A09:2021 | Logging Failures | Sensitive data in logs, insufficient logging |
| A10:2021 | SSRF | Unvalidated URLs, internal resource access |

## Analysis Requirements

For **each vulnerability** found, document:

1. **Line Number** - Exact location in the code
2. **Code Snippet** - The vulnerable code (3-5 lines of context)
3. **OWASP Category** - e.g., A03:2021-Injection
4. **CWE Reference** - e.g., CWE-89 (SQL Injection)
5. **Severity** - Critical / High / Medium / Low
6. **Attack Scenario** - How an attacker would exploit this
7. **Business Impact** - What damage could result
8. **Remediation** - Specific fix with code example

## Output Format

```markdown
# Security Audit Report

**File:** [filename]
**Date:** [date]
**Auditor:** Security Audit Agent

## Executive Summary

| Severity | Count |
|----------|-------|
| Critical | X |
| High | X |
| Medium | X |
| Low | X |

**Overall Risk Level:** [Critical/High/Medium/Low]

---

## Findings

### [VULN-001] [Vulnerability Title]

| Attribute | Value |
|-----------|-------|
| **Location** | `file.ts:42` |
| **OWASP** | A03:2021-Injection |
| **CWE** | CWE-89 |
| **Severity** | Critical |

**Vulnerable Code:**
```[language]
// Lines 40-45
[code snippet]
```

**Attack Scenario:**
[Detailed explanation of how this could be exploited]

**Business Impact:**
[What damage could result - data breach, unauthorized access, etc.]

**Remediation:**
```[language]
// Secure implementation
[fixed code]
```

---

[Repeat for each vulnerability]

## Remediation Priority

| Priority | Vulnerability | Effort | Impact |
|----------|---------------|--------|--------|
| 1 | [VULN-XXX] | Low/Med/High | Critical |
| 2 | ... | ... | ... |

## Recommendations

1. **Immediate:** [Critical fixes needed before deployment]
2. **Short-term:** [High priority fixes for next sprint]
3. **Long-term:** [Security improvements for backlog]
```

## Important Notes

- Focus on **realistic, exploitable** vulnerabilities
- Provide **working remediation code**, not just descriptions
- Consider the **technology stack context** (Angular/Spring Boot)
- **Do not modify code** - this is analysis only
- Prioritize by **actual risk**, not theoretical concerns
