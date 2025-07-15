import React, { useState } from 'react';
import { Bell, HelpCircle, ChevronDown } from 'lucide-react';
import type { User as UserType } from '../types';

interface TopbarProps {
  user?: UserType;
  onLogout?: () => void;
}

const Topbar: React.FC<TopbarProps> = ({ 
  user = { 
    id: '1', 
    name: '生产管理员', 
    avatar: 'https://tutor-test.aimingmed.com/sampleregister/assets/panda-CUwKr6bp.png',
    role: '生产管理员'
  },
  onLogout 
}) => {
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const [helpMenuOpen, setHelpMenuOpen] = useState(false);
  const [notificationMenuOpen, setNotificationMenuOpen] = useState(false);

  return (
    <header className="topbar-element">
      <h1 className="text-lg font-normal">
        数字类器官模型（Digital Organoid ModelS, DOMS）
      </h1>
      
      <div className="flex items-center gap-2">
        {/* Help Dropdown */}
        <div className="relative">
          <button
            onClick={() => setHelpMenuOpen(!helpMenuOpen)}
            className="flex items-center gap-1 px-3 py-2 rounded hover:bg-primary-600 transition-colors duration-200"
          >
            <HelpCircle size={16} />
            <span className="text-sm">帮助</span>
            <ChevronDown size={14} />
          </button>
          
          {helpMenuOpen && (
            <div className="absolute right-0 top-full mt-1 bg-white text-gray-900 rounded shadow-element border min-w-40 z-50">
              <button className="w-full text-left px-4 py-2 text-sm hover:bg-gray-50 rounded">
                插件下载
              </button>
            </div>
          )}
        </div>

        {/* Notifications Dropdown */}
        <div className="relative">
          <button
            onClick={() => setNotificationMenuOpen(!notificationMenuOpen)}
            className="flex items-center gap-1 px-3 py-2 rounded hover:bg-primary-600 transition-colors duration-200"
          >
            <Bell size={16} />
            <span className="text-sm">通知</span>
            <ChevronDown size={14} />
          </button>
          
          {notificationMenuOpen && (
            <div className="absolute right-0 top-full mt-1 bg-white text-gray-900 rounded shadow-element border min-w-40 z-50">
              <button className="w-full text-left px-4 py-2 text-sm hover:bg-gray-50">
                消息列表
              </button>
              <hr className="my-1 border-gray-200" />
              <button className="w-full text-left px-4 py-2 text-sm hover:bg-gray-50 rounded-b">
                消息盒
              </button>
            </div>
          )}
        </div>

        {/* User Dropdown */}
        <div className="relative">
          <button
            onClick={() => setUserMenuOpen(!userMenuOpen)}
            className="flex items-center gap-2 px-3 py-2 rounded hover:bg-primary-600 transition-colors duration-200"
          >
            <img
              src={user.avatar}
              alt={user.name}
              className="w-8 h-8 rounded-full border-2 border-white/20"
            />
          </button>
          
          {userMenuOpen && (
            <div className="absolute right-0 top-full mt-1 bg-white text-gray-900 rounded shadow-element border min-w-48 z-50">
              <div className="flex flex-col items-center p-4 border-b border-gray-200">
                <img
                  src={user.avatar}
                  alt={user.name}
                  className="w-12 h-12 rounded-full mb-2"
                />
                <span className="text-base font-medium">{user.name}</span>
              </div>
              <button className="w-full text-left px-4 py-2 text-sm hover:bg-gray-50">
                个人资料
              </button>
              <button 
                className="w-full text-left px-4 py-2 text-sm hover:bg-gray-50 rounded-b"
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
