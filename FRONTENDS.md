# Web Frontends - Comparison Guide

The Customer Order Services application now has **TWO web frontends** that you can compare side-by-side!

## 🌐 Access Both Frontends

### Modern React Frontend (Port 3000)
**URL:** http://localhost:3000

- **Stack:** React 18 + TypeScript + Vite + TailwindCSS
- **Features:**
  - Modern, responsive UI design
  - Type-safe development
  - Fast hot-reload development
  - State management with Zustand
  - Data fetching with React Query
  - Beautiful gradient design
  - Mobile-friendly

**Pages:**
- Shop (Browse products by category)
- Cart (Manage shopping cart & checkout)
- Orders (View order history)
- Account (View customer profile)

### Classic Dojo Frontend (Port 3001)
**URL:** http://localhost:3001

- **Stack:** Dojo Toolkit (original from JEE version)
- **Features:**
  - Classic Web 2.0 interface
  - Tab-based navigation
  - Tree widget for cart preview
  - DataGrid for product catalog
  - Drag-and-drop functionality
  - Original Dojo widgets

**Pages:**
- Shop (Product catalog with category menu)
- Cart (Shopping cart management)
- Order History (Past orders)
- Account (Customer information)

## 🚀 Starting the Frontends

Both frontends are included in docker-compose:

```bash
# Start everything (API + both frontends)
podman-compose up -d

# Or rebuild and start
podman-compose up -d --build
```

## 🔑 Login Credentials

Both frontends use the same authentication:
- **Username:** `rbarcia`
- **Password:** `b0wfish`

## 📊 Feature Comparison

| Feature | React Frontend | Dojo Frontend |
|---------|----------------|---------------|
| **Technology** | React 18, TypeScript | Dojo Toolkit |
| **Year** | 2024 (Modern) | 2010s (Classic) |
| **Mobile Support** | ✅ Responsive | ❌ Desktop-only |
| **Load Time** | Fast (<1s) | Moderate (~2s) |
| **Bundle Size** | ~200KB (gzipped) | ~500KB+ |
| **Development** | Hot reload | Full page reload |
| **Type Safety** | ✅ TypeScript | ❌ JavaScript |
| **State Management** | Zustand + React Query | Manual XHR |
| **UI Framework** | TailwindCSS | Dijit widgets |
| **Icons** | Lucide React | None |
| **Animations** | CSS transitions | Dojo effects |
| **Browser Support** | Modern browsers | IE8+ |

## 🎨 UI/UX Differences

### React Frontend
- Clean, modern gradient design
- Card-based product layout
- Floating action buttons
- Loading states & error handling
- Toast notifications
- Smooth transitions
- Icon-based navigation

### Dojo Frontend
- Classic tabbed interface
- Grid-based product layout
- Menu-driven navigation
- Tree widget for cart preview
- Dialog boxes
- Traditional form controls
- Toolbar-based actions

## 🧪 Testing Both Frontends

### Test the React Frontend
```bash
# 1. Open http://localhost:3000
# 2. Login with rbarcia/b0wfish
# 3. Browse products in "Shop" tab
# 4. Add items to cart
# 5. View cart in real-time sidebar
# 6. Go to "Cart" to checkout
# 7. Submit order
# 8. View in "Orders" history
```

### Test the Dojo Frontend
```bash
# 1. Open http://localhost:3001
# 2. Login with rbarcia/b0wfish
# 3. Navigate using top tabs
# 4. Browse products via category menu
# 5. Click product to view details
# 6. Drag product to cart tree
# 7. Switch to "Cart" tab
# 8. Submit order
# 9. Check "Order History" tab
```

## 🔧 Development

### React Frontend (Local Development)
```bash
cd frontend-react
npm install
npm run dev
# Opens on http://localhost:3000 with hot reload
```

### Dojo Frontend (Local Development)
```bash
cd frontend-dojo
# Serve with any static file server
python -m http.server 8080
# Or use nginx/apache
```

## 📁 Project Structure

```
refarch-python-customerorder/
├── frontend-react/           # Modern React app
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API client
│   │   ├── hooks/            # Custom hooks
│   │   └── types/            # TypeScript types
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
│
├── frontend-dojo/            # Classic Dojo app
│   ├── dojo/                 # Dojo Toolkit
│   ├── dojo_depot/           # Custom Dojo modules
│   ├── product/              # Product views
│   ├── cart/                 # Cart views
│   ├── auth-adapter.js       # JWT adapter
│   ├── login.html
│   ├── index.html
│   ├── Dockerfile
│   └── dojo-nginx.conf
│
└── app/                      # Python FastAPI backend
```

## 🎯 Which Frontend to Use?

### Choose React Frontend if you want:
- Modern development experience
- TypeScript type safety
- Better mobile support
- Faster load times
- Future-proof codebase
- Component reusability
- Better developer tools

### Choose Dojo Frontend if you want:
- Classic Web 2.0 experience
- Original application look & feel
- Familiarity with Dojo Toolkit
- Legacy browser support
- Tree/Grid enterprise widgets
- To compare with the JEE version

## 🐛 Troubleshooting

### React Frontend Not Loading
```bash
# Check if container is running
podman ps | grep frontend-react

# View logs
podman logs customerorder-frontend-react

# Rebuild
podman-compose build frontend-react
podman-compose up -d frontend-react
```

### Dojo Frontend Not Loading
```bash
# Check if container is running
podman ps | grep frontend-dojo

# View logs
podman logs customerorder-frontend-dojo

# Rebuild
podman-compose build frontend-dojo
podman-compose up -d frontend-dojo
```

### Both Frontends: API Connection Issues
Both frontends proxy API requests through nginx to the Python backend.

Check API is running:
```bash
curl http://localhost:8000/health
```

## 🎉 Enjoy Comparing!

You now have two complete frontends to compare:
1. **Modern React** - showcasing latest web development practices
2. **Classic Dojo** - preserving the original application experience

Both use the same Python FastAPI backend, demonstrating how a well-designed API can support multiple frontend technologies!

---

**Pro Tip:** Open both in side-by-side browser windows and perform the same actions to see how each handles the user experience!
