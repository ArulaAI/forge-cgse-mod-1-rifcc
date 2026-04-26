package com.arula.lab1.service;

import com.arula.lab1.model.User;
import com.arula.lab1.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
@DisplayName("UserService Tests")
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    private UserService userService;

    private User testUser;

    @BeforeEach
    void setUp() {
        userService = new UserService(userRepository);

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
        assertThat(userService).isNotNull();
    }

    @Test
    @DisplayName("should find all users")
    void shouldFindAllUsers() {
        when(userRepository.findAll()).thenReturn(Arrays.asList(testUser));

        List<User> users = userService.findAll();

        assertThat(users).hasSize(1);
        assertThat(users.get(0).getEmail()).isEqualTo("test@example.com");
    }

    @Test
    @DisplayName("should find user by id")
    void shouldFindUserById() {
        when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));

        User user = userService.findById(1L);

        assertThat(user).isNotNull();
        assertThat(user.getEmail()).isEqualTo("test@example.com");
    }

    // TODO: Students add more tests here using AI assistance
    // Consider testing:
    // - createUser
    // - updateUser
    // - deleteUser
    // - verifyCredentials (and its security implications)
    // - emailExists
}
