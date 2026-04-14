import { useQuery } from '@tanstack/react-query';
import { customerApi } from '../services/api';
import { Package } from 'lucide-react';

export function Orders() {
  const { data: orders = [], isLoading } = useQuery({
    queryKey: ['orderHistory'],
    queryFn: customerApi.getOrderHistory,
  });

  if (isLoading) {
    return <div className="p-6 text-center">Loading order history...</div>;
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h2 className="text-3xl font-bold mb-6 flex items-center gap-2">
        <Package className="w-8 h-8" />
        Order History
      </h2>

      {orders.length === 0 ? (
        <div className="bg-gray-100 p-12 rounded-lg text-center">
          <p className="text-xl text-gray-600">No orders yet</p>
          <p className="text-gray-500 mt-2">Your submitted orders will appear here</p>
        </div>
      ) : (
        <div className="space-y-6">
          {orders.map((order) => (
            <div key={order.order_id} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold">Order #{order.order_id}</h3>
                  <p className="text-gray-600">
                    {order.submit_time
                      ? new Date(order.submit_time).toLocaleDateString()
                      : 'N/A'}
                  </p>
                </div>
                <span
                  className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    order.status === 'SUBMITTED'
                      ? 'bg-blue-100 text-blue-800'
                      : order.status === 'SHIPPED'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {order.status}
                </span>
              </div>

              <div className="border-t pt-4">
                <h4 className="font-semibold mb-2">Items:</h4>
                <div className="space-y-2">
                  {order.lineitems.map((item) => (
                    <div
                      key={item.product_id}
                      className="flex justify-between items-center bg-gray-50 p-3 rounded"
                    >
                      <span>Product #{item.product_id}</span>
                      <span className="text-gray-600">Qty: {item.quantity}</span>
                      <span className="font-semibold">
                        ${parseFloat(item.amount).toFixed(2)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="mt-4 pt-4 border-t flex justify-between items-center">
                <span className="text-lg font-semibold">Total:</span>
                <span className="text-2xl font-bold text-blue-600">
                  ${parseFloat(order.total).toFixed(2)}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
