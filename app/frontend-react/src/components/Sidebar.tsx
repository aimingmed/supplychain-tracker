import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { 
  Factory, 
  Package, 
  Warehouse, 
  ListTodo, 
  Calendar, 
  Wrench, 
  Trash2,
  ChevronDown,
  ChevronRight,
  Menu
} from 'lucide-react';
import type { MenuItem } from '../types';

interface SidebarProps {
  collapsed?: boolean;
  onToggle?: () => void;
  isMobile?: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ collapsed = false, onToggle, isMobile = false }) => {
  const [expandedMenus, setExpandedMenus] = useState<string[]>(['production']);

  const menuItems: MenuItem[] = [
    {
      key: 'production',
      label: '生产管理',
      icon: 'Factory',
      children: [
        { key: 'product-management', label: '产品管理', path: '/product-management', icon: 'Package' },
        { key: 'inventory-management', label: '库存管理', path: '/inventory-management', icon: 'Warehouse' },
        { key: 'demand-management', label: '需求管理', path: '/demand-management', icon: 'ListTodo' },
        { key: 'task-management', label: '任务管理', path: '/task-management', icon: 'Calendar' },
        { key: 'material-management', label: '物料管理', path: '/material-management', icon: 'Wrench' },
        { key: 'scrap-management', label: '余料管理', path: '/scrap-management', icon: 'Trash2' },
      ]
    }
  ];

  const getIcon = (iconName: string, size = 18) => {
    const icons = {
      Factory: <Factory size={size} />,
      Package: <Package size={size} />,
      Warehouse: <Warehouse size={size} />,
      ListTodo: <ListTodo size={size} />,
      Calendar: <Calendar size={size} />,
      Wrench: <Wrench size={size} />,
      Trash2: <Trash2 size={size} />,
    };
    return icons[iconName as keyof typeof icons] || null;
  };

  const toggleMenu = (key: string) => {
    setExpandedMenus(prev => 
      prev.includes(key) 
        ? prev.filter(item => item !== key)
        : [...prev, key]
    );
  };

  return (
    <aside className={`sidebar-element transition-all duration-300 ${
      collapsed ? 'w-16' : 'w-64'
    } ${
      isMobile ? 'fixed left-0 top-0 h-full z-40 transform' + (collapsed ? ' -translate-x-full' : ' translate-x-0') : ''
    }`}>
      {/* Logo Section */}
      <div className="flex items-center p-4 border-b border-gray-200">
        {!collapsed && (
          <img 
            src="https://tutor.aimingmed.com/file/assets/logo.png" 
            alt="Logo" 
            className="w-20 h-auto"
          />
        )}
        <button
          onClick={onToggle}
          className="ml-auto p-2 hover:bg-gray-100 rounded transition-colors duration-200"
        >
          <Menu size={18} />
        </button>
      </div>

      {/* Menu Section */}
      <div className="flex-1 overflow-y-auto">
        <nav className="sidebar-menu">
          {menuItems.map((item) => (
            <div key={item.key} className="sidebar-menu-group">
              {/* Parent Menu Item */}
              <button
                onClick={() => toggleMenu(item.key)}
                className="sidebar-menu-title"
              >
                {item.icon && getIcon(item.icon)}
                {!collapsed && (
                  <>
                    <span className="flex-1 text-left">{item.label}</span>
                    {expandedMenus.includes(item.key) ? (
                      <ChevronDown size={16} />
                    ) : (
                      <ChevronRight size={16} />
                    )}
                  </>
                )}
              </button>

              {/* Children Menu Items */}
              {!collapsed && expandedMenus.includes(item.key) && item.children && (
                <div className="sidebar-submenu">
                  {item.children.map((child) => (
                    <NavLink
                      key={child.key}
                      to={child.path || '#'}
                      className={({ isActive }) =>
                        `sidebar-menu-item sidebar-submenu-item ${isActive ? 'active' : ''}`
                      }
                    >
                      {child.icon && getIcon(child.icon, 16)}
                      <span className="ml-2">{child.label}</span>
                    </NavLink>
                  ))}
                </div>
              )}
            </div>
          ))}
        </nav>
      </div>
    </aside>
  );
};

export default Sidebar;
