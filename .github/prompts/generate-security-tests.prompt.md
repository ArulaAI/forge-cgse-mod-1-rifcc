---
agent: 'agent'
description: 'Generate comprehensive security-focused unit tests for authentication services targeting 70%+ coverage.'
tools: ['search/codebase', 'edit/editFiles', 'search', 'execute/testFailure']
---

# Generate Security Tests

Generate comprehensive unit tests for **${input:TestFile}** with focus on security scenarios.

## Target Coverage

- **Line Coverage:** >70%
- **Branch Coverage:** >60%
- **Focus:** Security-critical paths and error handling

## Required Test Scenarios

### Authentication Tests

| Scenario | Priority | Description |
|----------|----------|-------------|
| Login Success | High | Valid credentials return token/session |
| Login Invalid Password | High | Wrong password rejected, generic error |
| Login Non-existent User | High | Unknown user rejected, same error as invalid password (prevent enumeration) |
| Login Empty Credentials | Medium | Empty email/password handled gracefully |
| Login Timing | High | Response time consistent for valid/invalid users |

### Session/Token Tests

| Scenario | Priority | Description |
|----------|----------|-------------|
| Token Generation | High | Valid login produces properly formatted token |
| Token Validation Valid | High | Valid token passes validation |
| Token Validation Invalid | High | Malformed token rejected |
| Token Validation Expired | High | Expired token rejected |
| Token Refresh | Medium | Refresh token flow works (if implemented) |

### Logout Tests

| Scenario | Priority | Description |
|----------|----------|-------------|
| Logout Clears State | High | All session data cleared on logout |
| Logout Token Invalid | Medium | Token unusable after logout (if server-side invalidation) |

### Security-Specific Tests

| Scenario | Priority | Description |
|----------|----------|-------------|
| Password Hashing | Critical | Verify passwords not stored plain text |
| No Sensitive Logging | Critical | Mock logger to verify no tokens/passwords logged |
| Input Validation | High | Invalid email format rejected |
| Password Strength | Medium | Weak passwords rejected (if implemented) |

### Error Handling Tests

| Scenario | Priority | Description |
|----------|----------|-------------|
| Network Error | Medium | API failure handled gracefully |
| Server Error | Medium | 500 responses handled gracefully |
| Generic Errors | High | Error messages don't leak information |

## Framework-Specific Templates

### Angular (Jasmine/Karma)

```typescript
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { AuthService } from './auth.service';

describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    // Clear storage before each test
    localStorage.clear();
    sessionStorage.clear();

    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AuthService]
    });

    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
    sessionStorage.clear();
  });

  describe('login', () => {
    it('should return token on successful login', () => {
      // Arrange
      const mockResponse = { token: 'jwt.token.here', user: { id: '1', email: 'test@test.com' } };

      // Act
      service.login('test@test.com', 'password123').subscribe(response => {
        // Assert
        expect(response.token).toBeTruthy();
      });

      // Mock HTTP
      const req = httpMock.expectOne('/api/auth/login');
      expect(req.request.method).toBe('POST');
      req.flush(mockResponse);
    });

    it('should handle invalid credentials', () => {
      // Test implementation
    });
  });

  describe('security', () => {
    it('should not log sensitive data', () => {
      // Spy on console.log
      spyOn(console, 'log');

      // Perform login
      // ...

      // Verify no sensitive data logged
      expect(console.log).not.toHaveBeenCalledWith(jasmine.stringMatching(/token|password/i));
    });
  });
});
```

### Java (JUnit 5/Mockito)

```java
@ExtendWith(MockitoExtension.class)
@DisplayName("AuthService Security Tests")
class AuthServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private AuthService authService;

    private User testUser;

    @BeforeEach
    void setUp() {
        testUser = User.builder()
            .id(1L)
            .email("test@example.com")
            .password("$2a$10$hashedpassword")  // BCrypt hash
            .role("USER")
            .build();
    }

    @Nested
    @DisplayName("Authentication Tests")
    class AuthenticationTests {

        @Test
        @DisplayName("should authenticate with valid credentials")
        void shouldAuthenticateWithValidCredentials() {
            // Arrange
            when(userRepository.findByEmail("test@example.com"))
                .thenReturn(Optional.of(testUser));
            when(passwordEncoder.matches("password123", testUser.getPassword()))
                .thenReturn(true);

            // Act
            String token = authService.authenticate("test@example.com", "password123");

            // Assert
            assertThat(token).isNotNull();
            assertThat(token).isNotEmpty();
        }

        @Test
        @DisplayName("should reject invalid password with generic error")
        void shouldRejectInvalidPassword() {
            // Arrange
            when(userRepository.findByEmail("test@example.com"))
                .thenReturn(Optional.of(testUser));
            when(passwordEncoder.matches("wrongpassword", testUser.getPassword()))
                .thenReturn(false);

            // Act
            String token = authService.authenticate("test@example.com", "wrongpassword");

            // Assert
            assertThat(token).isNull();
        }

        @Test
        @DisplayName("should handle non-existent user same as invalid password")
        void shouldHandleNonExistentUser() {
            // Arrange
            when(userRepository.findByEmail("nonexistent@example.com"))
                .thenReturn(Optional.empty());

            // Act & Assert - should not throw, should return null
            String token = authService.authenticate("nonexistent@example.com", "anypassword");
            assertThat(token).isNull();
        }
    }

    @Nested
    @DisplayName("Security Tests")
    class SecurityTests {

        @Test
        @DisplayName("should hash passwords on registration")
        void shouldHashPasswordsOnRegistration() {
            // Arrange
            when(passwordEncoder.encode("plainpassword"))
                .thenReturn("$2a$10$hashedvalue");
            when(userRepository.save(any(User.class)))
                .thenAnswer(inv -> inv.getArgument(0));

            // Act
            User user = authService.register("new@example.com", "plainpassword", "New User");

            // Assert
            verify(passwordEncoder).encode("plainpassword");
            assertThat(user.getPassword()).isNotEqualTo("plainpassword");
        }
    }
}
```

## Output Requirements

Generate a complete test file that:

1. **Follows framework conventions** (Jasmine for Angular, JUnit 5 for Java)
2. **Includes all imports** needed to run
3. **Has descriptive test names** using `@DisplayName` or `describe/it`
4. **Groups related tests** using `@Nested` or `describe`
5. **Covers all required scenarios** listed above
6. **Uses proper mocking** for dependencies
7. **Includes security-specific tests** for logging and data protection
8. **Has setup/teardown** to ensure test isolation

## Coverage Verification

After generating tests, suggest commands to verify coverage:

**Angular:**
```bash
npm run test:ci
open coverage/cgse-lab1-angular/index.html
```

**Java:**
```bash
mvn test jacoco:report
open target/site/jacoco/index.html
```
