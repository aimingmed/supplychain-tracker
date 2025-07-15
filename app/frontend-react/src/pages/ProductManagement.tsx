import React, { useState } from 'react';
import { Search, RotateCcw, Plus, Edit, Trash2, History, RefreshCw } from 'lucide-react';
import { Card, Button, Input, Select, Table, Modal } from '../components/ui';
import type { Product } from '../types';

const ProductManagement: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProductType, setSelectedProductType] = useState('产品');
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  // Sample data
  const [products] = useState<Product[]>([
    {
      id: 1,
      type: '产品',
      name: 'MasterAim®Primary Enhancer',
      code: '100-008',
      spec: '500μL',
      created: '2024-09-03',
      updated: '',
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
    { key: 'created', label: '添加时间', align: 'center' as const },
    { key: 'updated', label: '修改时间', align: 'center' as const },
    {
      key: 'actions',
      label: '操作',
      align: 'center' as const,
      render: () => (
        <Button variant="secondary" size="sm">
          详情
        </Button>
      )
    }
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
            <Button icon={Plus} onClick={() => setIsAddModalOpen(true)}>
              添加产品
            </Button>
            <Button variant="secondary" icon={Edit}>
              修改产品
            </Button>
            <Button variant="danger" icon={Trash2}>
              删除产品
            </Button>
            <Button variant="secondary" icon={History}>
              历史产品
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
          data={products.filter(p => p.type === selectedProductType)}
          loading={loading}
        />
      </Card>

      {/* Add Product Modal */}
      <Modal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        title="添加产品"
        size="xl"
        footer={
          <>
            <Button variant="secondary" onClick={() => setIsAddModalOpen(false)}>
              取消
            </Button>
            <Button>
              确定
            </Button>
          </>
        }
      >
        <div className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <Select
              label="产品类型"
              options={productTypes}
              defaultValue="产品"
            />
            <Input
              label="产品名称"
              placeholder="请输入产品名称"
            />
            <Input
              label="产品编号"
              placeholder="请输入产品编号"
            />
            <Select
              label="产品单位"
              options={[
                { value: 'μL', label: 'μL' },
                { value: 'mL', label: 'mL' },
                { value: 'L', label: 'L' }
              ]}
            />
          </div>

          <div>
            <h4 className="text-lg font-medium text-gray-700 mb-4">规格</h4>
            <Table
              columns={[
                { key: 'required', label: '需要', align: 'center' },
                { key: 'name', label: '名称', align: 'center' },
                { key: 'concentration', label: '浓度', align: 'center' },
                { key: 'concentrationUnit', label: '浓度单位', align: 'center' },
                { key: 'usage', label: '用量', align: 'center' },
                { key: 'usageUnit', label: '用量单位', align: 'center' },
                { key: 'actions', label: '操作', align: 'center' }
              ]}
              data={[
                {
                  required: 1,
                  name: 'MasterAim®Primary Enhancer',
                  concentration: 500,
                  concentrationUnit: 'μL',
                  usage: 100,
                  usageUnit: 'μL',
                  actions: '+'
                }
              ]}
            />
          </div>

          <div>
            <h4 className="text-lg font-medium text-gray-700 mb-2">组分</h4>
            {/* Add component form here */}
          </div>

          <div>
            <h4 className="text-lg font-medium text-gray-700 mb-2">添加物</h4>
            {/* Add additives form here */}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">备注</label>
            <textarea
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              rows={4}
              placeholder="备注信息"
            />
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default ProductManagement;
