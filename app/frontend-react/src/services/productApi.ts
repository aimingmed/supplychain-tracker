import type { ProductDetails, ProductInventory } from '../types';

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
    const response = await fetch(`${API_BASE_URL}/productlog/product-details`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      throw new Error(`Failed to create product: ${response.statusText}`);
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
}

export default ProductApi;
