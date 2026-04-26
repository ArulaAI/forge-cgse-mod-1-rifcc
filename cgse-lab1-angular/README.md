# CGSE-A Lab 1: AI-Assisted Development Fundamentals (Angular)

## Warning: Educational Purpose Only

This project contains **intentional security vulnerabilities** for training purposes.
**DO NOT** use this code in production!

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm start

# Run tests with coverage
npm run test:ci
```

## Lab Tasks

1. **Security Audit** (15 min) - Find vulnerabilities in `user.service.ts`
2. **Critique & Create** (20 min) - Refactor `auth.service.ts`
3. **Test Coverage** (15 min) - Achieve >70% coverage
4. **Documentation** (10 min) - Complete docs in `/docs`

## Success Criteria

- [ ] 3+ vulnerabilities documented
- [ ] AuthService refactored (no localStorage)
- [ ] >70% test coverage
- [ ] All documentation complete

## Project Structure

```
src/
  app/
    services/
      user.service.ts      # Contains vulnerabilities - audit this
      auth.service.ts      # PRIMARY FOCUS - critique and refactor
    models/
      user.model.ts
    components/
      user-detail/
docs/
  SECURITY_AUDIT.md        # Fill in vulnerabilities found
  AUTH_SERVICE_CRITIQUE.md # Document top 5 issues
  AI_USAGE_LOG.md          # Track your AI prompts
```

## Resources

- [Angular Security Guide](https://angular.io/guide/security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [RIFCC Framework](https://github.com/anthropics/courses/tree/master/prompt_engineering_interactive_tutorial)
