# Forge Prowess — CGSE — Module 1: RIFCC

**Lab slug:** `cgse-mod-1` · **Repo:** `arula-ai/forge-cgse-mod-1-rifcc` (renamed from `forge-cgse-1`, Spec B §7) · **Track:** CGSE · **Status:** Modernized (Plan 16)

> **Dual-harness:** Read [`AGENTS.md`](./AGENTS.md) first. Modern arc lives in [`exercises/`](./exercises/) — walk → batch → validate → critique. The L3 [`/walk-rifcc`](./.forge/local/primitives/walk-rifcc/) primitive is the canonical F8 reference impl (also published upstream). The **rifcc-walker** sub-agent drives every exercise in Educator output style.

> **Quickstart:** `uv sync` → `make demo` → open `exercises/lab-1-rifcc-walk/instructions.md`.

## Forge primitives + CLI (modernized arc)

| Command | Purpose |
|---|---|
| `make demo` | Print the entry-point hint for the modernized arc |
| `make sync` | `forge sync` — refresh `.forge/primitives/` from the pinned primitive library version |
| `make validate` | `forge validate .` — schema-check `.forge/sim.yaml`, manifest, primitives |
| `make test` | `uv run pytest` — runs L3 walker tests + per-exercise smoke tests |
| `make grade` | `make test` + `lab_grader` — produces a weighted scorecard from `.forge/grader.yaml` |

Primitive layers used by this lab:

- **L1** — `rifcc-walker` agent (Claude + Copilot), Educator output style, `/walk-rifcc` and `/critique-prompts` slash commands, RIFCC rule (Claude path-scoped + Copilot `applyTo:`).
- **L2** — 7 primitives synced from `arula-ai/forge-prowess-primitives` v0.4.0: `journey_recorder`, `journey_curator`, `confidence_score`, `failure_mode_audit`, `hypothesis`, `spec_write`, `lab_grader`.
- **L3** — `/walk-rifcc` at `.forge/local/primitives/walk-rifcc/` (canonical F8 reference impl; pure-stdlib walker; 5 pytest cases). Also published upstream so every other lab can `forge sync` it.

---

# CGSE-Advanced Module 1: AI-Assisted Development Fundamentals

> Certified Generative Software Engineer - Advanced Training Series

## Overview

This module provides hands-on lab exercises for learning AI-assisted development techniques with a focus on **security vulnerability identification and remediation**. Students use GitHub Copilot (or similar AI assistants) with structured prompting frameworks to find, document, and fix security issues in real codebases.

### Learning Objectives

By completing this module, students will be able to:

1. **Apply the RIFCC framework** for effective AI prompts (Role, Instructions, Format, Context, Constraints)
2. **Identify security vulnerabilities** mapped to OWASP Top 10 categories
3. **Execute the "Critique then Create" pattern** for systematic code improvement
4. **Generate comprehensive tests** with AI assistance to achieve coverage targets

---

## Lab Projects

| Project | Technology | Focus Area |
|---------|------------|------------|
| [cgse-lab1-angular](./cgse-lab1-angular/) | Angular 17+, TypeScript | Client-side security (XSS, token storage, input validation) |
| [cgse-lab1-java](./cgse-lab1-java/) | Spring Boot 3.2, Java 17 | Server-side security (SQL injection, authentication, cryptography) |

Both projects contain **intentional security vulnerabilities** for educational purposes.

---

## Quick Start

### Angular Lab

```bash
cd cgse-lab1-angular
npm install
npm test              # Run tests
npm run test:ci       # Run with coverage
```

**Lab Guide**: [cgse-lab1-angular/LAB_ACTION_GUIDE.md](./cgse-lab1-angular/LAB_ACTION_GUIDE.md)

### Java Lab

```bash
cd cgse-lab1-java
mvn clean install -DskipTests
mvn test                      # Run tests
mvn jacoco:report             # Generate coverage
open target/site/jacoco/index.html
```

**Lab Guide**: [cgse-lab1-java/LAB_ACTION_GUIDE.md](./cgse-lab1-java/LAB_ACTION_GUIDE.md)

---

## Session Format

| Phase | Duration | Activity |
|-------|----------|----------|
| Instruction | 20 min | RIFCC framework, Critique-then-Create methodology |
| Hands-on Lab | 60 min | Security audit, refactoring, test generation |
| Q&A | 10 min | Discussion, review of findings |

