# 🚀 Quick Start - Compare Both Frontends!

The Customer Order Services app is **running with 2 web frontends** you can compare!

## 🌐 Open Both Frontends

### 1. Modern React Frontend
**Open:** http://localhost:3000

Modern, responsive UI with:
- Beautiful gradient design
- Real-time cart updates
- Smooth animations
- Mobile-friendly

### 2. Classic Dojo Frontend
**Open:** http://localhost:3001

Original Web 2.0 interface with:
- Tab-based navigation
- Tree widget cart
- DataGrid product catalog
- Classic enterprise look

## 🔑 Login to Both

**Credentials (same for both):**
- Username: `rbarcia`
- Password: `b0wfish`

## 🛍️ Try the Shopping Flow

### In React Frontend (Port 3000)
1. Click **Shop** in nav bar
2. Browse categories in left sidebar
3. Click **Add to Cart** on products
4. Watch cart update in right sidebar
5. Click **Cart** in nav bar
6. Click **Submit Order** button
7. View in **Orders** tab

### In Dojo Frontend (Port 3001)
1. Click **Shop** tab
2. Choose category from menu
3. Click product row to see details
4. Drag product to cart tree (or use dialog)
5. Click **Cart** tab
6. Click submit order
7. Check **Order History** tab

## 📊 Side-by-Side Comparison

**Try this:**
1. Open both URLs in separate browser windows
2. Arrange them side-by-side
3. Login to both
4. Perform the same actions in each
5. Compare the user experience!

## 🎨 What to Compare

| Aspect | React | Dojo |
|--------|-------|------|
| **Login** | Modern gradient screen | Simple login page |
| **Navigation** | Top nav bar | Tabbed interface |
| **Product Grid** | Cards with images | DataGrid rows |
| **Categories** | Left sidebar | Dropdown menu |
| **Cart Preview** | Right sidebar | Tree widget |
| **Add to Cart** | Button click | Drag & drop |
| **Checkout** | Dedicated cart page | Cart tab |
| **Mobile** | Fully responsive | Desktop only |

## 🔧 Stop/Start Services

```bash
# Stop all
podman-compose down

# Start all
podman-compose up -d

# Restart just frontends
podman-compose restart frontend-react frontend-dojo

# View logs
podman logs customerorder-frontend-react
podman logs customerorder-frontend-dojo
```

## 📚 More Information

- **[FRONTENDS.md](FRONTENDS.md)** - Detailed frontend comparison
- **[RUNNING.md](RUNNING.md)** - Live API testing guide
- **[README.md](README.md)** - Complete project documentation

---

## ✨ The Point

This demonstrates how a **well-designed REST API** can support multiple frontend technologies:
- Same backend serves both frontends
- Same authentication system
- Same business logic
- Different user experiences

Choose the frontend that fits your use case, or build your own! 🚀
