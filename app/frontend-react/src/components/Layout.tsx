import React, { useState, useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import Topbar from './Topbar';
import Sidebar from './Sidebar';
import { useAuth } from '../contexts/AuthContext';

const Layout: React.FC = () => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const checkMobile = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);
      if (mobile) {
        setSidebarCollapsed(true);
      }
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleSidebarToggle = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  return (
    <div className="layout-element">
      <Topbar 
        user={user} 
        onLogout={handleLogout} 
        onMenuToggle={handleSidebarToggle}
        showMenuButton={isMobile}
      />
      
      <div className="layout-body">
        <Sidebar 
          collapsed={sidebarCollapsed} 
          onToggle={handleSidebarToggle}
          isMobile={isMobile}
        />
        
        {/* Mobile overlay when sidebar is open */}
        {isMobile && !sidebarCollapsed && (
          <div 
            className="fixed inset-0 z-30 bg-black bg-opacity-50 md:hidden"
            onClick={() => setSidebarCollapsed(true)}
          />
        )}
        
        <main className="layout-main">
          <div className="p-4 sm:p-6">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;
