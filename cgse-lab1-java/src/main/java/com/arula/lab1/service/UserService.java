/**
 * CGSE-A Lab 1 - Java/Spring Boot Starter Code
 * UserService - Contains INTENTIONAL security vulnerabilities
 *
 * WARNING: DO NOT use in production!
 *
 * VULNERABILITIES TO FIND:
 * 1. Line ~55: SQL Injection via JPQL string concatenation
 * 2. Line ~65: SQL Injection via LIKE clause
 * 3. Line ~75: PII/Password logging
 * 4. Line ~85: Mass assignment via BeanUtils.copyProperties
 * 5. Line ~95: Timing attack in credential verification
 * 6. Line ~100: Plain text password comparison
 */

package com.arula.lab1.service;

import com.arula.lab1.model.User;
import com.arula.lab1.repository.UserRepository;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {

    private final UserRepository userRepository;

    @PersistenceContext
    private EntityManager entityManager;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public List<User> findAll() {
        return userRepository.findAll();
    }

    public User findById(Long id) {
        return userRepository.findById(id).orElse(null);
    }

    // VULNERABILITY 1: SQL Injection via JPQL concatenation
    public User findByEmailUnsafe(String email) {
        String jpql = "SELECT u FROM User u WHERE u.email = '" + email + "'";
        try {
            return entityManager.createQuery(jpql, User.class).getSingleResult();
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage()); // Info disclosure
            return null;
        }
    }

    // VULNERABILITY 2: SQL Injection via LIKE clause
    public List<User> searchByName(String namePattern) {
        String jpql = "SELECT u FROM User u WHERE u.name LIKE '%" + namePattern + "%'";
        return entityManager.createQuery(jpql, User.class).getResultList();
    }

    // VULNERABILITY 3: PII and password logging
    public User createUser(User user) {
        System.out.println("Creating user: " + user.toString());
        System.out.println("Password: " + user.getPassword()); // CRITICAL!
        return userRepository.save(user);
    }

    // VULNERABILITY 4: Mass assignment
    public User updateUser(Long id, User updatedUser) {
        User user = findById(id);
        if (user == null) {
            throw new RuntimeException("User not found");
        }
        // Copies ALL fields including role, isAdmin, etc.
        BeanUtils.copyProperties(updatedUser, user, "id");
        return userRepository.save(user);
    }

    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }

    // VULNERABILITY 5: Timing attack
    // VULNERABILITY 6: Plain text password comparison
    public boolean verifyCredentials(String email, String password) {
        User user = userRepository.findByEmail(email).orElse(null);

        // Timing attack: fast return if user doesn't exist
        if (user == null) {
            return false;
        }

        // Plain text comparison (no hashing)
        return user.getPassword().equals(password);
    }

    // VULNERABILITY: User enumeration
    public boolean emailExists(String email) {
        return userRepository.existsByEmail(email);
    }
}
