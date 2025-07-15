import React, { useState } from 'react';
import { Search, RotateCcw, Edit, RefreshCw } from 'lucide-react';
import { Card, Button, Input, Table } from '../components/ui';
import type { InventoryItem } from '../types';

const InventoryManagement: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProductType, setSelectedProductType] = useState('产品');
  const [loading, setLoading] = useState(false);

  // Sample data
  const [inventory] = useState<InventoryItem[]>([
    {
      id: 1,
      type: '产品',
      name: 'MasterAim®Primary Enhancer',
      code: '100-008',
      spec: '500μL',
      quantity: 50,
      latestInTime: '2024-09-03',
      latestOutTime: '2024-09-05',
    }
  ]);

  const productTypes = [
    { value: '产品', label: '产品' },
    { value: '母液', label: '母液' },
    { value: '原料', label: '原料' },
    { value: '耗材', label: '耗材' }
  ];

  const columns = [
    { key: 'id', label: '序号', align: 'center' as const, sortable: true },
    { key: 'type', label: '产品类型', align: 'center' as const },
    { key: 'name', label: '产品名称', align: 'center' as const },
    { key: 'code', label: '产品编号', align: 'center' as const },
    { key: 'spec', label: '规格', align: 'center' as const },
    { 
      key: 'quantity', 
      label: '数量', 
      align: 'center' as const,
      render: (value: number) => (
        <span className={value <= 10 ? 'text-red-600 font-medium' : 'text-gray-900'}>
          {value}
        </span>
      )
    },
    { key: 'latestInTime', label: '最新入库时间', align: 'center' as const },
    { key: 'latestOutTime', label: '最新出库时间', align: 'center' as const },
  ];

  const handleSearch = () => {
    setLoading(true);
    // Implement search logic
    setTimeout(() => setLoading(false), 1000);
  };

  const handleReset = () => {
    setSearchTerm('');
    setSelectedProductType('产品');
  };

  return (
    <div className="space-y-6">
      {/* Filter Section */}
      <Card title="数据筛选">
        <div className="space-y-4">
          <div className="flex items-center gap-4">
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

      {/* Product Type Tabs and Actions */}
      <Card>
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
            <Button variant="secondary" icon={Edit}>
              修改库存
            </Button>
            <Button variant="secondary" icon={RefreshCw}>
              刷新
            </Button>
          </div>
        </div>
      </Card>

      {/* Data Table */}
      <Card>
        <Table
          columns={columns}
          data={inventory.filter(item => item.type === selectedProductType)}
          loading={loading}
        />
      </Card>
    </div>
  );
};

export default InventoryManagement;
