# CGSE-A Lab 1: AI-Assisted Development Fundamentals (Java)

## Warning: Educational Purpose Only

This project contains **intentional security vulnerabilities** for training purposes.
**DO NOT** use this code in production!

## Quick Start

```bash
# Build project
mvn clean install -DskipTests

# Run application
mvn spring-boot:run

# Run tests with coverage
mvn test jacoco:report

# View coverage report
open target/site/jacoco/index.html
```

## Lab Tasks

1. **Security Audit** (15 min) - Find vulnerabilities in `UserService.java`
2. **Critique & Create** (20 min) - Refactor `AuthService.java`
3. **Test Coverage** (15 min) - Achieve >70% coverage
4. **Documentation** (10 min) - Complete docs in `/docs`

## Success Criteria

- [ ] 3+ vulnerabilities documented (including SQL injection)
- [ ] AuthService refactored (BCrypt, secure JWT)
- [ ] >70% test coverage
- [ ] All documentation complete

## Project Structure

```
src/main/java/com/arula/lab1/
  service/
    UserService.java       # Contains vulnerabilities - audit this
    AuthService.java       # PRIMARY FOCUS - critique and refactor
  model/
    User.java
  repository/
    UserRepository.java
  controller/
    UserController.java
  config/
    SecurityConfig.java

src/test/java/com/arula/lab1/
  service/
    UserServiceTest.java   # Minimal starter tests
    AuthServiceTest.java   # Add tests here

docs/
  SECURITY_AUDIT.md        # Fill in vulnerabilities found
  AUTH_SERVICE_CRITIQUE.md # Document top 5 issues
  AI_USAGE_LOG.md          # Track your AI prompts
```

## H2 Database Console

When the application is running, access the H2 console at:
- URL: http://localhost:8080/h2-console
- JDBC URL: jdbc:h2:mem:labdb
- Username: sa
- Password: (empty)

## Resources

- [OWASP Java Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Java_Security_Cheat_Sheet.html)
- [Spring Security Reference](https://docs.spring.io/spring-security/reference/)
- [RIFCC Framework](https://github.com/anthropics/courses/tree/master/prompt_engineering_interactive_tutorial)