---

## Lab Structure

Each lab follows a 5-stage workflow:

```
┌─────────────────────────────────────────────────────────────┐
│  Stage 0: Environment Setup                                  │
│  Verify builds, run tests, establish baseline coverage       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  CRITIQUE PHASE                                              │
├─────────────────────────────────────────────────────────────┤
│  Stage 1: Security Audit      → SECURITY_AUDIT.md           │
│  Stage 2: Deep Code Critique  → AUTH_SERVICE_CRITIQUE.md    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  CREATE PHASE                                                │
├─────────────────────────────────────────────────────────────┤
│  Stage 3: Secure Refactoring  → Fixed service code          │
│  Stage 4: Test Coverage       → >70% coverage               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Stage 5: Validation & Documentation                         │
│  Complete AI_USAGE_LOG.md, verify all criteria met          │
└─────────────────────────────────────────────────────────────┘
```

---

## RIFCC Framework

Structure your AI prompts with these five components:

| Component | Purpose | Example |
|-----------|---------|---------|
| **R**ole | Define AI expertise | "Act as a senior security engineer..." |
| **I**nstructions | Clear task description | "Identify OWASP Top 10 vulnerabilities..." |
| **F**ormat | Output structure | "Return as a markdown table..." |
| **C**ontext | Relevant background | "This is an Angular auth service using JWT..." |
| **C**onstraints | Boundaries | "Focus on client-side issues only..." |

---

## Vulnerabilities Overview

### Angular Project

| Service | Vulnerabilities | OWASP Categories |
|---------|-----------------|------------------|
| UserService | 5 | Injection, Logging, Access Control |
| AuthService | 8 | XSS (localStorage), Broken Auth, Security Misconfiguration |

### Java Project

| Service | Vulnerabilities | OWASP Categories |
|---------|-----------------|------------------|
| UserService | 6 | SQL Injection, Mass Assignment, Auth Failures |
| AuthService | 6 | Cryptographic Failures, Broken Auth, Security Logging |

---

## Success Criteria

Students must complete:

- [ ] Document 3+ vulnerabilities in `SECURITY_AUDIT.md`
- [ ] Document top 5 issues in `AUTH_SERVICE_CRITIQUE.md`
- [ ] Refactor AuthService to fix critical vulnerabilities
- [ ] Achieve >70% test coverage on AuthService
- [ ] Complete `AI_USAGE_LOG.md` with prompt documentation

---

## Repository Structure

```
cgse-module-1/
├── README.md                      # This file
├── LAB_BUILD_INSTRUCTIONS.md      # Build specifications (for instructors)
├── EX_LAB_ACTION_GUIDE.md         # Example guide format reference
│
├── cgse-lab1-angular/             # Angular Lab Project
│   ├── LAB_ACTION_GUIDE.md        # Step-by-step student guide
│   ├── README.md                  # Project quick start
│   ├── src/app/services/          # Vulnerable services
│   ├── docs/                      # Documentation templates
│   └── ...
│
└── cgse-lab1-java/                # Java Lab Project
    ├── LAB_ACTION_GUIDE.md        # Step-by-step student guide
    ├── README.md                  # Project quick start
    ├── src/main/java/.../service/ # Vulnerable services
    ├── docs/                      # Documentation templates
    └── ...
```

---

## Prerequisites

### Angular Lab
- Node.js 18+ and npm
- Chrome browser (for Karma tests)
- VS Code with GitHub Copilot

### Java Lab
- Java 17+ (JDK)
- Maven 3.8+
- VS Code or IntelliJ with GitHub Copilot

---

## Resources

### Security References
- [OWASP Top 10 (2021)](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Angular Security Guide](https://angular.io/guide/security)
- [Spring Security Reference](https://docs.spring.io/spring-security/reference/)

### AI-Assisted Development
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

---

## Important Notice

> **Warning**: This repository contains **intentional security vulnerabilities** for educational purposes. These projects are designed for controlled training environments only.
>
> **DO NOT**:
> - Deploy this code to production
> - Use these patterns in real applications
> - Remove vulnerability markers without fixing the underlying issues

---

## License

This training material is provided for educational use within the CGSE-Advanced certification program.

---

## Contributing

For issues or improvements to the lab materials, please contact the CGSE training team.
