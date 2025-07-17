import type { ProductDetails, ProductInventory } from '../types';
import AuthApi from './authApi';

// In Vite, environment variables are accessed via import.meta.env and must be prefixed with VITE_
const API_BASE_URL = import.meta.env.VITE_REACT_APP_BASE_URL || 'https://staging-sctracker.aimingmed.local/api';

class ProductApi {
  static async getAllProductDetails(): Promise<ProductDetails[]> {
    const response = await fetch(`${API_BASE_URL}/productlog/product-details`);
    if (!response.ok) {
      throw new Error(`Failed to fetch product details: ${response.statusText}`);
    }
    return response.json();
  }

  static async createProductDetails(data: ProductDetails): Promise<ProductDetails> {
    const token = AuthApi.getToken();
    
    const response = await fetch(`${API_BASE_URL}/productlog/product-details`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
      },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Failed to create product' }));
      throw new Error(errorData.detail || `Failed to create product: ${response.statusText}`);
    }
    return response.json();
  }

  static async getAllProductInventory(): Promise<ProductInventory[]> {
    const response = await fetch(`${API_BASE_URL}/productlog/product-inventory`);
    if (!response.ok) {
      throw new Error(`Failed to fetch product inventory: ${response.statusText}`);
    }
    return response.json();
  }

  static async getProductDetails(productId: string): Promise<ProductDetails> {
    const response = await fetch(`${API_BASE_URL}/productlog/product-details/${productId}`);
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Failed to get product' }));
      throw new Error(errorData.detail || `Failed to get product: ${response.statusText}`);
    }
    return response.json();
  }

  static async updateProductDetails(productId: string, data: ProductDetails): Promise<ProductDetails> {
    const token = AuthApi.getToken();
    
    const response = await fetch(`${API_BASE_URL}/productlog/product-details/${productId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
      },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Failed to update product' }));
      throw new Error(errorData.detail || `Failed to update product: ${response.statusText}`);
    }
    return response.json();
  }

  static async deleteProductDetails(productId: string): Promise<{ message: string; product_id: string }> {
    const token = AuthApi.getToken();
    
    const response = await fetch(`${API_BASE_URL}/productlog/product-details/${productId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
      },
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Failed to delete product' }));
      throw new Error(errorData.detail || `Failed to delete product: ${response.statusText}`);
    }
    return response.json();
  }
}

export default ProductApi;
