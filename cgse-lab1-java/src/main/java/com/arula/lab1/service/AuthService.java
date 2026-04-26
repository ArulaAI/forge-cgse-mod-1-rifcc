/**
 * CGSE-A Lab 1 - Java/Spring Boot Starter Code
 * AuthService - PRIMARY FOCUS for Critique & Create
 *
 * WARNING: Contains INTENTIONAL security vulnerabilities!
 *
 * VULNERABILITIES TO FIND:
 * 1. Line ~30: Hardcoded weak JWT secret
 * 2. Line ~45: Plain text password storage
 * 3. Line ~55: Timing attack in authentication
 * 4. Line ~90: No old password verification in change
 * 5. Line ~100: Information disclosure in password reset
 * 6. Line ~115: JWT can't be invalidated (logout issue)
 */

package com.arula.lab1.service;

import com.arula.lab1.model.User;
import com.arula.lab1.repository.UserRepository;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@Service
public class AuthService {

    private final UserRepository userRepository;

    // VULNERABILITY 1: Hardcoded weak secret
    private static final String JWT_SECRET = "secret123secret123secret123secret123";

    // VULNERABILITY: Very long expiration
    private static final long JWT_EXPIRATION_MS = 30L * 24 * 60 * 60 * 1000; // 30 days

    public AuthService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    // VULNERABILITY 2: Plain text password storage
    public User register(String email, String password, String name) {
        User user = new User();
        user.setEmail(email);
        user.setName(name);
        user.setPassword(password); // NOT HASHED!
        return userRepository.save(user);
    }

    // VULNERABILITY 3: Timing attack
    public String authenticate(String email, String password) {
        User user = userRepository.findByEmail(email).orElse(null);

        // Early return reveals user existence
        if (user == null) {
            return null;
        }

        // Plain text comparison
        if (!user.getPassword().equals(password)) {
            System.out.println("Failed login for: " + email); // Info disclosure
            return null;
        }

        return generateToken(user);
    }

    private String generateToken(User user) {
        Map<String, Object> claims = new HashMap<>();
        claims.put("userId", user.getId());
        claims.put("email", user.getEmail());
        claims.put("role", user.getRole());

        SecretKey key = Keys.hmacShaKeyFor(JWT_SECRET.getBytes(StandardCharsets.UTF_8));

        return Jwts.builder()
            .claims(claims)
            .subject(user.getId().toString())
            .issuedAt(new Date())
            .expiration(new Date(System.currentTimeMillis() + JWT_EXPIRATION_MS))
            .signWith(key)
            .compact();
    }

    public boolean validateToken(String token) {
        try {
            SecretKey key = Keys.hmacShaKeyFor(JWT_SECRET.getBytes(StandardCharsets.UTF_8));
            Jwts.parser().verifyWith(key).build().parseSignedClaims(token);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    // VULNERABILITY 4: No old password verification
    public void changePassword(Long userId, String newPassword) {
        User user = userRepository.findById(userId).orElse(null);
        if (user != null) {
            user.setPassword(newPassword); // Not hashed, no old password check
            userRepository.save(user);
            System.out.println("Password changed for: " + user.getEmail());
        }
    }

    // VULNERABILITY 5: Information disclosure
    public boolean resetPassword(String email) {
        User user = userRepository.findByEmail(email).orElse(null);

        if (user == null) {
            System.out.println("Reset for non-existent: " + email);
            return false; // Reveals email doesn't exist
        }

        String tempPassword = "temp" + System.currentTimeMillis(); // Predictable!
        user.setPassword(tempPassword);
        userRepository.save(user);
        System.out.println("Temp password for " + email + ": " + tempPassword);
        return true;
    }

    // VULNERABILITY 6: JWT can't be invalidated
    public void logout(String token) {
        System.out.println("Logout called but token still valid!");
        // JWTs are stateless - can't invalidate without blacklist
    }
}
