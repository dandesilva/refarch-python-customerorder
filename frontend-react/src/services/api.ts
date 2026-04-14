import axios from 'axios';
import type { Category, Product, Customer, Order, AuthResponse } from '../types';

const api = axios.create({
  baseURL: '/api/v1',
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  login: async (username: string, password: string): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/login', null, {
      auth: { username, password }
    });
    return response.data;
  },
};

export const categoryApi = {
  getAll: async (): Promise<Category[]> => {
    const response = await api.get<any[]>('/Category');
    // Flatten nested category structure (API returns subcategories nested)
    const flatCategories: Category[] = [];
    response.data.forEach((topCat: any) => {
      flatCategories.push({
        cat_id: topCat.cat_id,
        name: topCat.name,
        parent_cat_id: topCat.parent_cat_id,
      });
      if (topCat.subCategories) {
        topCat.subCategories.forEach((subCat: any) => {
          flatCategories.push({
            cat_id: subCat.cat_id,
            name: subCat.name,
            parent_cat_id: subCat.parent_cat_id,
          });
        });
      }
    });
    return flatCategories;
  },
  getByParent: async (parentId: number): Promise<Category[]> => {
    const response = await api.get<Category[]>(`/Category?parentId=${parentId}`);
    return response.data;
  },
};

export const productApi = {
  getByCategory: async (categoryId: number): Promise<Product[]> => {
    const response = await api.get<Product[]>(`/Product?categoryId=${categoryId}`);
    return response.data;
  },
  getById: async (id: number): Promise<Product> => {
    const response = await api.get<Product>(`/Product/${id}`);
    return response.data;
  },
};

export const customerApi = {
  get: async (): Promise<Customer> => {
    const response = await api.get<Customer>('/Customer');
    return response.data;
  },
  updateAddress: async (address: {
    street: string;
    city: string;
    state: string;
    zip_code: string;
  }): Promise<void> => {
    await api.put('/Customer/Address', address);
  },
  addLineItem: async (productId: number, quantity: number, etag?: string): Promise<Order> => {
    const headers: any = {};
    if (etag) {
      headers['If-Match'] = etag;
    }
    const response = await api.post<Order>(
      '/Customer/OpenOrder/LineItem',
      { productId, quantity },
      { headers }
    );
    return response.data;
  },
  removeLineItem: async (productId: number, etag: string): Promise<Order> => {
    const response = await api.delete<Order>(
      `/Customer/OpenOrder/LineItem/${productId}`,
      { headers: { 'If-Match': etag } }
    );
    return response.data;
  },
  submitOrder: async (etag: string): Promise<void> => {
    await api.post('/Customer/OpenOrder', null, {
      headers: { 'If-Match': etag }
    });
  },
  getOrderHistory: async (): Promise<Order[]> => {
    const response = await api.get<Order[]>('/Customer/Orders');
    return response.data;
  },
};

export default api;
