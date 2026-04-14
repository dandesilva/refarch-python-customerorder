# Fixing Runtime Errors

## Error 1: React Frontend - Missing Product Images

**Symptoms:**
- React frontend couldn't display images for catalog items
- Image references in database pointed to non-existent files

**Root Causes:**
1. Images existed only in `frontend-dojo/images/` directory
2. React frontend had empty `public/images/` directory
3. Database seed data used placeholder filenames (`laptop1.jpg`, `desktop1.jpg`) that didn't match actual image files

**Solutions:**
1. Created `frontend-react/public/images/` directory
2. Copied all product images from Dojo frontend to React frontend (22 image files)
3. Updated seed data in `alembic/versions/001_initial_schema.py`:
   - Replaced placeholder names with actual image filenames (PS3.jpg, SonyTV.jpg, etc.)
   - Expanded catalog from 5 to 10 products with real images
   - Added Gaming and Movies categories
   - Fixed NULL handling in SQL INSERT statements

---

## Error 2: Dojo Frontend - "Sorry an error occurred"

**Symptoms:**
- Classic Dojo frontend displayed error message instead of product catalog
- Category menu not loading
- Product grid empty

**Root Causes:**
1. **API Path Mismatch**: Dojo called `/jaxrs/*` endpoints, but Python backend served at `/api/v1/*`
2. **Category Response Format**: Backend returned flat category array, but Dojo expected nested structure with `subCategories` field
3. **Product Response Format**: Missing `id` field (Dojo used `idAttribute="id"`), only had `product_id`
4. **Price Data Type**: Dojo expected string, backend returned Decimal

**Solutions:**

### 2.1 Nginx Proxy Configuration
Updated `frontend-dojo/dojo-nginx.conf`:
```nginx
# Map /jaxrs/* to /api/v1/*
location /jaxrs/ {
    rewrite ^/jaxrs/(.*)$ /api/v1/$1 break;
    proxy_pass http://customerorder-app:8000;
}
```

### 2.2 Category Schema Changes
Updated `app/schemas/category.py`:
- Added `id` field as alias for `cat_id` (Dojo compatibility)
- Created `CategoryWithSubcategories` schema for nested structure
- Modified `app/api/routes/category.py` to return top-level categories with their subcategories included

### 2.3 Product Schema Changes
Updated `app/schemas/product.py`:
- Added `id` field alongside `product_id`
- Changed `price` from Decimal to string type
- Created custom `from_orm()` method to handle conversions
- Updated `app/api/routes/product.py` to use `ProductResponse.from_orm()`

---

## Error 3: React Frontend - Category Links Not Working

**Symptoms:**
- Category sidebar displayed but links didn't respond
- Clicking on subcategories didn't load products

**Root Cause:**
- React frontend expected flat array of categories
- API now returned nested structure (for Dojo compatibility)
- React code couldn't find subcategories in the nested format

**Solution:**
Updated `frontend-react/src/services/api.ts`:
```javascript
// Flatten nested category structure
const flatCategories: Category[] = [];
response.data.forEach((topCat: any) => {
  flatCategories.push({ cat_id, name, parent_cat_id });
  if (topCat.subCategories) {
    topCat.subCategories.forEach((subCat: any) => {
      flatCategories.push({ cat_id, name, parent_cat_id });
    });
  }
});
```

---

## Error 4: Dojo Frontend - Trailing Slash Redirect Issue

**Symptoms:**
- Dojo frontend still showed "error occurred" after previous fixes
- Network logs showed 307 redirect responses
- JsonRestStore couldn't load data

**Root Cause:**
- Dojo's `JsonRestStore` automatically appends trailing slash to requests: `/jaxrs/Product/?categoryId=2`
- FastAPI's default behavior redirects trailing slashes (307 Temporary Redirect)
- JsonRestStore didn't follow redirects, causing data load failure

**Solutions:**

### 4.1 FastAPI Configuration
Updated `app/main.py`:
```python
app = FastAPI(
    redirect_slashes=False,  # Disable automatic redirects
    # ... other config
)
```

### 4.2 Product Route Enhancement
Updated `app/api/routes/product.py`:
```python
@router.get("", response_model=List[ProductResponse])
@router.get("/", response_model=List[ProductResponse])  # Handle trailing slash
def get_products_by_category(...):
```

---

## Final Architecture

### API Compatibility Layer
- **Path Mapping**: `/jaxrs/*` → `/api/v1/*` (nginx rewrite)
- **Dual Field Support**: Both `id` and `product_id` in responses
- **Flexible Response Format**: Nested categories for Dojo, flattened client-side for React
- **Trailing Slash Handling**: Explicit routes for both variants

### Image Assets
- **Location**: Both frontends have images in `/public/images/` or `/images/`
- **Path Format**: `/images/PS3.jpg` (absolute paths from root)
- **Delivery**: Served by nginx from container filesystem

### Database Seed Data
- **10 Products** across 3 category hierarchies (Electronics, Home & Garden, Entertainment)
- **Actual image references** matching files in images directory
- **Subcategories**: Computers, Gaming, Movies, Furniture, Appliances

---

## Key Lessons

1. **Legacy Frontend Compatibility**: Modern Python backends can serve legacy Dojo applications with proper API adapters (nginx rewrites, dual field names, response format variations)

2. **Trailing Slash Handling**: Critical for REST stores - must handle both `/resource` and `/resource/` explicitly when working with frameworks that auto-append slashes

3. **Image Asset Management**: When porting between frontends, verify asset locations and update seed data paths to match actual filesystem

4. **Schema Evolution**: Adding compatibility fields (`id` alongside `product_id`) allows single backend to serve multiple frontend generations

5. **Type Conversions**: Legacy systems often expect strings where modern systems use typed fields (Decimal → string for prices)
