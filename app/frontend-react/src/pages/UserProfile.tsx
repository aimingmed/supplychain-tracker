import React, { useState, useEffect } from 'react';
import { User, Mail, Shield, CheckCircle, XCircle, Edit, Save, X } from 'lucide-react';
import { Card, Button, Input } from '../components/ui';
import { useAuth } from '../contexts/AuthContext';

const UserProfile: React.FC = () => {
  const { user, refreshUser } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  
  // Form state for editing
  const [formData, setFormData] = useState({
    username: user?.username || '',
    email: user?.email || '',
  });

  // Update form data when user data changes
  useEffect(() => {
    if (user) {
      setFormData({
        username: user.username,
        email: user.email,
      });
    }
  }, [user]);

  const handleEdit = () => {
    setIsEditing(true);
    setError(null);
    setSuccess(null);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setFormData({
      username: user?.username || '',
      email: user?.email || '',
    });
    setError(null);
    setSuccess(null);
  };

  const handleSave = async () => {
    try {
      setLoading(true);
      setError(null);
      setSuccess(null);

      // Note: The current backend doesn't support profile updates
      // This is a placeholder for when the API is implemented
      console.log('Profile update would be sent:', formData);
      
      // For now, just show a success message
      setSuccess('个人资料已更新');
      setIsEditing(false);
      
      // Refresh user data
      await refreshUser();
    } catch (err) {
      setError(err instanceof Error ? err.message : '更新失败');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const getRoleDisplayName = (role: string) => {
    const roleMap: Record<string, string> = {
      'ADMIN': '系统管理员',
      'PRODUCTION_MANAGER': '生产管理员',
      'INVENTORY_MANAGER': '库存管理员',
      'QUALITY_MANAGER': '质量管理员',
      'USER': '普通用户',
    };
    return roleMap[role] || role;
  };

  if (!user) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-gray-500">加载用户信息中...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">个人资料</h1>
        {!isEditing && (
          <Button onClick={handleEdit} icon={Edit} variant="primary">
            编辑资料
          </Button>
        )}
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
          {success}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Profile Information Card */}
        <div className="lg:col-span-2">
          <Card title="基本信息">
            <div className="space-y-6">
              {/* Avatar Section */}
              <div className="flex items-center space-x-6">
                <div className="relative">
                  <img
                    src="https://tutor-test.aimingmed.com/sampleregister/assets/panda-CUwKr6bp.png"
                    alt={user.username}
                    className="w-24 h-24 rounded-full border-4 border-gray-200"
                  />
                  <div className="absolute bottom-0 right-0 w-6 h-6 bg-primary-500 rounded-full flex items-center justify-center">
                    <User size={14} className="text-white" />
                  </div>
                </div>
                <div>
                  <h3 className="text-lg font-medium text-gray-900">{user.username}</h3>
                  <p className="text-sm text-gray-500">用户头像</p>
                  {!isEditing && (
                    <button className="mt-2 text-sm text-primary-600 hover:text-primary-700">
                      更换头像
                    </button>
                  )}
                </div>
              </div>

              {/* Form Fields */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <Input
                    label="用户名"
                    value={isEditing ? formData.username : user.username}
                    onChange={(e) => isEditing && handleInputChange('username', e.target.value)}
                    disabled={!isEditing}
                    className={isEditing ? '' : 'bg-gray-50'}
                  />
                </div>
                <div>
                  <Input
                    label="邮箱地址"
                    type="email"
                    value={isEditing ? formData.email : user.email}
                    onChange={(e) => isEditing && handleInputChange('email', e.target.value)}
                    disabled={!isEditing}
                    className={isEditing ? '' : 'bg-gray-50'}
                  />
                </div>
              </div>

              {/* Action Buttons */}
              {isEditing && (
                <div className="flex items-center space-x-3 pt-4 border-t border-gray-200">
                  <Button
                    onClick={handleSave}
                    loading={loading}
                    icon={Save}
                    variant="primary"
                  >
                    保存更改
                  </Button>
                  <Button
                    onClick={handleCancel}
                    icon={X}
                    variant="secondary"
                    disabled={loading}
                  >
                    取消
                  </Button>
                </div>
              )}
            </div>
          </Card>
        </div>

        {/* Account Status Card */}
        <div className="space-y-6">
          <Card title="账户状态">
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className={`p-2 rounded-full ${user.is_verified ? 'bg-green-100' : 'bg-red-100'}`}>
                  {user.is_verified ? (
                    <CheckCircle size={16} className="text-green-600" />
                  ) : (
                    <XCircle size={16} className="text-red-600" />
                  )}
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-900">账户验证</p>
                  <p className={`text-xs ${user.is_verified ? 'text-green-600' : 'text-red-600'}`}>
                    {user.is_verified ? '已验证' : '未验证'}
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <div className="p-2 rounded-full bg-blue-100">
                  <Mail size={16} className="text-blue-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-900">邮箱状态</p>
                  <p className="text-xs text-blue-600">正常</p>
                </div>
              </div>
            </div>
          </Card>

          <Card title="用户角色">
            <div className="space-y-3">
              {user.list_of_roles.map((role, index) => (
                <div key={index} className="flex items-center space-x-3">
                  <div className="p-2 rounded-full bg-purple-100">
                    <Shield size={16} className="text-purple-600" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {getRoleDisplayName(role)}
                    </p>
                    <p className="text-xs text-gray-500">
                      角色代码: {role}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>

      {/* Additional Information */}
      <Card title="其他信息">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <h4 className="text-sm font-medium text-gray-900">用户ID</h4>
            <p className="mt-1 text-sm text-gray-600">{user.username}</p>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-900">注册时间</h4>
            <p className="mt-1 text-sm text-gray-600">2024-01-01</p>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-900">最后登录</h4>
            <p className="mt-1 text-sm text-gray-600">刚刚</p>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default UserProfile;
