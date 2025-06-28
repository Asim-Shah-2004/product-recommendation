# 🚀 Bazaar Recommendation System

A sophisticated e-commerce recommendation engine built with Flask and MongoDB, featuring hybrid algorithms, real-time metrics, and intelligent user behavior analysis.

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Data Model](#data-model)
- [Derived Metrics](#derived-metrics)
- [Recommendation Algorithms](#recommendation-algorithms)
- [API Documentation](#api-documentation)
- [Setup & Installation](#setup--installation)
- [Usage Examples](#usage-examples)
- [Performance & Scalability](#performance--scalability)

## 🎯 Overview

The Bazaar Recommendation System is a comprehensive e-commerce recommendation engine that provides intelligent product and brand suggestions using:

- **Hybrid Recommendation Algorithms** (Content-based + Collaborative filtering)
- **Real-time Derived Metrics** (Trending, Engagement, Popularity, Quality scores)
- **Multi-dimensional User Profiling** (Behavior, preferences, demographics)
- **Advanced Scoring Systems** with weighted factors and diversity mechanisms

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph "Frontend/Client"
        A[Web App] --> B[Mobile App]
        A --> C[API Client]
    end
    
    subgraph "API Layer"
        D[Flask API] --> E[Recommendation Engine]
        E --> F[Algorithm Orchestrator]
    end
    
    subgraph "Data Layer"
        G[MongoDB] --> H[Users Collection]
        G --> I[Products Collection]
        G --> J[Stores Collection]
    end
    
    subgraph "Processing Layer"
        K[Metrics Calculator] --> L[User Behavior Analyzer]
        L --> M[Similarity Engine]
        M --> N[Scoring Engine]
    end
    
    B --> D
    C --> D
    F --> K
    K --> G
    N --> E
```

## 📊 Data Model

### User Schema
```mermaid
erDiagram
    USER {
        ObjectId _id
        string userName
        string userEmail
        string userPhone
        string userGender
        string userLocation
        int userAge
        string userOccupation
        string userIncome
        array userInterests
        object userPreferences
        object userEvents
        object userStats
    }
    
    USER_EVENTS {
        object storeClicks
        object productClicks
        array purchases
        array wishlist
        array searchHistory
    }
    
    USER_PREFERENCES {
        array preferredCategories
        array preferredBrands
        string budgetRange
        string shoppingFrequency
    }
    
    USER ||--|| USER_EVENTS : has
    USER ||--|| USER_PREFERENCES : has
```

### Store Schema
```mermaid
erDiagram
    STORE {
        ObjectId _id
        string storeName
        string storeTagline
        string storeOfficialUrl
        string storeImageUrl
        string category
        string subcategory
        string location
        float rating
        int totalReviews
        int foundedYear
        string description
        array specialties
        array brands
        array services
        object socialMedia
        object contactInfo
        int clickCount
        int viewCount
        int followerCount
        int productCount
        float trendingScore
        float engagementScore
        float popularityIndex
        float qualityScore
    }
    
    STORE ||--o{ PRODUCT : contains
```

### Product Schema
```mermaid
erDiagram
    PRODUCT {
        ObjectId _id
        string productName
        string productImageUrl
        string productDescription
        int productCost
        string productUrl
        ObjectId productStoreId
        string category
        string subcategory
        string brand
        float rating
        int totalReviews
        boolean inStock
        int discountPercentage
        int originalPrice
        array tags
        array features
        object specifications
        int clickCount
        int viewCount
        int purchaseCount
        int wishlistCount
        float trendingScore
        float engagementScore
        float popularityIndex
        float qualityScore
    }
    
    PRODUCT }o--|| STORE : belongs_to
```

## 📈 Derived Metrics

### 1. Trending Score Algorithm

The trending score measures how popular and relevant an item is currently.

```mermaid
flowchart TD
    A[Input Metrics] --> B[CTR Score]
    A --> C[Conversion Score]
    A --> D[Wishlist Score]
    A --> E[Rating Score]
    A --> F[Review Score]
    
    B --> G[CTR = clicks/views]
    C --> H[Conversion = purchases/clicks]
    D --> I[Wishlist = wishlist/views]
    E --> J[Rating = rating/5.0]
    F --> K[Review = min(reviews/1000, 1.0)]
    
    G --> L[Weight: 25%]
    H --> M[Weight: 30%]
    I --> N[Weight: 15%]
    J --> O[Weight: 20%]
    K --> P[Weight: 10%]
    
    L --> Q[Final Trending Score]
    M --> Q
    N --> Q
    O --> Q
    P --> Q
```

**Formula:**
```
Trending Score = (CTR × 0.25) + (Conversion × 0.30) + (Wishlist × 0.15) + (Rating × 0.20) + (Review × 0.10)
```

### 2. Engagement Score Algorithm

Measures the depth and quality of user interactions.

```mermaid
flowchart TD
    A[User Interactions] --> B[Interaction Rate]
    A --> C[Completion Rate]
    A --> D[Social Score]
    
    B --> E[interactions/views]
    C --> F[completions/clicks]
    D --> G[follower_count/10000]
    
    E --> H[Weight: 40%]
    F --> I[Weight: 40%]
    G --> J[Weight: 20%]
    
    H --> K[Final Engagement Score]
    I --> K
    J --> K
```

**Formula:**
```
Engagement Score = (Interaction Rate × 0.40) + (Completion Rate × 0.40) + (Social Score × 0.20)
```

### 3. Popularity Index Algorithm

Measures overall visibility and reach across the platform.

```mermaid
flowchart TD
    A[Reach Metrics] --> B[Total Reach]
    A --> C[Total Engagement]
    A --> D[Scale Factor]
    
    B --> E[views + followers]
    C --> F[clicks + purchases]
    D --> G[product_count/500]
    
    E --> H[Reach Score]
    F --> I[Engagement Score]
    G --> J[Scale Factor]
    
    H --> K[Weight: 50%]
    I --> L[Weight: 40%]
    J --> M[Weight: 10%]
    
    K --> N[Final Popularity Index]
    L --> N
    M --> N
```

**Formula:**
```
Popularity Index = (Reach Score × 0.50) + (Engagement Score × 0.40) + (Scale Factor × 0.10)
```

### 4. Quality Score Algorithm

Measures user satisfaction and value perception.

```mermaid
flowchart TD
    A[Quality Metrics] --> B[Rating Score]
    A --> C[Satisfaction Rate]
    A --> D[Value Score]
    
    B --> E[rating × review_credibility]
    C --> F[purchases/total_interest]
    D --> G[1 - discount_percentage/100]
    
    E --> H[Weight: 50%]
    F --> I[Weight: 30%]
    G --> J[Weight: 20%]
    
    H --> K[Final Quality Score]
    I --> K
    J --> K
```

**Formula:**
```
Quality Score = (Rating Score × 0.50) + (Satisfaction Rate × 0.30) + (Value Score × 0.20)
```

## 🧠 Recommendation Algorithms

### Brand Recommendation Algorithm

```mermaid
flowchart TD
    A[User Input] --> B[Get User Data]
    B --> C[Calculate User Preference Score]
    B --> D[Calculate Store Relevance Score]
    
    C --> E[Direct Interaction: 40%]
    C --> F[Purchase History: 30%]
    C --> G[Category Match: 20%]
    C --> H[Location Match: 10%]
    
    D --> I[Performance Metrics: 40%]
    D --> J[Budget Alignment: 35%]
    D --> K[Reputation: 25%]
    
    E --> L[User Preference Score]
    F --> L
    G --> L
    H --> L
    
    I --> M[Store Relevance Score]
    J --> M
    K --> M
    
    L --> N[Content-based Score]
    M --> N
    
    N --> O[Add Diversity Factor]
    O --> P[Final Score]
    
    P --> Q[Sort by Score]
    Q --> R[Add Collaborative Filtering]
    R --> S[Return Top Recommendations]
```

**Scoring Breakdown:**
- **User Preference Score (60% weight)**
  - Direct Interaction: 40% (store clicks, purchases)
  - Category Preference: 20% (interest matching)
  - Location Preference: 10% (geographic proximity)
- **Store Relevance Score (40% weight)**
  - Performance Metrics: 40% (trending, engagement, popularity, quality)
  - Budget Alignment: 35% (price range matching)
  - Reputation: 25% (rating and review credibility)

### Product Recommendation Algorithm

```mermaid
flowchart TD
    A[User Input] --> B[Get User Data & Events]
    B --> C[Filter by Brand if specified]
    
    C --> D[Calculate Product Relevance Score]
    
    D --> E[User Interaction: 35%]
    D --> F[Performance Metrics: 30%]
    D --> G[Price & Discount: 20%]
    D --> H[Category & Brand: 15%]
    
    E --> I[Product Clicks: 50%]
    E --> J[Wishlist: 30%]
    E --> K[Purchase History: 20%]
    
    F --> L[Trending Score]
    F --> M[Engagement Score]
    F --> N[Popularity Index]
    F --> O[Quality Score]
    
    G --> P[Budget Match]
    G --> Q[Discount Bonus]
    
    H --> R[Category Match]
    H --> S[Brand Preference]
    
    I --> T[Product Relevance Score]
    J --> T
    K --> T
    L --> T
    M --> T
    N --> T
    O --> T
    P --> T
    Q --> T
    R --> T
    S --> T
    
    T --> U[Add Recency Factor]
    U --> V[Add Diversity Factor]
    V --> W[Final Score]
    
    W --> X[Sort by Score]
    X --> Y[Add Collaborative Filtering]
    Y --> Z[Return Top Recommendations]
```

**Scoring Breakdown:**
- **User Interaction Score (35% weight)**
  - Product Clicks: 50% (direct interest)
  - Wishlist: 30% (intent to purchase)
  - Purchase History: 20% (past behavior)
- **Product Performance Metrics (30% weight)**
  - Trending Score: Current popularity
  - Engagement Score: Interaction depth
  - Popularity Index: Overall visibility
  - Quality Score: User satisfaction
- **Price and Discount Relevance (20% weight)**
  - Budget Match: Price range alignment
  - Discount Bonus: Value perception
- **Category and Brand Alignment (15% weight)**
  - Category Match: Interest alignment
  - Brand Preference: Specific brand filtering

### Collaborative Filtering Process

```mermaid
flowchart TD
    A[Target User] --> B[Find Similar Users]
    B --> C[Same Interests]
    B --> D[Similar Behavior Patterns]
    
    C --> E[Get Similar User Events]
    D --> E
    
    E --> F[Extract Interactions]
    F --> G[Filter Out User's Existing Interactions]
    
    G --> H[Score by Interaction Count]
    H --> I[Sort by Score]
    I --> J[Return Top Items]
    
    J --> K[Add to Recommendations]
    K --> L[Fallback Mechanism]
```

## 🔗 API Documentation

### Base URL
```
http://localhost:5000
```

### 1. Brand Recommendations

**Endpoint:** `POST /recommend/brands`

**Description:** Get personalized brand/store recommendations based on user behavior and preferences.

**Request Body:**
```json
{
    "user_id": "507f1f77bcf86cd799439011",
    "number": 10
}
```

**Parameters:**
- `user_id` (required): MongoDB ObjectId of the user
- `number` (optional): Number of recommendations to return (default: 10)

**Response:**
```json
{
    "status": "success",
    "user_id": "507f1f77bcf86cd799439011",
    "recommendations_count": 10,
    "algorithm": "Hybrid (Content-based + Collaborative)",
    "recommendations": [
        {
            "store_id": "507f1f77bcf86cd799439012",
            "store_name": "TechHub Store 1",
            "store_tagline": "Quality products for everyone - Store 1",
            "category": "electronics",
            "location": "Mumbai, Maharashtra",
            "rating": 4.5,
            "total_reviews": 500,
            "trending_score": 0.85,
            "engagement_score": 0.72,
            "popularity_index": 0.68,
            "quality_score": 0.91,
            "recommendation_score": 0.823,
            "score_breakdown": {
                "user_preference_score": 0.75,
                "store_relevance_score": 0.92
            }
        }
    ]
}
```

### 2. Product Recommendations

**Endpoint:** `POST /recommend/products`

**Description:** Get personalized product recommendations, optionally filtered by brand.

**Request Body:**
```json
{
    "user_id": "507f1f77bcf86cd799439011",
    "brand_id": "507f1f77bcf86cd799439012",
    "number": 10
}
```

**Parameters:**
- `user_id` (required): MongoDB ObjectId of the user
- `brand_id` (optional): MongoDB ObjectId of the brand/store to filter by
- `number` (optional): Number of recommendations to return (default: 10)

**Response:**
```json
{
    "status": "success",
    "user_id": "507f1f77bcf86cd799439011",
    "brand_id": "507f1f77bcf86cd799439012",
    "recommendations_count": 10,
    "algorithm": "Hybrid (Content-based + Collaborative + Multi-metric)",
    "recommendations": [
        {
            "product_id": "507f1f77bcf86cd799439013",
            "product_name": "Smartphone 1",
            "product_description": "High-quality smartphone with amazing features.",
            "product_cost": 25000,
            "store_id": "507f1f77bcf86cd799439012",
            "category": "electronics",
            "brand": "TechHub",
            "rating": 4.3,
            "total_reviews": 150,
            "discount_percentage": 15,
            "in_stock": true,
            "trending_score": 0.78,
            "engagement_score": 0.65,
            "popularity_index": 0.72,
            "quality_score": 0.85,
            "recommendation_score": 0.756,
            "relevance_score": 0.743
        }
    ]
}
```

### 3. Health Check

**Endpoint:** `GET /api/health`

**Description:** Check API and database connectivity.

**Response:**
```json
{
    "status": "healthy",
    "message": "Flask app is running with MongoDB connection",
    "database": "connected",
    "timestamp": "2024-01-15T10:30:00.000Z"
}
```

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- MongoDB (local or cloud)
- pip package manager

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd baazar-recommendation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure MongoDB connection**
   Update the `MONGO_URI` in `app.py` and `data_ingestor_cli.py`:
   ```python
   MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/database"
   ```

4. **Populate database with sample data**
   ```bash
   python data_ingestor_cli.py
   ```

5. **Start the Flask server**
   ```bash
   python app.py
   ```

6. **Test the API**
   ```bash
   python test_recommendations.py
   ```

## 📝 Usage Examples

### Using cURL

#### Brand Recommendations
```bash
curl -X POST http://localhost:5000/recommend/brands \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "507f1f77bcf86cd799439011",
       "number": 5
     }'
```

#### Product Recommendations (General)
```bash
curl -X POST http://localhost:5000/recommend/products \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "507f1f77bcf86cd799439011",
       "number": 5
     }'
```

#### Product Recommendations (Brand-Specific)
```bash
curl -X POST http://localhost:5000/recommend/products \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "507f1f77bcf86cd799439011",
       "brand_id": "507f1f77bcf86cd799439012",
       "number": 5
     }'
```

### Using Python

```python
import requests

# Brand recommendations
response = requests.post('http://localhost:5000/recommend/brands', json={
    'user_id': '507f1f77bcf86cd799439011',
    'number': 5
})

# Product recommendations
response = requests.post('http://localhost:5000/recommend/products', json={
    'user_id': '507f1f77bcf86cd799439011',
    'brand_id': '507f1f77bcf86cd799439012',  # Optional
    'number': 5
})

data = response.json()
print(f"Found {data['recommendations_count']} recommendations")
```

### Using Postman

1. **Set Method:** POST
2. **Set URL:** `http://localhost:5000/recommend/brands` or `http://localhost:5000/recommend/products`
3. **Set Headers:** `Content-Type: application/json`
4. **Set Body (raw JSON):**
   ```json
   {
       "user_id": "507f1f77bcf86cd799439011",
       "number": 5
   }
   ```

## ⚡ Performance & Scalability

### Performance Features

```mermaid
graph LR
    A[Request] --> B[Load Balancer]
    B --> C[API Server 1]
    B --> D[API Server 2]
    B --> E[API Server N]
    
    C --> F[MongoDB Primary]
    D --> F
    E --> F
    
    F --> G[MongoDB Secondary 1]
    F --> H[MongoDB Secondary 2]
    
    I[Redis Cache] --> C
    I --> D
    I --> E
```

### Optimization Strategies

1. **Database Indexing**
   - Compound indexes on user_id + category
   - Indexes on derived metrics for fast sorting
   - Geospatial indexes for location-based queries

2. **Caching Strategy**
   - Redis for frequently accessed user preferences
   - Cache derived metrics for 1 hour
   - Cache collaborative filtering results

3. **Algorithm Optimization**
   - Lazy loading of user events
   - Batch processing for similar users
   - Parallel computation of derived metrics

### Scalability Considerations

- **Horizontal Scaling**: Multiple API instances behind load balancer
- **Database Sharding**: Shard by user_id for large datasets
- **CDN Integration**: Cache static content and API responses
- **Microservices**: Split recommendation engine into separate services

## 🔍 Error Handling

The API includes comprehensive error handling:

```mermaid
flowchart TD
    A[API Request] --> B{Valid User ID?}
    B -->|No| C[400 Bad Request]
    B -->|Yes| D{User Exists?}
    D -->|No| E[404 User Not Found]
    D -->|Yes| F{Valid Parameters?}
    F -->|No| G[400 Invalid Parameters]
    F -->|Yes| H[Process Request]
    H --> I{Database Error?}
    I -->|Yes| J[500 Internal Server Error]
    I -->|No| K[200 Success Response]
```

### Common Error Responses

```json
{
    "error": "user_id is required"
}
```

```json
{
    "error": "User not found"
}
```

```json
{
    "error": "Invalid user_id format"
}
```

## 📊 Monitoring & Analytics

### Key Metrics to Monitor

1. **API Performance**
   - Response time (target: <200ms)
   - Throughput (requests/second)
   - Error rate

2. **Recommendation Quality**
   - Click-through rate on recommendations
   - Conversion rate from recommendations
   - User satisfaction scores

3. **System Health**
   - Database connection status
   - Memory usage
   - CPU utilization

### Logging Strategy

```python
# Example logging configuration
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('recommendation_api.log'),
        logging.StreamHandler()
    ]
)
```

## 🚀 Future Enhancements

1. **Machine Learning Integration**
   - TensorFlow/PyTorch for deep learning models
   - A/B testing framework for algorithm comparison
   - Real-time model updates

2. **Advanced Features**
   - Seasonal recommendations
   - Cross-selling suggestions
   - Inventory-aware recommendations

3. **Performance Improvements**
   - GraphQL API for flexible queries
   - WebSocket for real-time updates
   - Edge computing for faster responses

---

## 📞 Support

For questions, issues, or contributions:

1. Check the [API Documentation](RECOMMENDATION_API.md)
2. Run the test suite: `python test_recommendations.py`
3. Review the logs for debugging information
4. Open an issue with detailed error information

---

**Built with ❤️ using Flask, MongoDB, and advanced recommendation algorithms** 