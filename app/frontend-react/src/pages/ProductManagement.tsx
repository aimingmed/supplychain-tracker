import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { Search, RotateCcw, Plus, Edit, Trash2, History, RefreshCw, Eye } from 'lucide-react';
import { Card, Button, Input, Select, Table, Modal } from '../components/ui';
import { Category, SubCategory, Source, Unit } from '../types';
import type { ProductDetails, CategoryType } from '../types';
import ProductApi from '../services/productApi';
import { useAuth } from '../contexts/AuthContext';

// Constants
const DEFAULT_PRODUCT: Partial<ProductDetails> = {
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
};

const PERMISSION_ROLES = ['ADMIN', 'PRODUCTION_MANAGER'];

// Helper functions
const createSelectOptions = <T extends string>(values: T[]) =>
  values.map(value => ({ value, label: value }));

const validateRequiredFields = (product: Partial<ProductDetails>): string | null => {
  if (!product.productid || !product.productnamezh || !product.productnameen) {
    return '请填写必要字段：产品编号、中文名称、英文名称';
  }
  return null;
};

const formatErrorMessage = (error: unknown, defaultMessage: string): string => {
  return error instanceof Error ? error.message : defaultMessage;
};

// Form field component for reusability
const ProductFormFields: React.FC<{
  product: Partial<ProductDetails>;
  setProduct: (product: Partial<ProductDetails>) => void;
  categoryOptions: Array<{ value: string; label: string }>;
  subCategoryOptions: Array<{ value: string; label: string }>;
  sourceOptions: Array<{ value: string; label: string }>;
  unitOptions: Array<{ value: string; label: string }>;
  isEdit?: boolean;
}> = React.memo(({ product, setProduct, categoryOptions, subCategoryOptions, sourceOptions, unitOptions, isEdit = false }) => (
  <>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <Input
        label="产品编号"
        placeholder="请输入产品编号"
        value={product.productid || ''}
        onChange={(e) => setProduct({...product, productid: e.target.value})}
      />
      <Select
        label="产品类别"
        options={categoryOptions}
        value={product.category}
        onChange={(e) => setProduct({...product, category: e.target.value as CategoryType})}
      />
      <Select
        label="产品子类别"
        options={subCategoryOptions}
        value={product.setsubcategory}
        onChange={(e) => setProduct({...product, setsubcategory: e.target.value as any})}
      />
      <Select
        label="产品来源"
        options={sourceOptions}
        value={product.source}
        onChange={(e) => setProduct({...product, source: e.target.value as any})}
      />
      <Input
        label="产品名称(中文)"
        placeholder="请输入产品名称"
        value={product.productnamezh || ''}
        onChange={(e) => setProduct({...product, productnamezh: e.target.value})}
      />
      <Input
        label="产品名称(英文)"
        placeholder="Please enter product name"
        value={product.productnameen || ''}
        onChange={(e) => setProduct({...product, productnameen: e.target.value})}
      />
      <Input
        label="规格"
        placeholder="请输入规格"
        value={product.specification || ''}
        onChange={(e) => setProduct({...product, specification: e.target.value})}
      />
      <Select
        label="产品单位"
        options={unitOptions}
        value={product.unit}
        onChange={(e) => setProduct({...product, unit: e.target.value as any})}
      />
      <Input
        label="补货水平"
        type="number"
        placeholder="10"
        value={product.reorderlevel?.toString() || ''}
        onChange={(e) => setProduct({...product, reorderlevel: parseInt(e.target.value) || 0})}
      />
      <Input
        label="目标库存水平"
        type="number"
        placeholder="100"
        value={product.targetstocklevel?.toString() || ''}
        onChange={(e) => setProduct({...product, targetstocklevel: parseInt(e.target.value) || 0})}
      />
      <Input
        label="交货时间(天)"
        type="number"
        placeholder="5"
        value={product.leadtime?.toString() || ''}
        onChange={(e) => setProduct({...product, leadtime: parseInt(e.target.value) || 0})}
      />
    </div>

    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">温度标注</label>
      <Input
        placeholder="如: Store at -20°C"
        value={product.remarks_temperature || ''}
        onChange={(e) => setProduct({...product, remarks_temperature: e.target.value})}
      />
    </div>

    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">储存温度&质保期</label>
      <Input
        placeholder="如: Store at -20°C for 6 months"
        value={product.storage_temperature_duration || ''}
        onChange={(e) => setProduct({...product, storage_temperature_duration: e.target.value})}
      />
    </div>

    <div className="flex items-center">
      <input
        type="checkbox"
        id={isEdit ? "edit_is_sold_independently" : "is_sold_independently"}
        checked={product.is_sold_independently || false}
        onChange={(e) => setProduct({...product, is_sold_independently: e.target.checked})}
        className="mr-2"
      />
      <label htmlFor={isEdit ? "edit_is_sold_independently" : "is_sold_independently"} className="text-sm font-medium text-gray-700">
        是否独立销售
      </label>
    </div>
  </>
));

