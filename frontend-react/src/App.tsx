import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAuth } from './hooks/useAuth';
import { Login } from './components/Login';
import { Shop } from './pages/Shop';
import { Cart } from './pages/Cart';
import { Orders } from './pages/Orders';
import { Account } from './pages/Account';
import { ShoppingBag, ShoppingCart, Package, User, LogOut } from 'lucide-react';

const queryClient = new QueryClient();

function AppLayout() {
  const { isAuthenticated, username, logout } = useAuth();

  if (!isAuthenticated) {
    return <Login />;
  }

  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <header className="bg-blue-600 text-white shadow-lg">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold">Customer Order Services</h1>
            <div className="flex items-center gap-4">
              <span className="text-sm">Welcome, {username}!</span>
              <button
                onClick={logout}
                className="flex items-center gap-2 bg-blue-700 px-3 py-2 rounded hover:bg-blue-800"
              >
                <LogOut className="w-4 h-4" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b">
        <div className="container mx-auto px-4">
          <div className="flex space-x-8">
            <Link
              to="/shop"
              className="flex items-center gap-2 py-4 border-b-2 border-transparent hover:border-blue-600"
            >
              <ShoppingBag className="w-5 h-5" />
              Shop
            </Link>
            <Link
              to="/cart"
              className="flex items-center gap-2 py-4 border-b-2 border-transparent hover:border-blue-600"
            >
              <ShoppingCart className="w-5 h-5" />
              Cart
            </Link>
            <Link
              to="/orders"
              className="flex items-center gap-2 py-4 border-b-2 border-transparent hover:border-blue-600"
            >
              <Package className="w-5 h-5" />
              Order History
            </Link>
            <Link
              to="/account"
              className="flex items-center gap-2 py-4 border-b-2 border-transparent hover:border-blue-600"
            >
              <User className="w-5 h-5" />
              Account
            </Link>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden bg-gray-50">
        <Routes>
          <Route path="/" element={<Navigate to="/shop" replace />} />
          <Route path="/shop" element={<Shop />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/orders" element={<Orders />} />
          <Route path="/account" element={<Account />} />
        </Routes>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-3 text-center text-sm">
        <p>Customer Order Services - Modern React Edition</p>
      </footer>
    </div>
  );
}

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppLayout />
      </BrowserRouter>
    </QueryClientProvider>
  );
}
