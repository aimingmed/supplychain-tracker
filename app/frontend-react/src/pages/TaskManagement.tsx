import React, { useState } from 'react';
import { Search, RotateCcw, Plus, Edit, Merge, UserPlus, CheckCircle, RefreshCw } from 'lucide-react';
import { Card, Button, Input, Table } from '../components/ui';
import FullCalendarComponent from '../components/FullCalendar';
import type { Task, CalendarEvent } from '../types';

const TaskManagement: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [productStatus, setProductStatus] = useState('');
  const [selectedProductType, setSelectedProductType] = useState('产品');
  const [activeTab, setActiveTab] = useState('task');
  const [loading, setLoading] = useState(false);

  // Sample data
  const [tasks] = useState<Task[]>([
    {
      id: 1,
      productType: '产品',
      productName: 'MasterAim®Primary Enhancer',
      productCode: '100-008',
      status: '待生产',
      assignee: '张三',
      createdAt: '2024-09-03',
      dueDate: '2024-09-10',
    }
  ]);

  const [calendarEvents] = useState<CalendarEvent[]>([
    {
      id: '1',
      title: 'MasterAim®Primary Enhancer 生产任务',
      start: '2024-09-05',
      end: '2024-09-06',
      backgroundColor: '#409eff',
      borderColor: '#409eff'
    }
  ]);

  const productTypes = [
    { value: '产品', label: '产品' },
    { value: '母液', label: '母液' },
    { value: '原料', label: '原料' },
    { value: '耗材', label: '耗材' }
  ];

  const taskColumns = [
    { key: 'id', label: '序号', align: 'center' as const, sortable: true },
    { key: 'productType', label: '产品类型', align: 'center' as const },
    { key: 'productName', label: '产品名称', align: 'center' as const },
    { key: 'productCode', label: '产品编号', align: 'center' as const },
    { 
      key: 'status', 
      label: '生产状态', 
      align: 'center' as const,
      render: (value: string) => {
        const statusColors = {
          '待生产': 'bg-yellow-100 text-yellow-800',
          '生产中': 'bg-blue-100 text-blue-800',
          '已完成': 'bg-green-100 text-green-800',
          '已暂停': 'bg-red-100 text-red-800'
        };
        return (
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusColors[value as keyof typeof statusColors] || 'bg-gray-100 text-gray-800'}`}>
            {value}
          </span>
        );
      }
    },
    { key: 'assignee', label: '负责人', align: 'center' as const },
    { key: 'createdAt', label: '创建时间', align: 'center' as const },
    { key: 'dueDate', label: '预期完成时间', align: 'center' as const },
  ];

  const handleSearch = () => {
    setLoading(true);
    // Implement search logic
    setTimeout(() => setLoading(false), 1000);
  };

  const handleReset = () => {
    setSearchTerm('');
    setProductStatus('');
    setSelectedProductType('产品');
  };

  const handleEventClick = (info: any) => {
    console.log('Event clicked:', info);
  };

  const handleDateClick = (info: any) => {
    console.log('Date clicked:', info);
  };

  return (
    <div className="space-y-6">
      {/* Filter Section */}
      <Card title="数据筛选">
        <div className="space-y-4">
          <div className="flex items-center gap-4">
            <label className="text-gray-600 whitespace-nowrap">生产状态：</label>
            <Input
              placeholder="请选择"
              value={productStatus}
              onChange={(e) => setProductStatus(e.target.value)}
              className="w-64"
            />
            <label className="text-gray-600 whitespace-nowrap">产品名称/编号：</label>
            <Input
              placeholder="产品名称/编号"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-64"
            />
          </div>
          
          <div className="flex justify-end gap-2">
            <Button icon={Search} onClick={handleSearch} loading={loading}>
              查询
            </Button>
            <Button variant="secondary" icon={RotateCcw} onClick={handleReset}>
              重置
            </Button>
          </div>
        </div>
      </Card>

      {/* Tabs and Content */}
      <Card>
        {/* Tab Headers */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('task')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'task'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              任务视图
            </button>
            <button
              onClick={() => setActiveTab('schedule')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'schedule'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              排班视图
            </button>
          </nav>
        </div>

        {/* Tab Content */}
        {activeTab === 'task' && (
          <div className="space-y-6">
            {/* Product Type Tabs and Actions */}
            <div className="flex justify-between items-center">
              {/* Product Type Toggle */}
              <div className="flex border rounded-md">
                {productTypes.map((type) => (
                  <button
                    key={type.value}
                    onClick={() => setSelectedProductType(type.value)}
                    className={`px-4 py-2 text-sm font-medium transition-colors ${
                      selectedProductType === type.value
                        ? 'bg-primary-500 text-white'
                        : 'text-gray-700 hover:bg-gray-50'
                    } ${type.value === productTypes[0].value ? 'rounded-l-md' : ''} ${
                      type.value === productTypes[productTypes.length - 1].value ? 'rounded-r-md' : ''
                    }`}
                  >
                    {type.label}
                  </button>
                ))}
              </div>

              {/* Action Buttons */}
              <div className="flex gap-2">
                <Button icon={Plus}>
                  添加任务
                </Button>
                <Button variant="secondary" icon={Edit}>
                  修改任务
                </Button>
                <Button variant="success" icon={Merge}>
                  合并任务
                </Button>
                <Button variant="danger" icon={UserPlus}>
                  分配任务
                </Button>
                <Button variant="secondary" icon={CheckCircle}>
                  入库审核
                </Button>
                <Button variant="secondary" icon={RefreshCw}>
                  刷新
                </Button>
              </div>
            </div>

            {/* Tasks Table */}
            <Table
              columns={taskColumns}
              data={tasks.filter(task => task.productType === selectedProductType)}
              loading={loading}
            />
          </div>
        )}

        {activeTab === 'schedule' && (
          <div className="space-y-4">
            <FullCalendarComponent
              events={calendarEvents}
              onEventClick={handleEventClick}
              onDateClick={handleDateClick}
              height={600}
            />
          </div>
        )}
      </Card>
    </div>
  );
};

export default TaskManagement;
