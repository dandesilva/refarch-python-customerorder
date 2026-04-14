export interface Category {
  cat_id: number;
  name: string;
  parent_cat_id: number | null;
}

export interface Product {
  product_id: number;
  name: string;
  price: string;
  description: string | null;
  image: string | null;
}

export interface LineItem {
  product_id: number;
  quantity: number;
  amount: string;
}

export interface Order {
  order_id: number;
  total: string;
  status: 'OPEN' | 'SUBMITTED' | 'SHIPPED' | 'CLOSED';
  submit_time: string | null;
  version: number;
  lineitems: LineItem[];
}

export interface Customer {
  customer_id: number;
  username: string;
  name: string;
  type: 'business' | 'residential';
  street: string | null;
  city: string | null;
  state: string | null;
  zip_code: string | null;
  open_order: Order | null;
  description?: string | null;
  business_partner?: string | null;
  volume_discount?: string | null;
  frequent_customer?: string | null;
  household_size?: number | null;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  username: string;
}
