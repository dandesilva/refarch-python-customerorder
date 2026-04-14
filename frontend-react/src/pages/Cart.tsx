import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { customerApi } from '../services/api';
import { Trash2, Check } from 'lucide-react';

export function Cart() {
  const queryClient = useQueryClient();

  const { data: customer } = useQuery({
    queryKey: ['customer'],
    queryFn: customerApi.get,
  });

  const removeItemMutation = useMutation({
    mutationFn: ({ productId, etag }: { productId: number; etag: string }) =>
      customerApi.removeLineItem(productId, etag),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['customer'] });
    },
  });

  const submitOrderMutation = useMutation({
    mutationFn: (etag: string) => customerApi.submitOrder(etag),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['customer'] });
      alert('Order submitted successfully!');
    },
  });

  const handleRemoveItem = (productId: number) => {
    if (!customer?.open_order?.version) return;
    removeItemMutation.mutate({
      productId,
      etag: customer.open_order.version.toString(),
    });
  };

  const handleSubmitOrder = () => {
    if (!customer?.open_order?.version) return;
    if (confirm('Submit this order?')) {
      submitOrderMutation.mutate(customer.open_order.version.toString());
    }
  };

  const order = customer?.open_order;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-3xl font-bold mb-6">Shopping Cart</h2>

      {!order || order.lineitems.length === 0 ? (
        <div className="bg-gray-100 p-12 rounded-lg text-center">
          <p className="text-xl text-gray-600">Your cart is empty</p>
          <p className="text-gray-500 mt-2">Add some products from the Shop page</p>
        </div>
      ) : (
        <div>
          <div className="bg-white rounded-lg shadow-md">
            <div className="divide-y">
              {order.lineitems.map((item) => (
                <div key={item.product_id} className="p-4 flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg">Product #{item.product_id}</h3>
                    <p className="text-gray-600">Quantity: {item.quantity}</p>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="text-xl font-bold text-blue-600">
                      ${parseFloat(item.amount).toFixed(2)}
                    </span>
                    <button
                      onClick={() => handleRemoveItem(item.product_id)}
                      className="text-red-600 hover:text-red-800 p-2"
                      disabled={removeItemMutation.isPending}
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              ))}
            </div>

            <div className="p-6 bg-gray-50 border-t">
              <div className="flex justify-between items-center mb-4">
                <span className="text-xl font-semibold">Order Total:</span>
                <span className="text-2xl font-bold text-blue-600">
                  ${parseFloat(order.total).toFixed(2)}
                </span>
              </div>
              <button
                onClick={handleSubmitOrder}
                disabled={submitOrderMutation.isPending}
                className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 disabled:opacity-50 flex items-center justify-center gap-2 font-semibold"
              >
                <Check className="w-5 h-5" />
                {submitOrderMutation.isPending ? 'Submitting...' : 'Submit Order'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
