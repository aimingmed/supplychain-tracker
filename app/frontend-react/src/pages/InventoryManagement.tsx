import React, { useState, useEffect } from 'react';
import { Search, RotateCcw, Edit, RefreshCw, Plus, Eye, Trash2 } from 'lucide-react';
import { Card, Button, Input, Table, Modal, Select } from '../components/ui';
import type { ProductInventory, InventoryStatusType } from '../types';
import ProductApi from '../services/productApi';

const InventoryManagement: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedProductType, setSelectedProductType] = useState('产品');
  const [loading, setLoading] = useState(false);
  const [inventory, setInventory] = useState<ProductInventory[]>([]);
  const [filteredInventory, setFilteredInventory] = useState<ProductInventory[]>([]);
  
  // Modal states
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isDetailsModalOpen, setIsDetailsModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<ProductInventory | null>(null);
  const [detailsItem, setDetailsItem] = useState<ProductInventory | null>(null);
  const [modalLoading, setModalLoading] = useState(false);

  // Product types - only 产品 has API, others are placeholders for future
  const productTypes = [
    { value: '产品', label: '产品' },
    { value: '母液', label: '母液' },
    { value: '原料', label: '原料' },
    { value: '耗材', label: '耗材' }
  ];

  // Load inventory data on component mount - only for 产品
  useEffect(() => {
    if (selectedProductType === '产品') {
      loadInventory();
    } else {
      // Clear inventory for other types (not yet implemented)
      setInventory([]);
      setFilteredInventory([]);
    }
  }, [selectedProductType]);

  // Filter inventory when search term changes
  useEffect(() => {
    if (selectedProductType === '产品') {
      filterInventory();
    }
  }, [inventory, searchTerm, selectedProductType]);

  const loadInventory = async () => {
    try {
      setLoading(true);
      const data = await ProductApi.getAllProductInventory();
      setInventory(data);
    } catch (error) {
      console.error('Error loading inventory:', error);
      // You might want to show a toast notification here
    } finally {
      setLoading(false);
    }
  };

  const filterInventory = () => {
    let filtered = inventory;

    // Filter by search term (product name or product ID)
    if (searchTerm.trim()) {
      const searchLower = searchTerm.toLowerCase().trim();
      filtered = filtered.filter(item => 
        item.productnameen.toLowerCase().includes(searchLower) ||
        item.productnamezh.toLowerCase().includes(searchLower) ||
        item.productid.toLowerCase().includes(searchLower)
      );
    }

    setFilteredInventory(filtered);
  };

  const columns = [
    { 
      key: 'productid', 
      label: '产品编号', 
      align: 'center' as const,
      sortable: true 
    },
    { 
      key: 'category', 
      label: '产品类型', 
      align: 'center' as const,
      render: (value: string) => {
        // Display simplified category names
        switch (value) {
          case 'Organoid(类器官)': return '类器官';
          case 'Consumable(耗材)': return '耗材';
          case 'Equipment(设备)': return '设备';
          case 'Reagent(试剂)': return '试剂';
          default: return value;
        }
      }
    },
    { 
      key: 'productnamezh', 
      label: '产品名称', 
      align: 'center' as const 
    },
    { 
      key: 'batchid_external', 
      label: '批次号', 
      align: 'center' as const 
    },
    { 
      key: 'specification', 
      label: '规格', 
      align: 'center' as const 
    },
    { 
      key: 'quantityinstock', 
      label: '库存数量', 
      align: 'center' as const,
      sortable: true,
      render: (value: number, item: ProductInventory) => (
        <span className={value <= item.reorderlevel ? 'text-red-600 font-medium' : 'text-gray-900'}>
          {value}
        </span>
      )
    },
    { 
      key: 'status', 
      label: '状态', 
      align: 'center' as const,
      render: (value: string) => {
        const statusColors = {
          'AVAILABLE(可用)': 'text-green-600 bg-green-50',
          'RESERVED(预留)': 'text-yellow-600 bg-yellow-50',
          'IN_USE(使用中)': 'text-blue-600 bg-blue-50',
          'OUT_OF_STOCK(缺货)': 'text-red-600 bg-red-50',
          'EXPIRED(过期)': 'text-gray-600 bg-gray-50',
          'DAMAGED(损坏)': 'text-red-600 bg-red-50',
          'QUARANTINE(隔离)': 'text-orange-600 bg-orange-50'
        };
        const statusLabels = {
          'AVAILABLE(可用)': '可用',
          'RESERVED(预留)': '预留',
          'IN_USE(使用中)': '使用中',
          'OUT_OF_STOCK(缺货)': '缺货',
          'EXPIRED(过期)': '过期',
          'DAMAGED(损坏)': '损坏',
          'QUARANTINE(隔离)': '隔离'
        };
        return (
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusColors[value as keyof typeof statusColors] || 'text-gray-600 bg-gray-50'}`}>
            {statusLabels[value as keyof typeof statusLabels] || value}
          </span>
        );
      }
    },
    { 
      key: 'productiondate', 
      label: '生产日期', 
      align: 'center' as const,
      render: (value: string) => new Date(value).toLocaleDateString('zh-CN')
    },
    { 
      key: 'lastupdated', 
      label: '最新更新', 
      align: 'center' as const,
      render: (value: string) => new Date(value).toLocaleDateString('zh-CN')
    },
  ];

  const handleSearch = () => {
    filterInventory(); // The filtering is already reactive, but we can trigger it manually if needed
  };

  const handleReset = () => {
    setSearchTerm('');
  };

  const handleRefresh = async () => {
    if (selectedProductType === '产品') {
      await loadInventory();
    }
  };

  const handleEditInventory = (item: ProductInventory) => {
    setEditingItem(item);
    setIsEditModalOpen(true);
  };

  const handleCreateInventory = () => {
    setIsCreateModalOpen(true);
  };

  const handleShowInventoryDetails = (item: ProductInventory) => {
    setDetailsItem(item);
    setIsDetailsModalOpen(true);
  };

  const handleDeleteInventory = async (item: ProductInventory) => {
    const confirmed = window.confirm(`确定要删除批次号为 "${item.batchid_external}" 的库存记录吗？此操作不可撤销。`);
    if (!confirmed) return;

    try {
      setLoading(true);
      await ProductApi.deleteProductInventory(item.batchid_internal);
      await loadInventory(); // Refresh the data
    } catch (error) {
      console.error('Error deleting inventory:', error);
      // You might want to show an error toast here
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateQuantity = async (newQuantity: number) => {
    if (!editingItem) return;
    
    try {
      setModalLoading(true);
      const updatedData = {
        ...editingItem,
        quantityinstock: newQuantity
      };
      
      await ProductApi.updateProductInventory(editingItem.batchid_internal, updatedData);
      await loadInventory(); // Refresh the data
      setIsEditModalOpen(false);
      setEditingItem(null);
    } catch (error) {
      console.error('Error updating inventory:', error);
      // You might want to show an error toast here
    } finally {
      setModalLoading(false);
    }
  };

  // Add action column to the table
  const columnsWithActions = [
    ...columns,
    {
      key: 'actions',
      label: '操作',
      align: 'center' as const,
      render: (_: any, item: ProductInventory) => (
        <div className="flex gap-1 justify-center">
          <Button
            size="sm"
            variant="secondary"
            icon={Eye}
            onClick={() => handleShowInventoryDetails(item)}
            title="查看详情"
          >
            详情
          </Button>
          <Button
            size="sm"
            variant="secondary"
            icon={Edit}
            onClick={() => handleEditInventory(item)}
            title="编辑库存"
          >
            编辑
          </Button>
          <Button
            size="sm"
            variant="danger"
            icon={Trash2}
            onClick={() => handleDeleteInventory(item)}
            title="删除库存"
          >
            删除
          </Button>
        </div>
      )
    }
  ];

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
                disabled={type.value !== '产品'} // Only 产品 is available
                title={type.value !== '产品' ? '该功能暂未开放' : ''}
              >
                {type.label}
                {type.value !== '产品' && <span className="ml-1 text-xs opacity-60">(即将推出)</span>}
              </button>
            ))}
          </div>

          {/* Action Buttons - Only show for 产品 */}
          <div className="flex gap-2">
            <Button 
              variant="secondary" 
              icon={RefreshCw} 
              onClick={handleRefresh}
              disabled={selectedProductType !== '产品'}
            >
              刷新
            </Button>
            <Button 
              icon={Plus} 
              onClick={handleCreateInventory}
              disabled={selectedProductType !== '产品'}
            >
              新增库存
            </Button>
          </div>
        </div>
      </Card>

      {/* Data Table */}
      <Card>
        {selectedProductType === '产品' ? (
          <Table
            columns={columnsWithActions}
            data={filteredInventory}
            loading={loading}
          />
        ) : (
          <div className="text-center py-12">
            <div className="text-gray-400 text-lg mb-2">📦</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {selectedProductType} 库存管理
            </h3>
            <p className="text-gray-500">
              该功能正在开发中，敬请期待...
            </p>
          </div>
        )}
      </Card>

      {/* Edit Inventory Modal - Only show for 产品 */}
      {selectedProductType === '产品' && (
        <EditInventoryModal
          isOpen={isEditModalOpen}
          onClose={() => setIsEditModalOpen(false)}
          item={editingItem}
          onUpdate={handleUpdateQuantity}
          loading={modalLoading}
        />
      )}

      {/* Create Inventory Modal - Only show for 产品 */}
      {selectedProductType === '产品' && (
        <CreateInventoryModal
          isOpen={isCreateModalOpen}
          onClose={() => setIsCreateModalOpen(false)}
          onSuccess={() => {
            setIsCreateModalOpen(false);
            loadInventory();
          }}
        />
      )}

      {/* Inventory Details Modal - Only show for 产品 */}
      {selectedProductType === '产品' && (
        <InventoryDetailsModal
          isOpen={isDetailsModalOpen}
          onClose={() => {
            setIsDetailsModalOpen(false);
            setDetailsItem(null);
          }}
          item={detailsItem}
        />
      )}
    </div>
  );
};

// Edit Inventory Modal Component
interface EditInventoryModalProps {
  isOpen: boolean;
  onClose: () => void;
  item: ProductInventory | null;
  onUpdate: (newQuantity: number) => Promise<void>;
  loading: boolean;
}

const EditInventoryModal: React.FC<EditInventoryModalProps> = ({
  isOpen,
  onClose,
  item,
  onUpdate,
  loading
}) => {
  const [quantity, setQuantity] = useState(0);

  useEffect(() => {
    if (item) {
      setQuantity(item.quantityinstock);
    }
  }, [item]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onUpdate(quantity);
  };

  if (!item) return null;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="修改库存数量"
      footer={
        <div className="flex gap-2 justify-end">
          <Button variant="secondary" onClick={onClose}>
            取消
          </Button>
          <Button onClick={handleSubmit} loading={loading}>
            保存
          </Button>
        </div>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            产品名称
          </label>
          <p className="text-gray-900">{item.productnamezh}</p>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            批次号
          </label>
          <p className="text-gray-900">{item.batchid_external}</p>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            当前库存
          </label>
          <p className="text-gray-900">{item.quantityinstock}</p>
        </div>
        <Input
          label="新库存数量"
          type="number"
          value={quantity}
          onChange={(e) => setQuantity(Number(e.target.value))}
          min="0"
          required
        />
      </form>
    </Modal>
  );
};

// Create Inventory Modal Component
interface CreateInventoryModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

const CreateInventoryModal: React.FC<CreateInventoryModalProps> = ({
  isOpen,
  onClose,
  onSuccess
}) => {
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    productid: '',
    basicmediumid: '',
    addictiveid: '',
    quantityinstock: 0,
    productiondate: '',
    imageurl: '',
    status: 'AVAILABLE(可用)' as InventoryStatusType,
    productiondatetime: '',
    producedby: '',
    lastupdatedby: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      // Note: This would need the full ProductInventory data structure
      // For now, this is a simplified version
      await ProductApi.createProductInventory(formData as any);
      onSuccess();
    } catch (error) {
      console.error('Error creating inventory:', error);
    } finally {
      setLoading(false);
    }
  };

  const statusOptions = [
    { value: 'AVAILABLE(可用)', label: '可用' },
    { value: 'RESERVED(预留)', label: '预留' },
    { value: 'IN_USE(使用中)', label: '使用中' },
    { value: 'OUT_OF_STOCK(缺货)', label: '缺货' },
    { value: 'EXPIRED(过期)', label: '过期' },
    { value: 'DAMAGED(损坏)', label: '损坏' },
    { value: 'QUARANTINE(隔离)', label: '隔离' }
  ];

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="新增库存"
      size="lg"
      footer={
        <div className="flex gap-2 justify-end">
          <Button variant="secondary" onClick={onClose}>
            取消
          </Button>
          <Button onClick={handleSubmit} loading={loading}>
            保存
          </Button>
        </div>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <Input
            label="产品ID"
            value={formData.productid}
            onChange={(e) => setFormData({...formData, productid: e.target.value})}
            required
          />
          <Input
            label="基础培养基ID"
            value={formData.basicmediumid}
            onChange={(e) => setFormData({...formData, basicmediumid: e.target.value})}
            required
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <Input
            label="添加剂ID"
            value={formData.addictiveid}
            onChange={(e) => setFormData({...formData, addictiveid: e.target.value})}
            required
          />
          <Input
            label="库存数量"
            type="number"
            value={formData.quantityinstock}
            onChange={(e) => setFormData({...formData, quantityinstock: Number(e.target.value)})}
            min="0"
            required
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <Input
            label="生产日期"
            type="date"
            value={formData.productiondate}
            onChange={(e) => setFormData({...formData, productiondate: e.target.value})}
            required
          />
          <Select
            label="状态"
            value={formData.status}
            onChange={(e) => setFormData({...formData, status: e.target.value as InventoryStatusType})}
            options={statusOptions}
            required
          />
        </div>
        <Input
          label="生产人员"
          value={formData.producedby}
          onChange={(e) => setFormData({...formData, producedby: e.target.value})}
          required
        />
        <Input
          label="图片URL"
          value={formData.imageurl}
          onChange={(e) => setFormData({...formData, imageurl: e.target.value})}
          placeholder="可选"
        />
      </form>
    </Modal>
  );
};

// Inventory Details Modal Component
interface InventoryDetailsModalProps {
  isOpen: boolean;
  onClose: () => void;
  item: ProductInventory | null;
}

const InventoryDetailsModal: React.FC<InventoryDetailsModalProps> = ({
  isOpen,
  onClose,
  item
}) => {
  if (!item) return null;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="库存详情"
      size="xl"
      footer={
        <Button variant="secondary" onClick={onClose}>
          关闭
        </Button>
      }
    >
      <div className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">产品编号</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              {item.productid}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">产品类型</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              {item.category}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">产品名称(中文)</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              {item.productnamezh}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">产品名称(英文)</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              {item.productnameen}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">规格</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              {item.specification || '无'}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">单位</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              {item.unit}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">内部批次号</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              {item.batchid_internal}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">外部批次号</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              {item.batchid_external}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">基础培养基ID</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              {item.basicmediumid}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">添加剂ID</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              {item.addictiveid}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">库存数量</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              <span className={item.quantityinstock <= item.reorderlevel ? 'text-red-600 font-medium' : 'text-gray-900'}>
                {item.quantityinstock}
              </span>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">状态</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              {item.status}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">生产日期</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              {new Date(item.productiondate).toLocaleDateString('zh-CN')}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">生产时间</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              {item.productiondatetime ? new Date(item.productiondatetime).toLocaleString('zh-CN') : '无'}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">生产人员</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              {item.producedby}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">最后更新</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              {new Date(item.lastupdated).toLocaleString('zh-CN')}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">最后更新人员</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              {item.lastupdatedby}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">是否显示</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              {item.to_show ? '是' : '否'}
            </div>
          </div>
        </div>

        {item.imageurl && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">产品图片</label>
            <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
              <a href={item.imageurl} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800">
                查看图片
              </a>
            </div>
          </div>
        )}

        {/* COA (Certificate of Analysis) Information */}
        {(item.coa_appearance || item.coa_clarity !== undefined || item.coa_osmoticpressure || 
          item.coa_ph || item.coa__mycoplasma !== undefined || item.coa_sterility !== undefined || 
          item.coa_fillingvolumedifference !== undefined) && (
          <>
            <div className="pt-4 border-t border-gray-200">
              <h4 className="text-lg font-medium text-gray-900 mb-4">COA 检测信息</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {item.coa_appearance && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">外观</label>
                    <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                      {item.coa_appearance}
                    </div>
                  </div>
                )}
                {item.coa_clarity !== undefined && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">透明度</label>
                    <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                      {item.coa_clarity ? '透明' : '不透明'}
                    </div>
                  </div>
                )}
                {item.coa_osmoticpressure && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">渗透压</label>
                    <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                      {item.coa_osmoticpressure}
                    </div>
                  </div>
                )}
                {item.coa_ph && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">pH值</label>
                    <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                      {item.coa_ph}
                    </div>
                  </div>
                )}
                {item.coa__mycoplasma !== undefined && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">支原体检测</label>
                    <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                      {item.coa__mycoplasma ? '阴性' : '阳性'}
                    </div>
                  </div>
                )}
                {item.coa_sterility !== undefined && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">无菌检测</label>
                    <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                      {item.coa_sterility ? '无菌' : '有菌'}
                    </div>
                  </div>
                )}
                {item.coa_fillingvolumedifference !== undefined && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">装量差异</label>
                    <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                      {item.coa_fillingvolumedifference ? '合格' : '不合格'}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </Modal>
  );
};

export default InventoryManagement;
