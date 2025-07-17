import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Eye, EyeOff, LogIn } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

interface LoginCredentials {
  username: string;
  password: string;
}

interface LocationState {
  from?: {
    pathname: string;
  };
}

const Login: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isAuthenticated, isLoading } = useAuth();
  
  // All hooks must be called at the top level before any early returns
  const [credentials, setCredentials] = useState<LoginCredentials>({
    username: '',
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  
  const state = location.state as LocationState;
  const from = state?.from?.pathname || '/product-management';

  // Redirect if already authenticated
  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, isLoading, navigate, from]);

  // Show loading while checking authentication
  if (isLoading) {
    return (
      <div className="login-container">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">加载中...</p>
        </div>
      </div>
    );
  }

  // Don't render login form if already authenticated
  if (isAuthenticated) {
    return null;
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCredentials(prev => ({
      ...prev,
      [name]: value,
    }));
    // Clear error when user starts typing
    if (error) setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!credentials.username || !credentials.password) {
      setError('请输入用户名和密码');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await login(credentials.username, credentials.password);
      
      // Redirect to the page they tried to visit or dashboard
      navigate(from, { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : '登录失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <div className="login-container">
      <div className="login-card">
        {/* Logo and Title */}
        <div className="text-center">
          <img
            className="login-logo"
            src="https://tutor-test.aimingmed.com/sampleregister/assets/panda-CUwKr6bp.png"
            alt="DOMS Logo"
          />
          <h2 className="login-title">
            数字类器官模型系统
          </h2>
          <p className="login-subtitle">
            Digital Organoid ModelS (DOMS)
          </p>
        </div>

        {/* Login Form */}
        <form className="login-form" onSubmit={handleSubmit}>
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <div className="login-input-group">
            <label htmlFor="username" className="login-input-label">
              用户名
            </label>
            <input
              id="username"
              name="username"
              type="text"
              required
              className="input-element"
              placeholder="请输入用户名"
              value={credentials.username}
              onChange={handleInputChange}
              disabled={loading}
            />
          </div>

          <div className="login-input-group">
            <label htmlFor="password" className="login-input-label">
              密码
            </label>
            <div className="password-input-container">
              <input
                id="password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                required
                className="input-element pr-12"
                placeholder="请输入密码"
                value={credentials.password}
                onChange={handleInputChange}
                disabled={loading}
              />
              <button
                type="button"
                className="password-toggle-btn"
                onClick={togglePasswordVisibility}
                disabled={loading}
              >
                {showPassword ? (
                  <EyeOff className="h-5 w-5" />
                ) : (
                  <Eye className="h-5 w-5" />
                )}
              </button>
            </div>
          </div>

          <div className="login-options">
            <div className="remember-me">
              <input
                id="remember-me"
                name="remember-me"
                type="checkbox"
                className="remember-me-checkbox"
              />
              <label htmlFor="remember-me" className="remember-me-label">
                记住我
              </label>
            </div>

            <div className="text-sm">
              <a
                href="#"
                className="forgot-password-link"
                onClick={(e) => e.preventDefault()}
              >
                忘记密码？
              </a>
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="login-submit-btn"
            >
              {loading ? (
                <>
                  <div className="loading-spinner"></div>
                  登录中...
                </>
              ) : (
                <>
                  <LogIn className="h-4 w-4" />
                  登录
                </>
              )}
            </button>
          </div>
        </form>

        {/* Footer */}
        <div className="login-footer">
          <p className="login-footer-text">
            © 2025 AimingMed. 版权所有
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
