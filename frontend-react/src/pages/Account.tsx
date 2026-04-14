import { useQuery } from '@tanstack/react-query';
import { customerApi } from '../services/api';
import { User, MapPin, Building2, Home } from 'lucide-react';

export function Account() {
  const { data: customer, isLoading } = useQuery({
    queryKey: ['customer'],
    queryFn: customerApi.get,
  });

  if (isLoading) {
    return <div className="p-6 text-center">Loading account information...</div>;
  }

  if (!customer) {
    return <div className="p-6 text-center">No account information found</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-3xl font-bold mb-6 flex items-center gap-2">
        <User className="w-8 h-8" />
        Account Information
      </h2>

      <div className="grid gap-6">
        {/* Personal Info */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4">Personal Information</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm text-gray-600">Name</label>
              <p className="font-semibold">{customer.name}</p>
            </div>
            <div>
              <label className="text-sm text-gray-600">Username</label>
              <p className="font-semibold">{customer.username}</p>
            </div>
            <div>
              <label className="text-sm text-gray-600">Customer ID</label>
              <p className="font-semibold">#{customer.customer_id}</p>
            </div>
            <div>
              <label className="text-sm text-gray-600">Account Type</label>
              <p className="font-semibold capitalize flex items-center gap-2">
                {customer.type === 'business' ? (
                  <><Building2 className="w-4 h-4" /> Business</>
                ) : (
                  <><Home className="w-4 h-4" /> Residential</>
                )}
              </p>
            </div>
          </div>
        </div>

        {/* Address */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <MapPin className="w-5 h-5" />
            Address
          </h3>
          <div className="space-y-2">
            <p>{customer.street || 'N/A'}</p>
            <p>
              {customer.city}, {customer.state} {customer.zip_code}
            </p>
          </div>
        </div>

        {/* Type-specific info */}
        {customer.type === 'business' && customer.business_partner && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold mb-4">Business Details</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm text-gray-600">Business Partner</label>
                <p className="font-semibold">{customer.business_partner}</p>
              </div>
              <div>
                <label className="text-sm text-gray-600">Volume Discount</label>
                <p className="font-semibold">{customer.volume_discount}%</p>
              </div>
              {customer.description && (
                <div className="col-span-2">
                  <label className="text-sm text-gray-600">Description</label>
                  <p>{customer.description}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {customer.type === 'residential' && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold mb-4">Residential Details</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm text-gray-600">Frequent Customer</label>
                <p className="font-semibold">{customer.frequent_customer === 'Y' ? 'Yes' : 'No'}</p>
              </div>
              <div>
                <label className="text-sm text-gray-600">Household Size</label>
                <p className="font-semibold">{customer.household_size || 'N/A'}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
