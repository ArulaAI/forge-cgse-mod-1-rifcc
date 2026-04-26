/**
 * CGSE-A Lab 1 - Angular Starter Code
 * UserService - Contains INTENTIONAL security vulnerabilities
 *
 * WARNING: DO NOT use in production!
 *
 * VULNERABILITIES TO FIND:
 * 1. Line ~50: URL parameter injection (string interpolation)
 * 2. Line ~55: PII logging to console
 * 3. Line ~60: Mass assignment (accepts any fields)
 * 4. Line ~75: User enumeration endpoint
 * 5. Line ~65: No error handling
 */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { User } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = 'http://localhost:3000/api';

  constructor(private http: HttpClient) {}

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiUrl}/users`);
  }

  getUserById(id: string): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/users/${id}`);
  }

  // VULNERABILITY 1: SQL-like injection via URL parameter
  // Direct string interpolation allows injection attacks
  getUserByFilter(filter: string): Observable<User[]> {
    // VULNERABLE: Direct interpolation without encoding
    return this.http.get<User[]>(`${this.apiUrl}/users?filter=${filter}`);
  }

  // VULNERABILITY 2: PII logging
  searchUsers(query: string): Observable<User[]> {
    console.log('Search query:', query); // May log PII
    return this.http.get<User[]>(`${this.apiUrl}/users/search?q=${query}`);
  }

  // VULNERABILITY 3: No input validation, PII logged
  createUser(user: User): Observable<User> {
    console.log('Creating user:', user); // Logs entire user object including password
    return this.http.post<User>(`${this.apiUrl}/users`, user);
  }

  // VULNERABILITY 4: Mass assignment - accepts any fields
  updateUser(id: string, user: Partial<User>): Observable<User> {
    // Could update role, isAdmin, etc.
    return this.http.put<User>(`${this.apiUrl}/users/${id}`, user);
  }

  deleteUser(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/users/${id}`);
  }

  // VULNERABILITY 5: Information disclosure - user enumeration
  checkEmailExists(email: string): Observable<boolean> {
    // Allows attackers to enumerate valid emails
    return this.http.get<boolean>(`${this.apiUrl}/users/check-email?email=${email}`);
  }
}
