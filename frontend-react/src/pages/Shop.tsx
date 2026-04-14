import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { categoryApi, productApi, customerApi } from '../services/api';
import { Product } from '../types';
import { ShoppingCart, Plus } from 'lucide-react';

export function Shop() {
  const [selectedCategory, setSelectedCategory] = useState<number>(2);
  const [cartMessage, setCartMessage] = useState('');

  const { data: categories = [] } = useQuery({
    queryKey: ['categories'],
    queryFn: categoryApi.getAll,
  });

  const { data: products = [], isLoading } = useQuery({
    queryKey: ['products', selectedCategory],
    queryFn: () => productApi.getByCategory(selectedCategory),
    enabled: !!selectedCategory,
  });

  const { data: customer, refetch: refetchCustomer } = useQuery({
    queryKey: ['customer'],
    queryFn: customerApi.get,
  });

  const addToCart = async (product: Product) => {
    try {
      const etag = customer?.open_order?.version?.toString();
      await customerApi.addLineItem(product.product_id, 1, etag);
      await refetchCustomer();
      setCartMessage(`Added ${product.name} to cart!`);
      setTimeout(() => setCartMessage(''), 3000);
    } catch (error) {
      alert('Failed to add item to cart');
    }
  };

  const topCategories = categories.filter(c => !c.parent_cat_id);

  return (
    <div className="flex h-full">
      {/* Sidebar */}
      <div className="w-64 bg-gray-100 p-4 overflow-y-auto">
        <h3 className="font-bold text-lg mb-4">Categories</h3>
        {topCategories.map((topCat) => {
          const children = categories.filter(c => c.parent_cat_id === topCat.cat_id);
          return (
            <div key={topCat.cat_id} className="mb-4">
              <div className="font-semibold text-gray-700 mb-2">{topCat.name}</div>
              {children.map((child) => (
                <button
                  key={child.cat_id}
                  onClick={() => setSelectedCategory(child.cat_id)}
                  className={`block w-full text-left px-3 py-2 rounded mb-1 ${
                    selectedCategory === child.cat_id
                      ? 'bg-blue-600 text-white'
                      : 'hover:bg-gray-200'
                  }`}
                >
                  {child.name}
                </button>
              ))}
            </div>
          );
        })}
      </div>

      {/* Main Content */}
      <div className="flex-1 p-6 overflow-y-auto">
        {cartMessage && (
          <div className="bg-green-100 text-green-800 p-3 rounded mb-4">
            {cartMessage}
          </div>
        )}

        <h2 className="text-2xl font-bold mb-6">
          {categories.find(c => c.cat_id === selectedCategory)?.name || 'Products'}
        </h2>

        {isLoading ? (
          <div className="text-center py-12">Loading products...</div>
        ) : products.length === 0 ? (
          <div className="text-center py-12 text-gray-500">No products found</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.map((product) => (
              <div key={product.product_id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div className="h-48 bg-gray-200 flex items-center justify-center">
                  {product.image ? (
                    <img src={product.image} alt={product.name} className="max-h-full" />
                  ) : (
                    <div className="text-gray-400">No image</div>
                  )}
                </div>
                <div className="p-4">
                  <h3 className="font-bold text-lg mb-2">{product.name}</h3>
                  <p className="text-gray-600 text-sm mb-3">{product.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-xl font-bold text-blue-600">
                      ${parseFloat(product.price).toFixed(2)}
                    </span>
                    <button
                      onClick={() => addToCart(product)}
                      className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 flex items-center gap-2"
                    >
                      <Plus className="w-4 h-4" />
                      Add to Cart
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Cart Preview */}
      <div className="w-80 bg-gray-50 p-4 overflow-y-auto border-l">
        <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
          <ShoppingCart className="w-5 h-5" />
          Shopping Cart
        </h3>
        {customer?.open_order?.lineitems && customer.open_order.lineitems.length > 0 ? (
          <div>
            {customer.open_order.lineitems.map((item) => (
              <div key={item.product_id} className="bg-white p-3 rounded mb-2 shadow-sm">
                <div className="font-semibold">Product #{item.product_id}</div>
                <div className="text-sm text-gray-600">Qty: {item.quantity}</div>
                <div className="text-blue-600 font-bold">${parseFloat(item.amount).toFixed(2)}</div>
              </div>
            ))}
            <div className="mt-4 pt-4 border-t">
              <div className="flex justify-between items-center font-bold text-lg">
                <span>Total:</span>
                <span className="text-blue-600">
                  ${parseFloat(customer.open_order.total || '0').toFixed(2)}
                </span>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center text-gray-500 py-8">Cart is empty</div>
        )}
      </div>
    </div>
  );
}
