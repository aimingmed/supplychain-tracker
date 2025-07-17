import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bell, HelpCircle, ChevronDown, Menu } from 'lucide-react';
import type { UserResponse } from '../services/authApi';

interface TopbarProps {
  user?: UserResponse | null;
  onLogout?: () => void;
  onMenuToggle?: () => void;
  showMenuButton?: boolean;
}

const Topbar: React.FC<TopbarProps> = ({ 
  user = null,
  onLogout,
  onMenuToggle,
  showMenuButton = false
}) => {
  const navigate = useNavigate();
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const [helpMenuOpen, setHelpMenuOpen] = useState(false);
  const [notificationMenuOpen, setNotificationMenuOpen] = useState(false);

  // Default user data when no user is provided
  const defaultUser = {
    username: '生产管理员',
    email: 'admin@example.com',
    list_of_roles: ['生产管理员'],
    is_verified: true
  };

  const currentUser = user || defaultUser;
  const avatar = 'https://tutor-test.aimingmed.com/sampleregister/assets/panda-CUwKr6bp.png';

  const handleProfileClick = () => {
    setUserMenuOpen(false);
    navigate('/profile');
  };

  return (
    <header className="topbar-element">
      <div className="flex items-center gap-2 sm:gap-3 min-w-0 flex-1">
        {/* Mobile Menu Button */}
        {showMenuButton && (
          <button
            onClick={onMenuToggle}
            className="flex items-center justify-center w-8 h-8 rounded hover:bg-primary-600 transition-colors duration-200 md:hidden flex-shrink-0"
          >
            <Menu size={18} />
          </button>
        )}
        
        <h1 className="text-sm sm:text-lg font-normal truncate min-w-0">
          <span className="hidden sm:inline">艾名供应链追踪系统（AimingMed Supply-Chain Tracking System）</span>
          <span className="sm:hidden">供应链追踪系统</span>
        </h1>
      </div>
      
      <div className="flex items-center gap-1 sm:gap-2 flex-shrink-0">
        {/* Help Dropdown */}
        <div className="relative">
          <button
            onClick={() => setHelpMenuOpen(!helpMenuOpen)}
            className="flex items-center gap-1 px-2 sm:px-3 py-2 rounded hover:bg-primary-600 transition-colors duration-200"
          >
            <HelpCircle size={14} className="sm:w-4 sm:h-4" />
            <span className="text-xs sm:text-sm hidden sm:inline">帮助</span>
            <ChevronDown size={12} className="sm:w-3.5 sm:h-3.5" />
          </button>
          
          {helpMenuOpen && (
            <div className="absolute right-0 top-full mt-1 bg-white text-gray-900 rounded shadow-element border min-w-32 sm:min-w-40 z-50">
              <button className="w-full text-left px-3 sm:px-4 py-2 text-xs sm:text-sm hover:bg-gray-50 rounded">
                插件下载
              </button>
            </div>
          )}
        </div>

        {/* Notifications Dropdown */}
        <div className="relative">
          <button
            onClick={() => setNotificationMenuOpen(!notificationMenuOpen)}
            className="flex items-center gap-1 px-2 sm:px-3 py-2 rounded hover:bg-primary-600 transition-colors duration-200"
          >
            <Bell size={14} className="sm:w-4 sm:h-4" />
            <span className="text-xs sm:text-sm hidden sm:inline">通知</span>
            <ChevronDown size={12} className="sm:w-3.5 sm:h-3.5" />
          </button>
          
          {notificationMenuOpen && (
            <div className="absolute right-0 top-full mt-1 bg-white text-gray-900 rounded shadow-element border min-w-32 sm:min-w-40 z-50">
              <button className="w-full text-left px-3 sm:px-4 py-2 text-xs sm:text-sm hover:bg-gray-50">
                消息列表
              </button>
              <hr className="my-1 border-gray-200" />
              <button className="w-full text-left px-3 sm:px-4 py-2 text-xs sm:text-sm hover:bg-gray-50 rounded-b">
                消息盒
              </button>
            </div>
          )}
        </div>

        {/* User Dropdown */}
        <div className="relative">
          <button
            onClick={() => setUserMenuOpen(!userMenuOpen)}
            className="flex items-center gap-1 sm:gap-2 px-2 sm:px-3 py-2 rounded hover:bg-primary-600 transition-colors duration-200"
          >
            <img
              src={avatar}
              alt={currentUser.username}
              className="w-6 h-6 sm:w-8 sm:h-8 rounded-full border-2 border-white/20"
            />
          </button>
          
          {userMenuOpen && (
            <div className="absolute right-0 top-full mt-1 bg-white text-gray-900 rounded shadow-element border min-w-44 sm:min-w-48 z-50">
              <div className="flex flex-col items-center p-3 sm:p-4 border-b border-gray-200">
                <img
                  src={avatar}
                  alt={currentUser.username}
                  className="w-10 h-10 sm:w-12 sm:h-12 rounded-full mb-2"
                />
                <span className="text-sm sm:text-base font-medium">{currentUser.username}</span>
                <span className="text-xs sm:text-sm text-gray-600">{currentUser.email}</span>
              </div>
              <button 
                className="w-full text-left px-3 sm:px-4 py-2 text-xs sm:text-sm hover:bg-gray-50"
                onClick={handleProfileClick}
              >
                个人资料
              </button>
              <button 
                className="w-full text-left px-3 sm:px-4 py-2 text-xs sm:text-sm hover:bg-gray-50 rounded-b"
                onClick={onLogout}
              >
                注销
              </button>
            </div>
          )}
        </div>
      </div>
      
      {/* Click outside to close dropdowns */}
      {(userMenuOpen || helpMenuOpen || notificationMenuOpen) && (
        <div 
          className="fixed inset-0 z-40"
          onClick={() => {
            setUserMenuOpen(false);
            setHelpMenuOpen(false);
            setNotificationMenuOpen(false);
          }}
        />
      )}
    </header>
  );
};

export default Topbar;
