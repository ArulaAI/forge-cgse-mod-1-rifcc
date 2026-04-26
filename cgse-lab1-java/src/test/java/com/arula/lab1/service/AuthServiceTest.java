package com.arula.lab1.service;

import com.arula.lab1.model.User;
import com.arula.lab1.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
@DisplayName("AuthService Tests")
class AuthServiceTest {

    @Mock
    private UserRepository userRepository;

    private AuthService authService;

    private User testUser;

    @BeforeEach
    void setUp() {
        authService = new AuthService(userRepository);

        testUser = User.builder()
            .id(1L)
            .email("test@example.com")
            .name("Test User")
            .password("password123")
            .role("USER")
            .build();
    }

    @Test
    @DisplayName("should be instantiated")
    void shouldBeInstantiated() {
        assertThat(authService).isNotNull();
    }

    // TODO: Students add more tests here using AI assistance
    // Target: >70% coverage on AuthService

    // Hints for tests to add:
    // - authenticate with valid credentials
    // - authenticate with invalid credentials
    // - authenticate with non-existent user
    // - register creates user
    // - validateToken with valid token
    // - validateToken with invalid token
    // - changePassword updates password
}
