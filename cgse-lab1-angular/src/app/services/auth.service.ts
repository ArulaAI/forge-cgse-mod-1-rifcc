/**
 * CGSE-A Lab 1 - Angular Starter Code
 * AuthService - PRIMARY FOCUS for Critique & Create
 *
 * WARNING: Contains INTENTIONAL security vulnerabilities!
 *
 * VULNERABILITIES TO FIND:
 * 1. Line ~40: Token stored in localStorage (XSS risk)
 * 2. Line ~25: 'any' types used (type safety)
 * 3. Line ~50: Token and user logged to console
 * 4. Line ~85: No token validation (only checks existence)
 * 5. Line ~30: No subscription cleanup (memory leak)
 * 6. Line ~35: Hardcoded token expiry magic number
 * 7. Line ~70: Incomplete logout (doesn't invalidate server session)
 * 8. Line ~90: JWT parsed without signature validation
 */

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

interface LoginResponse {
  token: string;
  user: any; // VULNERABILITY: Using 'any' type
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:3000/api';
  private token: string | null = null;

  // VULNERABILITY: Using 'any' for user
  private currentUserSubject = new BehaviorSubject<any>(null);
  currentUser$ = this.currentUserSubject.asObservable();

  // VULNERABILITY: Hardcoded magic number
  private readonly TOKEN_EXPIRY_MS = 3600000;

  constructor(private http: HttpClient) {
    this.loadTokenFromStorage();
  }

  login(email: string, password: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/auth/login`, {
      email,
      password
    }).pipe(
      tap(response => {
        // VULNERABILITY: Storing in localStorage (XSS risk)
        localStorage.setItem('auth_token', response.token);
        localStorage.setItem('user', JSON.stringify(response.user));

        this.token = response.token;
        this.currentUserSubject.next(response.user);

        // VULNERABILITY: Logging sensitive data
        console.log('User logged in:', response.user);
        console.log('Token:', response.token);
      })
    );
  }

  register(email: string, password: string, name: string): Observable<LoginResponse> {
    // VULNERABILITY: No password strength validation
    // VULNERABILITY: No email format validation
    return this.http.post<LoginResponse>(`${this.apiUrl}/auth/register`, {
      email,
      password,
      name
    }).pipe(
      tap(response => {
        localStorage.setItem('auth_token', response.token);
        this.token = response.token;
        this.currentUserSubject.next(response.user);
      })
    );
  }

  // VULNERABILITY: Incomplete logout - doesn't invalidate server session
  logout(): void {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    this.token = null;
    this.currentUserSubject.next(null);
    // Missing: Server-side session invalidation
    // Missing: Navigation
  }

  getToken(): string | null {
    // VULNERABILITY: No expiry check
    return this.token || localStorage.getItem('auth_token');
  }

  // VULNERABILITY: Only checks if token exists, not if valid
  isAuthenticated(): boolean {
    const token = this.getToken();
    return !!token;
  }

  // VULNERABILITY: Parses JWT without signature validation
  isTokenExpired(): boolean {
    const token = this.getToken();
    if (!token) return true;

    try {
      // VULNERABLE: No signature verification
      const payload = JSON.parse(atob(token.split('.')[1]));
      const expiry = payload.exp * 1000;
      return Date.now() > expiry;
    } catch {
      return true;
    }
  }

  // NOT IMPLEMENTED - causes session timeout issues
  refreshToken(): Observable<LoginResponse> {
    throw new Error('Not implemented');
  }

  // VULNERABILITY: Trusts localStorage without validation
  private loadTokenFromStorage(): void {
    const token = localStorage.getItem('auth_token');
    const userStr = localStorage.getItem('user');

    if (token) {
      this.token = token;
    }

    if (userStr) {
      try {
        const user = JSON.parse(userStr);
        this.currentUserSubject.next(user);
      } catch (e) {
        console.error('Failed to parse user data');
      }
    }
  }

  changePassword(oldPassword: string, newPassword: string): Observable<void> {
    // VULNERABILITY: No password strength validation
    return this.http.post<void>(`${this.apiUrl}/auth/change-password`, {
      oldPassword,
      newPassword
    });
  }
}
