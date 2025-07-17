// In Vite, environment variables are accessed via import.meta.env and must be prefixed with VITE_
const API_BASE_URL = import.meta.env.VITE_REACT_APP_BASE_URL || 'https://staging-sctracker.aimingmed.local/api';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface LoginResponse {
  token: string;
}

export interface UserResponse {
  username: string;
  email: string;
  list_of_roles: string[];
  is_verified: boolean;
}

class AuthApi {
  static async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await fetch(`${API_BASE_URL}/accounts/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Login failed' }));
      throw new Error(errorData.detail || 'Login failed');
    }
    
    return response.json();
  }

  static async getCurrentUser(token: string): Promise<UserResponse> {
    const response = await fetch(`${API_BASE_URL}/accounts/me`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Failed to get user info' }));
      throw new Error(errorData.detail || 'Failed to get user info');
    }
    
    return response.json();
  }

  static async resetPassword(token: string, newPassword: string): Promise<{ message: string }> {
    const response = await fetch(`${API_BASE_URL}/accounts/reset-password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token, new_password: newPassword }),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Password reset failed' }));
      throw new Error(errorData.detail || 'Password reset failed');
    }
    
    return response.json();
  }

  // Token management
  static setToken(token: string): void {
    localStorage.setItem('authToken', token);
  }

  static getToken(): string | null {
    return localStorage.getItem('authToken');
  }

  static removeToken(): void {
    localStorage.removeItem('authToken');
  }

  static isAuthenticated(): boolean {
    return !!this.getToken();
  }

  // Utility method for making authenticated requests
  static async makeAuthenticatedRequest(url: string, options: RequestInit = {}): Promise<Response> {
    const token = this.getToken();
    
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    };

    return fetch(url, {
      ...options,
      headers,
    });
  }
}

export default AuthApi;
