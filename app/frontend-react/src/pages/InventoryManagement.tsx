import React, { useState, useEffect } from 'react';
import { Search, RotateCcw, Edit, RefreshCw, Plus, Eye, Trash2 } from 'lucide-react';
import { Card, Button, Input, Table, Modal, Select, Autocomplete } from '../components/ui';
import type { ProductInventory, InventoryStatusType, ProductInventoryCreateRequest, ProductDetails } from '../types';
import type { UserResponse } from '../services/authApi';
import ProductApi from '../services/productApi';
import AuthApi from '../services/authApi';

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
      align: 'center' as const,
      render: (value: string, item: ProductInventory) => {
        const internalBatchId = item.batchid_internal;
        const tooltipText = internalBatchId ? `内部批次号: ${internalBatchId}` : '内部批次号: 暂无数据';
        
        return (
          <div className="relative group">
            <span 
              className="cursor-help underline decoration-dotted hover:bg-blue-50 px-1 py-0.5 rounded transition-colors"
            >
              {value}
            </span>
            {/* Custom tooltip with clean dark styling */}
            <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-900 text-white text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-20 shadow-lg">
              {tooltipText}
            </div>
          </div>
        );
      }
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
        <div className="flex flex-col sm:flex-row gap-1 sm:gap-2 justify-center">
          <Button
            size="sm"
            variant="secondary"
            icon={Eye}
            onClick={() => handleShowInventoryDetails(item)}
            title="查看详情"
            className="w-full sm:w-auto"
          >
            <span className="sm:hidden">详情</span>
            <span className="hidden sm:inline">详情</span>
          </Button>
          <Button
            size="sm"
            variant="secondary"
            icon={Edit}
            onClick={() => handleEditInventory(item)}
            title="编辑库存"
            className="w-full sm:w-auto"
          >
            <span className="sm:hidden">编辑</span>
            <span className="hidden sm:inline">编辑</span>
          </Button>
          <Button
            size="sm"
            variant="danger"
            icon={Trash2}
            onClick={() => handleDeleteInventory(item)}
            title="删除库存"
            className="w-full sm:w-auto"
          >
            <span className="sm:hidden">删除</span>
            <span className="hidden sm:inline">删除</span>
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
          <div className="flex flex-col sm:flex-row sm:items-center gap-4">
            <label className="text-gray-600 whitespace-nowrap">产品名称/编号：</label>
            <Input
              placeholder="产品名称/编号"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full sm:w-64"
            />
          </div>
          
          <div className="flex flex-col sm:flex-row justify-end gap-2">
            <Button icon={Search} onClick={handleSearch} loading={loading} className="w-full sm:w-auto">
              查询
            </Button>
            <Button variant="secondary" icon={RotateCcw} onClick={handleReset} className="w-full sm:w-auto">
              重置
            </Button>
          </div>
        </div>
      </Card>

      {/* Product Type Tabs and Actions */}
      <Card>
        <div className="flex flex-col lg:flex-row lg:justify-between lg:items-center gap-4">
          {/* Product Type Toggle */}
          <div className="flex overflow-x-auto border rounded-md">
            {productTypes.map((type) => (
              <button
                key={type.value}
                onClick={() => setSelectedProductType(type.value)}
                className={`px-3 sm:px-4 py-2 text-sm font-medium transition-colors whitespace-nowrap ${
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
          <div className="flex flex-wrap gap-2">
            <Button 
              variant="secondary" 
              icon={RefreshCw} 
              onClick={handleRefresh}
              disabled={selectedProductType !== '产品'}
              className="flex-1 sm:flex-none"
            >
              <span className="hidden sm:inline">刷新</span>
            </Button>
            <Button 
              icon={Plus} 
              onClick={handleCreateInventory}
              disabled={selectedProductType !== '产品'}
              className="flex-1 sm:flex-none"
            >
              <span className="hidden sm:inline">新增库存</span>
            </Button>
          </div>
        </div>
      </Card>

      {/* Data Table */}
      <Card>
        {selectedProductType === '产品' ? (
          <div className="-m-6">
            <Table
              columns={columnsWithActions}
              data={filteredInventory}
              loading={loading}
            />
          </div>
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
  const [productDetailsLoading, setProductDetailsLoading] = useState(false);
  const [producersLoading, setProducersLoading] = useState(false);
  const [productDetails, setProductDetails] = useState<ProductDetails[]>([]);
  const [producers, setProducers] = useState<UserResponse[]>([]);
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
    lastupdatedby: '',
    to_show: true,
    // COA fields (optional)
    coa_appearance: '',
    coa_clarity: undefined as boolean | undefined,
    coa_osmoticpressure: undefined as number | undefined,
    coa_ph: undefined as number | undefined,
    coa__mycoplasma: undefined as boolean | undefined,
    coa_sterility: undefined as boolean | undefined,
    coa_fillingvolumedifference: undefined as boolean | undefined
  });

  // Load product details for autocomplete
  const loadProductDetails = async () => {
    try {
      setProductDetailsLoading(true);
      const data = await ProductApi.getAllProductDetails();
      setProductDetails(data);
    } catch (error) {
      console.error('Error loading product details:', error);
    } finally {
      setProductDetailsLoading(false);
    }
  };

  // Load producers for autocomplete
  const loadProducers = async () => {
    try {
      setProducersLoading(true);
      const data = await AuthApi.getUsersByRole('PRODUCER');
      setProducers(data);
    } catch (error) {
      console.error('Error loading producers:', error);
    } finally {
      setProducersLoading(false);
    }
  };

  // Handle product selection to auto-populate related fields
  const handleProductSelect = (productId: string) => {
    setFormData(prev => ({
      ...prev,
      productid: productId,
      // You could auto-populate other fields here if needed
      // For example, if you have default values based on product type
    }));
  };

  // Handle producer selection
  const handleProducerSelect = (username: string) => {
    setFormData(prev => ({
      ...prev,
      producedby: username,
      // Auto-populate lastupdatedby if it's empty
      lastupdatedby: prev.lastupdatedby || username
    }));
  };

  // Reset form when modal opens
  React.useEffect(() => {
    if (isOpen) {
      const now = new Date();
      const dateStr = now.toISOString().split('T')[0]; // YYYY-MM-DD
      const datetimeStr = now.toISOString().slice(0, 16); // YYYY-MM-DDTHH:mm
      
      setFormData({
        productid: '',
        basicmediumid: '',
        addictiveid: '',
        quantityinstock: 0,
        productiondate: dateStr,
        imageurl: '',
        status: 'AVAILABLE(可用)' as InventoryStatusType,
        productiondatetime: datetimeStr,
        producedby: '',
        lastupdatedby: '',
        to_show: true,
        // COA fields (optional)
        coa_appearance: '',
        coa_clarity: undefined as boolean | undefined,
        coa_osmoticpressure: undefined as number | undefined,
        coa_ph: undefined as number | undefined,
        coa__mycoplasma: undefined as boolean | undefined,
        coa_sterility: undefined as boolean | undefined,
        coa_fillingvolumedifference: undefined as boolean | undefined
      });

      // Load product details for autocomplete
      loadProductDetails();
      loadProducers();
    }
  }, [isOpen]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      
      // Basic validation
      if (!formData.productid.trim()) {
        alert('请输入产品ID');
        return;
      }
      if (!formData.basicmediumid.trim()) {
        alert('请输入基础培养基ID');
        return;
      }
      if (!formData.addictiveid.trim()) {
        alert('请输入添加剂ID');
        return;
      }
      if (!formData.producedby.trim()) {
        alert('请输入生产人员');
        return;
      }
      if (!formData.productiondate) {
        alert('请选择生产日期');
        return;
      }
      if (!formData.productiondatetime) {
        alert('请选择生产时间');
        return;
      }
      
      // Format the data to match backend schema
      const inventoryData: ProductInventoryCreateRequest = {
        productid: formData.productid,
        basicmediumid: formData.basicmediumid,
        addictiveid: formData.addictiveid,
        quantityinstock: formData.quantityinstock,
        productiondate: formData.productiondate, // Should be YYYY-MM-DD format
        status: formData.status,
        productiondatetime: formData.productiondatetime ? 
          new Date(formData.productiondatetime).toISOString() : 
          new Date().toISOString(),
        producedby: formData.producedby,
        lastupdatedby: formData.lastupdatedby || formData.producedby,
        to_show: formData.to_show,
        // Include imageurl only if provided
        ...(formData.imageurl && formData.imageurl.trim() && { imageurl: formData.imageurl.trim() }),
        // Only include COA fields if they have meaningful values (not empty strings or undefined)
        ...(formData.coa_appearance && formData.coa_appearance.trim() && { coa_appearance: formData.coa_appearance.trim() }),
        ...(formData.coa_clarity !== undefined && { coa_clarity: formData.coa_clarity }),
        ...(formData.coa_osmoticpressure !== undefined && formData.coa_osmoticpressure !== null && { coa_osmoticpressure: formData.coa_osmoticpressure }),
        ...(formData.coa_ph !== undefined && formData.coa_ph !== null && { coa_ph: formData.coa_ph }),
        ...(formData.coa__mycoplasma !== undefined && { coa__mycoplasma: formData.coa__mycoplasma }),
        ...(formData.coa_sterility !== undefined && { coa_sterility: formData.coa_sterility }),
        ...(formData.coa_fillingvolumedifference !== undefined && { coa_fillingvolumedifference: formData.coa_fillingvolumedifference })
      };
      
      console.log('Sending inventory data:', inventoryData); // Debug log
      
      await ProductApi.createProductInventory(inventoryData);
      onSuccess();
    } catch (error) {
      console.error('Error creating inventory:', error);
      // Show a user-friendly error message
      alert(`创建库存失败: ${error instanceof Error ? error.message : '未知错误'}`);
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
          <Autocomplete
            label="产品ID"
            value={formData.productid}
            onChange={handleProductSelect}
            options={productDetails.map(product => ({
              value: product.productid,
              label: product.productnamezh,
              description: `${product.productnameen} | ${product.category} | ${product.specification}`
            }))}
            loading={productDetailsLoading}
            required
            placeholder="选择或输入产品ID"
          />
          <Input
            label="基础培养基ID"
            value={formData.basicmediumid}
            onChange={(e) => setFormData({...formData, basicmediumid: e.target.value})}
            required
            placeholder="如: BM001"
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <Input
            label="添加剂ID"
            value={formData.addictiveid}
            onChange={(e) => setFormData({...formData, addictiveid: e.target.value})}
            required
            placeholder="如: AD001"
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
          <Input
            label="生产时间"
            type="datetime-local"
            value={formData.productiondatetime}
            onChange={(e) => setFormData({...formData, productiondatetime: e.target.value})}
            required
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <Autocomplete
            label="生产人员"
            value={formData.producedby}
            onChange={handleProducerSelect}
            options={producers.map(producer => ({
              value: producer.username,
              label: producer.username,
              description: producer.email
            }))}
            loading={producersLoading}
            placeholder="选择生产人员"
            required
          />
          <Input
            label="最后更新人员"
            value={formData.lastupdatedby}
            onChange={(e) => setFormData({...formData, lastupdatedby: e.target.value})}
            placeholder="默认与生产人员相同"
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <Select
            label="状态"
            value={formData.status}
            onChange={(e) => setFormData({...formData, status: e.target.value as InventoryStatusType})}
            options={statusOptions}
            required
          />
          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="to_show"
              checked={formData.to_show}
              onChange={(e) => setFormData({...formData, to_show: e.target.checked})}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <label htmlFor="to_show" className="text-sm font-medium text-gray-700">
              在系统中显示
            </label>
          </div>
        </div>
        <Input
          label="图片URL (可选)"
          value={formData.imageurl}
          onChange={(e) => setFormData({...formData, imageurl: e.target.value})}
          placeholder="输入产品图片URL (可选)"
        />
        
        {/* COA Section */}
        <div className="pt-4 border-t border-gray-200">
          <h4 className="text-md font-medium text-gray-900 mb-4">COA 检测信息 (可选)</h4>
          <div className="grid grid-cols-2 gap-4">
            <Input
              label="外观"
              value={formData.coa_appearance}
              onChange={(e) => setFormData({...formData, coa_appearance: e.target.value})}
              placeholder="描述产品外观"
            />
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">透明度</label>
              <Select
                value={formData.coa_clarity === undefined ? '' : formData.coa_clarity.toString()}
                onChange={(e) => setFormData({...formData, coa_clarity: e.target.value === '' ? undefined : e.target.value === 'true'})}
                options={[
                  { value: '', label: '未测试' },
                  { value: 'true', label: '透明' },
                  { value: 'false', label: '不透明' }
                ]}
              />
            </div>
            <Input
              label="渗透压"
              type="number"
              step="0.01"
              value={formData.coa_osmoticpressure || ''}
              onChange={(e) => setFormData({...formData, coa_osmoticpressure: e.target.value ? Number(e.target.value) : undefined})}
              placeholder="数值"
            />
            <Input
              label="pH值"
              type="number"
              step="0.01"
              value={formData.coa_ph || ''}
              onChange={(e) => setFormData({...formData, coa_ph: e.target.value ? Number(e.target.value) : undefined})}
              placeholder="数值"
            />
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">支原体检测</label>
              <Select
                value={formData.coa__mycoplasma === undefined ? '' : formData.coa__mycoplasma.toString()}
                onChange={(e) => setFormData({...formData, coa__mycoplasma: e.target.value === '' ? undefined : e.target.value === 'true'})}
                options={[
                  { value: '', label: '未测试' },
                  { value: 'true', label: '阴性' },
                  { value: 'false', label: '阳性' }
                ]}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">无菌检测</label>
              <Select
                value={formData.coa_sterility === undefined ? '' : formData.coa_sterility.toString()}
                onChange={(e) => setFormData({...formData, coa_sterility: e.target.value === '' ? undefined : e.target.value === 'true'})}
                options={[
                  { value: '', label: '未测试' },
                  { value: 'true', label: '无菌' },
                  { value: 'false', label: '有菌' }
                ]}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">装量差异</label>
              <Select
                value={formData.coa_fillingvolumedifference === undefined ? '' : formData.coa_fillingvolumedifference.toString()}
                onChange={(e) => setFormData({...formData, coa_fillingvolumedifference: e.target.value === '' ? undefined : e.target.value === 'true'})}
                options={[
                  { value: '', label: '未测试' },
                  { value: 'true', label: '合格' },
                  { value: 'false', label: '不合格' }
                ]}
              />
            </div>
          </div>
        </div>
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