const ProductManagement: React.FC = () => {
  const { user } = useAuth();
  
  // State
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<CategoryType>(Category.ORGANOID);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDetailsModalOpen, setIsDetailsModalOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<ProductDetails | null>(null);
  const [productForDetails, setProductForDetails] = useState<ProductDetails | null>(null);
  const [loading, setLoading] = useState(false);
  const [products, setProducts] = useState<ProductDetails[]>([]);
  const [error, setError] = useState<string>('');
  const [newProduct, setNewProduct] = useState<Partial<ProductDetails>>(DEFAULT_PRODUCT);

  // Computed values
  const canManageProducts = useMemo(() => 
    user?.list_of_roles?.some(role => PERMISSION_ROLES.includes(role)) ?? false,
    [user?.list_of_roles]
  );

  const categoryOptions = useMemo(() => createSelectOptions(Object.values(Category)), []);
  const subCategoryOptions = useMemo(() => createSelectOptions(Object.values(SubCategory)), []);
  const sourceOptions = useMemo(() => createSelectOptions(Object.values(Source)), []);
  const unitOptions = useMemo(() => createSelectOptions(Object.values(Unit)), []);

  const filteredProducts = useMemo(() => 
    products.filter(product => {
      const matchesCategory = product.category === selectedCategory;
      const matchesSearch = !searchTerm || 
        product.productid.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.productnamezh.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.productnameen.toLowerCase().includes(searchTerm.toLowerCase());
      
      return matchesCategory && matchesSearch;
    }),
    [products, selectedCategory, searchTerm]
  );

  // API handlers
  const fetchProducts = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const data = await ProductApi.getAllProductDetails();
      setProducts(data);
    } catch (error) {
      console.error('Error fetching products:', error);
      setError('获取产品列表失败');
    } finally {
      setLoading(false);
    }
  }, []);

  // Event handlers
  const handleSearch = useCallback(async () => {
    await fetchProducts();
  }, [fetchProducts]);

  const handleReset = useCallback(() => {
    setSearchTerm('');
    setSelectedCategory(Category.ORGANOID);
  }, []);

  const handleSelectProductForEdit = useCallback((product: ProductDetails) => {
    if (!canManageProducts) {
      setError('您没有权限修改产品，只有管理员或生产管理员可以修改产品');
      return;
    }
    
    setSelectedProduct(product);
    setError('');
    setIsEditModalOpen(true);
  }, [canManageProducts]);

  const resetNewProduct = useCallback(() => {
    setNewProduct(DEFAULT_PRODUCT);
  }, []);

  const handleOpenAddModal = useCallback(() => {
    if (!canManageProducts) {
      setError('您没有权限创建产品，只有管理员或生产管理员可以创建产品');
      return;
    }
    setError('');
    setIsAddModalOpen(true);
  }, [canManageProducts]);

  const handleAddProduct = useCallback(async () => {
    try {
      setError('');
      
      const validationError = validateRequiredFields(newProduct);
      if (validationError) {
        setError(validationError);
        return;
      }

      if (!canManageProducts) {
        setError('您没有权限创建产品，只有管理员或生产管理员可以创建产品');
        return;
      }

      await ProductApi.createProductDetails(newProduct as ProductDetails);
      setIsAddModalOpen(false);
      await fetchProducts();
      resetNewProduct();
    } catch (error) {
      console.error('Error adding product:', error);
      setError(formatErrorMessage(error, '添加产品失败，请重试'));
    }
  }, [newProduct, canManageProducts, fetchProducts, resetNewProduct]);

  const handleEditProduct = useCallback(async () => {
    if (!selectedProduct) return;
    
    try {
      setError('');
      
      const validationError = validateRequiredFields(selectedProduct);
      if (validationError) {
        setError(validationError);
        return;
      }

      if (!canManageProducts) {
        setError('您没有权限修改产品，只有管理员或生产管理员可以修改产品');
        return;
      }

      await ProductApi.updateProductDetails(selectedProduct.productid, selectedProduct);
      setIsEditModalOpen(false);
      setSelectedProduct(null);
      await fetchProducts();
    } catch (error) {
      console.error('Error updating product:', error);
      setError(formatErrorMessage(error, '修改产品失败，请重试'));
    }
  }, [selectedProduct, canManageProducts, fetchProducts]);

  const handleEditProductChange = useCallback((product: Partial<ProductDetails>) => {
    setSelectedProduct(product as ProductDetails);
  }, []);

  const handleDeleteProduct = useCallback(async (product: ProductDetails) => {
    if (!canManageProducts) {
      setError('您没有权限删除产品，只有管理员或生产管理员可以删除产品');
      return;
    }

    const confirmed = window.confirm(`确定要删除产品 "${product.productnamezh}" (${product.productid}) 吗？此操作不可撤销。`);
    if (!confirmed) return;

    try {
      setError('');
      await ProductApi.deleteProductDetails(product.productid);
      await fetchProducts();
    } catch (error) {
      console.error('Error deleting product:', error);
      setError(formatErrorMessage(error, '删除产品失败，请重试'));
    }
  }, [canManageProducts, fetchProducts]);

  const handleShowProductDetails = useCallback((product: ProductDetails) => {
    setProductForDetails(product);
    setError('');
    setIsDetailsModalOpen(true);
  }, []);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  // Table columns configuration
  const columns = useMemo(() => [
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
      render: (_value: any, product: ProductDetails) => (
        <div className="flex flex-col sm:flex-row gap-1 sm:gap-2 justify-center">
          <Button 
            variant="secondary" 
            size="sm"
            icon={Eye}
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              handleShowProductDetails(product);
            }}
            className="w-full sm:w-auto"
          >
            <span className="sm:hidden">详情</span>
            <span className="hidden sm:inline">详情</span>
          </Button>
          {canManageProducts && (
            <>
              <Button 
                variant="secondary" 
                size="sm" 
                icon={Edit}
                onClick={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  handleSelectProductForEdit(product);
                }}
                className="w-full sm:w-auto"
              >
                <span className="sm:hidden">编辑</span>
                <span className="hidden sm:inline">编辑</span>
              </Button>
              <Button 
                variant="danger" 
                size="sm" 
                icon={Trash2}
                onClick={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  handleDeleteProduct(product);
                }}
                className="w-full sm:w-auto"
              >
                <span className="sm:hidden">删除</span>
                <span className="hidden sm:inline">删除</span>
              </Button>
            </>
          )}
        </div>
      )
    }
  ], [canManageProducts, handleSelectProductForEdit, handleDeleteProduct, handleShowProductDetails]);

  return (
    <div className="space-y-6">
      {/* Error Display */}
      {error && (
        <Card>
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        </Card>
      )}

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

      {/* Product Category Tabs and Actions */}
      <Card>
        <div className="flex flex-col lg:flex-row lg:justify-between lg:items-center gap-4">
          {/* Product Category Toggle */}
          <div className="flex overflow-x-auto border rounded-md">
            {categoryOptions.map((type) => (
              <button
                key={type.value}
                onClick={() => setSelectedCategory(type.value)}
                className={`px-3 sm:px-4 py-2 text-sm font-medium transition-colors whitespace-nowrap ${
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
          <div className="flex flex-wrap gap-2">
            {canManageProducts ? (
              <Button icon={Plus} onClick={handleOpenAddModal} className="flex-1 sm:flex-none">
                <span className="hidden sm:inline">添加产品</span>
              </Button>
            ) : (
              <Button 
                icon={Plus} 
                disabled 
                title="只有管理员或生产管理员可以创建产品"
                className="opacity-50 cursor-not-allowed flex-1 sm:flex-none"
              >
                <span className="hidden sm:inline">添加产品</span>
              </Button>
            )}
            <Button variant="secondary" icon={History} className="flex-1 sm:flex-none">
              <span className="hidden sm:inline">历史产品</span>
            </Button>
            <Button variant="secondary" icon={RefreshCw} onClick={fetchProducts} className="flex-1 sm:flex-none">
              <span className="hidden sm:inline">刷新</span>
            </Button>
          </div>
        </div>
      </Card>

      {/* Data Table */}
      <Card>
        <div className="-m-6">
          <Table
            columns={columns}
            data={filteredProducts}
            loading={loading}
          />
        </div>
      </Card>

      {/* Add Product Modal */}
      <Modal
        isOpen={isAddModalOpen}
        onClose={() => {
          setIsAddModalOpen(false);
          setError('');
        }}
        title="添加产品"
        size="xl"
        footer={
          <div className="flex flex-col sm:flex-row gap-2 sm:gap-2">
            <Button variant="secondary" onClick={() => {
              setIsAddModalOpen(false);
              setError('');
            }} className="w-full sm:w-auto">
              取消
            </Button>
            <Button onClick={handleAddProduct} className="w-full sm:w-auto">
              确定
            </Button>
          </div>
        }
      >
        <div className="space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded text-sm">
              {error}
            </div>
          )}
          
          <ProductFormFields
            product={newProduct}
            setProduct={setNewProduct}
            categoryOptions={categoryOptions}
            subCategoryOptions={subCategoryOptions}
            sourceOptions={sourceOptions}
            unitOptions={unitOptions}
          />
        </div>
      </Modal>

      {/* Edit Product Modal */}
      <Modal
        isOpen={isEditModalOpen}
        onClose={() => {
          setIsEditModalOpen(false);
          setSelectedProduct(null);
          setError('');
        }}
        title="修改产品"
        size="xl"
        footer={
          <div className="flex flex-col sm:flex-row gap-2 sm:gap-2">
            <Button variant="secondary" onClick={() => {
              setIsEditModalOpen(false);
              setSelectedProduct(null);
              setError('');
            }} className="w-full sm:w-auto">
              取消
            </Button>
            <Button onClick={handleEditProduct} className="w-full sm:w-auto">
              确定
            </Button>
          </div>
        }
      >
        <div className="space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded text-sm">
              {error}
            </div>
          )}
          
          {selectedProduct && (
            <ProductFormFields
              product={selectedProduct}
              setProduct={handleEditProductChange}
              categoryOptions={categoryOptions}
              subCategoryOptions={subCategoryOptions}
              sourceOptions={sourceOptions}
              unitOptions={unitOptions}
              isEdit={true}
            />
          )}
        </div>
      </Modal>

      {/* Product Details Modal */}
      <Modal
        isOpen={isDetailsModalOpen}
        onClose={() => {
          setIsDetailsModalOpen(false);
          setProductForDetails(null);
        }}
        title="产品详情"
        size="xl"
        footer={
          <Button variant="secondary" onClick={() => {
            setIsDetailsModalOpen(false);
            setProductForDetails(null);
          }} className="w-full sm:w-auto">
            关闭
          </Button>
        }
      >
        <div className="space-y-4">
          {productForDetails && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">产品编号</label>
                <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                  {productForDetails.productid}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">产品类别</label>
                <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                  {productForDetails.category}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">产品子类别</label>
                <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                  {productForDetails.setsubcategory}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">产品来源</label>
                <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                  {productForDetails.source}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">产品名称(中文)</label>
                <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                  {productForDetails.productnamezh}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">产品名称(英文)</label>
                <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                  {productForDetails.productnameen}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">规格</label>
                <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                  {productForDetails.specification || '无'}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">产品单位</label>
                <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                  {productForDetails.unit}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">补货水平</label>
                <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                  {productForDetails.reorderlevel}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">目标库存水平</label>
                <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                  {productForDetails.targetstocklevel}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">交货时间(天)</label>
                <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                  {productForDetails.leadtime}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">是否独立销售</label>
                <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                  {productForDetails.is_sold_independently ? '是' : '否'}
                </div>
              </div>
            </div>
          )}

          {productForDetails && (
            <>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">温度标注</label>
                <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                  {productForDetails.remarks_temperature || '无'}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">储存温度&质保期</label>
                <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                  {productForDetails.storage_temperature_duration || '无'}
                </div>
              </div>

              {productForDetails.components && productForDetails.components.length > 0 && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">产品组件</label>
                  <div className="text-sm text-gray-900 bg-gray-50 p-2 rounded border">
                    {productForDetails.components.join(', ')}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </Modal>
    </div>
  );
};

export default ProductManagement;
