package com.arula.lab1.controller;

import com.arula.lab1.model.User;
import com.arula.lab1.service.AuthService;
import com.arula.lab1.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class UserController {

    private final UserService userService;
    private final AuthService authService;

    public UserController(UserService userService, AuthService authService) {
        this.userService = userService;
        this.authService = authService;
    }

    @GetMapping("/users")
    public List<User> getUsers() {
        return userService.findAll();
    }

    @GetMapping("/users/{id}")
    public ResponseEntity<User> getUserById(@PathVariable Long id) {
        User user = userService.findById(id);
        if (user == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(user);
    }

    @PostMapping("/users")
    public User createUser(@RequestBody User user) {
        return userService.createUser(user);
    }

    @PutMapping("/users/{id}")
    public ResponseEntity<User> updateUser(@PathVariable Long id, @RequestBody User user) {
        User updated = userService.updateUser(id, user);
        return ResponseEntity.ok(updated);
    }

    @DeleteMapping("/users/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        userService.deleteUser(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/users/search")
    public List<User> searchUsers(@RequestParam String name) {
        return userService.searchByName(name);
    }

    @GetMapping("/users/check-email")
    public boolean checkEmail(@RequestParam String email) {
        return userService.emailExists(email);
    }

    // Auth endpoints
    @PostMapping("/auth/register")
    public User register(@RequestBody Map<String, String> request) {
        return authService.register(
            request.get("email"),
            request.get("password"),
            request.get("name")
        );
    }

    @PostMapping("/auth/login")
    public ResponseEntity<Map<String, Object>> login(@RequestBody Map<String, String> request) {
        String token = authService.authenticate(
            request.get("email"),
            request.get("password")
        );

        if (token == null) {
            return ResponseEntity.status(401).body(Map.of("error", "Invalid credentials"));
        }

        return ResponseEntity.ok(Map.of("token", token));
    }

    @PostMapping("/auth/change-password")
    public ResponseEntity<Void> changePassword(@RequestBody Map<String, String> request) {
        Long userId = Long.parseLong(request.get("userId"));
        authService.changePassword(userId, request.get("newPassword"));
        return ResponseEntity.ok().build();
    }

    @PostMapping("/auth/reset-password")
    public ResponseEntity<Map<String, Boolean>> resetPassword(@RequestBody Map<String, String> request) {
        boolean result = authService.resetPassword(request.get("email"));
        return ResponseEntity.ok(Map.of("success", result));
    }
}
