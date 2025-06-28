# 🚀 Bazaar Recommendation API

A sophisticated recommendation system with hybrid algorithms for brand and product recommendations.

## 📋 Overview

The Bazaar Recommendation API provides intelligent recommendations using a combination of:
- **Content-based filtering** based on user preferences and behavior
- **Collaborative filtering** based on similar users
- **Multi-metric scoring** using derived metrics (trending, engagement, popularity, quality)

## 🔗 API Endpoints

### 1. Brand/Store Recommendations
**Endpoint:** `POST /recommend/brands`

**Purpose:** Recommend brands/stores based on user behavior and preferences.

**Request Body:**
```json
{
    "user_id": "507f1f77bcf86cd799439011",
    "number": 10
}
```

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

**Purpose:** Recommend products based on user behavior, brand preference, and various metrics.

**Request Body:**
```json
{
    "user_id": "507f1f77bcf86cd799439011",
    "brand_id": "507f1f77bcf86cd799439012",  // Optional
    "number": 10
}
```

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

## 🧠 Algorithm Details

### Brand Recommendation Algorithm

#### 1. User Preference Score (60% weight)
- **Direct Interaction (40%)**: Store clicks and purchase history
- **Category Preference (20%)**: Match with user interests
- **Location Preference (10%)**: Geographic proximity

#### 2. Store Relevance Score (40% weight)
- **Performance Metrics (40%)**: Trending, engagement, popularity, quality scores
- **Budget Alignment (35%)**: Match with user's budget range
- **Reputation (25%)**: Rating and review credibility

#### 3. Collaborative Filtering
- Finds users with similar interests and behavior patterns
- Recommends stores that similar users interacted with
- Used as fallback when content-based recommendations are insufficient

### Product Recommendation Algorithm

#### 1. User Interaction Score (35% weight)
- **Product Clicks (50%)**: Direct user interest
- **Wishlist (30%)**: Intent to purchase
- **Purchase History (20%)**: Past buying behavior

#### 2. Product Performance Metrics (30% weight)
- **Trending Score**: Current popularity and momentum
- **Engagement Score**: User interaction depth
- **Popularity Index**: Overall visibility and reach
- **Quality Score**: User satisfaction and value perception

#### 3. Price and Discount Relevance (20% weight)
- **Budget Match**: Aligns with user's budget range
- **Discount Bonus**: Higher discounts for budget-conscious users
- **Value Perception**: Price-to-quality ratio

#### 4. Category and Brand Alignment (15% weight)
- **Category Match**: Aligns with user interests
- **Brand Preference**: Specific brand/store filtering

## 📊 Derived Metrics

### Trending Score
```
CTR Score (25%) + Conversion Score (30%) + Wishlist Score (15%) + Rating Score (20%) + Review Score (10%)
```

### Engagement Score
```
Interaction Rate (40%) + Completion Rate (40%) + Social Score (20%)
```

### Popularity Index
```
Reach Score (50%) + Engagement Score (40%) + Scale Factor (10%)
```

### Quality Score
```
Rating Score (50%) + Satisfaction Rate (30%) + Value Score (20%)
```

## 🚀 Usage Examples

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

## 🧪 Testing

Run the test script to verify the API functionality:

```bash
python test_recommendations.py
```

This will:
1. Test API health
2. Test brand recommendations
3. Test general product recommendations
4. Test brand-specific product recommendations

## 🔧 Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Populate database with sample data:**
   ```bash
   python data_ingestor_cli.py
   ```

3. **Start the Flask server:**
   ```bash
   python app.py
   ```

4. **Test the API:**
   ```bash
   python test_recommendations.py
   ```

## 📈 Performance Features

- **Hybrid Algorithm**: Combines multiple recommendation approaches
- **Real-time Scoring**: Calculates scores based on current metrics
- **Diversity Factor**: Adds randomness to prevent filter bubbles
- **Fallback Mechanisms**: Uses collaborative filtering when content-based fails
- **Scalable Design**: Efficient MongoDB queries and indexing

## 🎯 Key Benefits

1. **Personalized Recommendations**: Based on individual user behavior
2. **Multi-dimensional Scoring**: Considers various factors and metrics
3. **Flexible Filtering**: Can filter by specific brands or categories
4. **Real-time Updates**: Recommendations adapt to changing user behavior
5. **Comprehensive Metrics**: Uses derived metrics for better accuracy

## 🔍 Error Handling

The API includes comprehensive error handling for:
- Invalid user IDs
- Missing required parameters
- Database connection issues
- Empty result sets
- Invalid data formats

All errors return appropriate HTTP status codes and descriptive error messages. 