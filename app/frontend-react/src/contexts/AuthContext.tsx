import React, { createContext, useContext, useState, useEffect } from 'react';
import AuthApi, { type UserResponse } from '../services/authApi';

interface AuthContextType {
  user: UserResponse | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<UserResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = !!user && AuthApi.isAuthenticated();

  // Check if user is logged in on app start
  useEffect(() => {
    const checkAuth = async () => {
      const token = AuthApi.getToken();
      if (token) {
        try {
          const userData = await AuthApi.getCurrentUser(token);
          setUser(userData);
        } catch (error) {
          // Invalid token, remove it
          AuthApi.removeToken();
          setUser(null);
        }
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (username: string, password: string): Promise<void> => {
    const response = await AuthApi.login({ username, password });
    AuthApi.setToken(response.token);
    
    // Get user data
    const userData = await AuthApi.getCurrentUser(response.token);
    setUser(userData);
  };

  const logout = (): void => {
    AuthApi.removeToken();
    setUser(null);
  };

  const refreshUser = async (): Promise<void> => {
    const token = AuthApi.getToken();
    if (token) {
      try {
        const userData = await AuthApi.getCurrentUser(token);
        setUser(userData);
      } catch (error) {
        logout();
      }
    }
  };

  const value: AuthContextType = {
    user,
    isAuthenticated,
    isLoading,
    login,
    logout,
    refreshUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
