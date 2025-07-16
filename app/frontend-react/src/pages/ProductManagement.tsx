import React, { useState, useEffect } from 'react';
import { Search, RotateCcw, Plus, Edit, Trash2, History, RefreshCw } from 'lucide-react';
import { Card, Button, Input, Select, Table, Modal } from '../components/ui';
import { Category, SubCategory, Source, Unit } from '../types';
import type { ProductDetails, CategoryType } from '../types';
import ProductApi from '../services/productApi';

const ProductManagement: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<CategoryType>(Category.ORGANOID);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [products, setProducts] = useState<ProductDetails[]>([]);

  // Form state for adding new product
  const [newProduct, setNewProduct] = useState<Partial<ProductDetails>>({
    productid: '',
    category: Category.ORGANOID,
    setsubcategory: SubCategory.HUMAN_ORGANOID,
    source: Source.HUMAN,
    productnameen: '',
    productnamezh: '',
    specification: '',
    unit: Unit.BOX,
    components: [],
    is_sold_independently: true,
    remarks_temperature: '',
    storage_temperature_duration: '',
    reorderlevel: 10,
    targetstocklevel: 100,
    leadtime: 5
  });

  // Category options matching backend enums
  const categoryOptions = [
    { value: Category.ORGANOID, label: Category.ORGANOID },
    { value: Category.CONSUMABLE, label: Category.CONSUMABLE },
    { value: Category.EQUIPMENT, label: Category.EQUIPMENT },
    { value: Category.REAGENT, label: Category.REAGENT }
  ];

  // SubCategory options
  const subCategoryOptions = Object.values(SubCategory).map(value => ({
    value,
    label: value
  }));

  // Source options
  const sourceOptions = Object.values(Source).map(value => ({
    value,
    label: value
  }));

  // Unit options
  const unitOptions = Object.values(Unit).map(value => ({
    value,
    label: value
  }));

  // Fetch products from API
  const fetchProducts = async () => {
    setLoading(true);
    try {
      const data = await ProductApi.getAllProductDetails();
      setProducts(data);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  // Filter products based on search term and selected category
  const filteredProducts = products.filter(product => {
    const matchesCategory = product.category === selectedCategory;
    const matchesSearch = !searchTerm || 
      product.productid.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.productnamezh.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.productnameen.toLowerCase().includes(searchTerm.toLowerCase());
    
    return matchesCategory && matchesSearch;
  });

  useEffect(() => {
    fetchProducts();
  }, []);

  const columns = [
    { key: 'productid', label: '产品编号', align: 'center' as const, sortable: true },
    { key: 'category', label: '产品类别', align: 'center' as const },
    { key: 'productnamezh', label: '产品名称(中文)', align: 'center' as const },
    { key: 'productnameen', label: '产品名称(英文)', align: 'center' as const },
    { key: 'specification', label: '规格', align: 'center' as const },
    { key: 'unit', label: '单位', align: 'center' as const },
    { key: 'setsubcategory', label: '产品子类别', align: 'center' as const },
    { key: 'source', label: '来源', align: 'center' as const },
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

  const handleSearch = async () => {
    // The search is now handled by the filteredProducts computed value
    // But we can still refresh the data if needed
    await fetchProducts();
  };

  const handleReset = () => {
    setSearchTerm('');
    setSelectedCategory(Category.ORGANOID);
  };

  const handleAddProduct = async () => {
    try {
      // Validate required fields
      if (!newProduct.productid || !newProduct.productnamezh || !newProduct.productnameen) {
        alert('请填写必要字段：产品编号、中文名称、英文名称');
        return;
      }

      await ProductApi.createProductDetails(newProduct as ProductDetails);
      setIsAddModalOpen(false);
      await fetchProducts();
      
      // Reset form
      setNewProduct({
        productid: '',
        category: Category.ORGANOID,
        setsubcategory: SubCategory.HUMAN_ORGANOID,
        source: Source.HUMAN,
        productnameen: '',
        productnamezh: '',
        specification: '',
        unit: Unit.BOX,
        components: [],
        is_sold_independently: true,
        remarks_temperature: '',
        storage_temperature_duration: '',
        reorderlevel: 10,
        targetstocklevel: 100,
        leadtime: 5
      });
    } catch (error) {
      console.error('Error adding product:', error);
      alert('添加产品失败，请重试');
    }
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

      {/* Product Category Tabs and Actions */}
      <Card>
        <div className="flex justify-between items-center">
          {/* Product Category Toggle */}
          <div className="flex border rounded-md">
            {categoryOptions.map((type) => (
              <button
                key={type.value}
                onClick={() => setSelectedCategory(type.value)}
                className={`px-4 py-2 text-sm font-medium transition-colors ${
                  selectedCategory === type.value
                    ? 'bg-primary-500 text-white'
                    : 'text-gray-700 hover:bg-gray-50'
                } ${type.value === categoryOptions[0].value ? 'rounded-l-md' : ''} ${
                  type.value === categoryOptions[categoryOptions.length - 1].value ? 'rounded-r-md' : ''
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
          data={filteredProducts}
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
            <Button onClick={handleAddProduct}>
              确定
            </Button>
          </>
        }
      >
        <div className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <Input
              label="产品编号"
              placeholder="请输入产品编号"
              value={newProduct.productid || ''}
              onChange={(e) => setNewProduct({...newProduct, productid: e.target.value})}
            />
            <Select
              label="产品类别"
              options={categoryOptions}
              value={newProduct.category}
              onChange={(e) => setNewProduct({...newProduct, category: e.target.value as CategoryType})}
            />
            <Select
              label="产品子类别"
              options={subCategoryOptions}
              value={newProduct.setsubcategory}
              onChange={(e) => setNewProduct({...newProduct, setsubcategory: e.target.value as any})}
            />
            <Select
              label="产品来源"
              options={sourceOptions}
              value={newProduct.source}
              onChange={(e) => setNewProduct({...newProduct, source: e.target.value as any})}
            />
            <Input
              label="产品名称(中文)"
              placeholder="请输入产品名称"
              value={newProduct.productnamezh || ''}
              onChange={(e) => setNewProduct({...newProduct, productnamezh: e.target.value})}
            />
            <Input
              label="产品名称(英文)"
              placeholder="Please enter product name"
              value={newProduct.productnameen || ''}
              onChange={(e) => setNewProduct({...newProduct, productnameen: e.target.value})}
            />
            <Input
              label="规格"
              placeholder="请输入规格"
              value={newProduct.specification || ''}
              onChange={(e) => setNewProduct({...newProduct, specification: e.target.value})}
            />
            <Select
              label="产品单位"
              options={unitOptions}
              value={newProduct.unit}
              onChange={(e) => setNewProduct({...newProduct, unit: e.target.value as any})}
            />
            <Input
              label="补货水平"
              type="number"
              placeholder="10"
              value={newProduct.reorderlevel?.toString() || ''}
              onChange={(e) => setNewProduct({...newProduct, reorderlevel: parseInt(e.target.value) || 0})}
            />
            <Input
              label="目标库存水平"
              type="number"
              placeholder="100"
              value={newProduct.targetstocklevel?.toString() || ''}
              onChange={(e) => setNewProduct({...newProduct, targetstocklevel: parseInt(e.target.value) || 0})}
            />
            <Input
              label="交货时间(天)"
              type="number"
              placeholder="5"
              value={newProduct.leadtime?.toString() || ''}
              onChange={(e) => setNewProduct({...newProduct, leadtime: parseInt(e.target.value) || 0})}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">温度标注</label>
            <Input
              placeholder="如: Store at -20°C"
              value={newProduct.remarks_temperature || ''}
              onChange={(e) => setNewProduct({...newProduct, remarks_temperature: e.target.value})}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">储存温度&质保期</label>
            <Input
              placeholder="如: Store at -20°C for 6 months"
              value={newProduct.storage_temperature_duration || ''}
              onChange={(e) => setNewProduct({...newProduct, storage_temperature_duration: e.target.value})}
            />
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="is_sold_independently"
              checked={newProduct.is_sold_independently || false}
              onChange={(e) => setNewProduct({...newProduct, is_sold_independently: e.target.checked})}
              className="mr-2"
            />
            <label htmlFor="is_sold_independently" className="text-sm font-medium text-gray-700">
              是否独立销售
            </label>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default ProductManagement;
