from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import os
from datetime import datetime, timedelta
import random
import json
import math
from collections import defaultdict, Counter

app = Flask(__name__)

# MongoDB Connection
MONGO_URI = "mongodb+srv://bazaar:bazaar123@cluster-1.o2duhip.mongodb.net/bazaar"
client = MongoClient(MONGO_URI)
db = client.bazaar

# Collections
users_collection = db.users
products_collection = db.products
stores_collection = db.stores
brands_collection = db.brands

@app.route('/')
def index():
    return jsonify({
        "message": "Bazaar Recommendation API",
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "users": "/api/users",
            "products": "/api/products", 
            "stores": "/api/stores",
            "brand_recommendations": "/recommend/brands",
            "product_recommendations": "/recommend/products"
        }
    })

@app.route('/api/health')
def health_check():
    try:
        # Test MongoDB connection
        client.admin.command('ping')
        return jsonify({
            'status': 'healthy',
            'message': 'Flask app is running with MongoDB connection',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': f'Database connection failed: {str(e)}',
            'database': 'disconnected'
        }), 500

@app.route('/api/users')
def get_users():
    try:
        users = list(users_collection.find({}, {'_id': 0}))
        return jsonify({
            'status': 'success',
            'count': len(users),
            'users': users
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products')
def get_products():
    try:
        products = list(products_collection.find({}, {'_id': 0}))
        return jsonify({
            'status': 'success',
            'count': len(products),
            'products': products
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stores')
def get_stores():
    try:
        stores = list(stores_collection.find({}, {'_id': 0}))
        return jsonify({
            'status': 'success',
            'count': len(stores),
            'stores': stores
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_user_preference_score(user, store, user_events):
    """Calculate user preference score for a store based on various factors."""
    score = 0.0
    
    # 1. Direct interaction score (40% weight)
    store_id_str = str(store['_id'])
    store_clicks = user_events.get('storeClicks', {}).get(store_id_str, 0)
    click_score = min(store_clicks / 100.0, 1.0) * 0.4
    score += click_score
    
    # 2. Purchase history score (30% weight)
    purchases = user_events.get('purchases', [])
    store_purchases = sum(1 for purchase in purchases if str(purchase.get('storeId')) == store_id_str)
    purchase_score = min(store_purchases / 10.0, 1.0) * 0.3
    score += purchase_score
    
    # 3. Category preference score (20% weight)
    user_interests = user.get('interests', [])
    store_category = store.get('category', '').lower()
    category_match = 1.0 if store_category in [interest.lower() for interest in user_interests] else 0.0
    score += category_match * 0.2
    
    # 4. Location preference score (10% weight)
    user_location = user.get('location', '').lower()
    store_location = store.get('location', '').lower()
    location_match = 0.5 if any(city in user_location for city in store_location.split(',')) else 0.0
    score += location_match * 0.1
    
    return score

def calculate_store_relevance_score(store, user_preferences):
    """Calculate store relevance score based on store metrics and user preferences."""
    score = 0.0
    
    # 1. Store performance metrics (40% weight)
    trending_score = store.get('trendingScore', 0.0)
    engagement_score = store.get('engagementScore', 0.0)
    popularity_index = store.get('popularityIndex', 0.0)
    quality_score = store.get('qualityScore', 0.0)
    
    performance_score = (trending_score + engagement_score + popularity_index + quality_score) / 4.0
    score += performance_score * 0.4
    
    # 2. User preference alignment (35% weight)
    user_budget = user_preferences.get('budgetRange', 'Medium')
    store_avg_price = store.get('averagePrice', 15000)  # Default average
    
    budget_scores = {
        '1000-5000': (0, 10000),
        '5000-15000': (5000, 20000),
        '15000-30000': (15000, 35000),
        '30000+': (25000, float('inf'))
    }
    
    min_price, max_price = budget_scores.get(user_budget, (0, 20000))
    price_match = 1.0 if min_price <= store_avg_price <= max_price else 0.5
    score += price_match * 0.35
    
    # 3. Store reputation (25% weight)
    rating = store.get('rating', 3.5)
    total_reviews = store.get('totalReviews', 0)
    review_credibility = min(total_reviews / 1000.0, 1.0)
    reputation_score = (rating / 5.0) * review_credibility
    score += reputation_score * 0.25
    
    return score

def calculate_product_relevance_score(product, user_events, user_preferences, brand_id=None):
    """Calculate product relevance score using complex algorithm."""
    score = 0.0
    
    # 1. User interaction score (35% weight)
    product_id_str = str(product['_id'])
    product_clicks = user_events.get('productClicks', {}).get(product_id_str, 0)
    wishlist_count = len([p for p in user_events.get('wishlist', []) if str(p) == product_id_str])
    purchases = [p for p in user_events.get('purchases', []) if str(p.get('productId')) == product_id_str]
    
    interaction_score = (
        min(product_clicks / 50.0, 1.0) * 0.5 +
        min(wishlist_count, 1.0) * 0.3 +
        min(len(purchases), 1.0) * 0.2
    )
    score += interaction_score * 0.35
    
    # 2. Product performance metrics (30% weight)
    trending_score = product.get('trendingScore', 0.0)
    engagement_score = product.get('engagementScore', 0.0)
    popularity_index = product.get('popularityIndex', 0.0)
    quality_score = product.get('qualityScore', 0.0)
    
    performance_score = (trending_score + engagement_score + popularity_index + quality_score) / 4.0
    score += performance_score * 0.30
    
    # 3. Price and discount relevance (20% weight)
    user_budget = user_preferences.get('budgetRange', 'Medium')
    product_cost = product.get('productCost', 0)
    discount_percentage = product.get('discountPercentage', 0)
    
    budget_scores = {
        '1000-5000': (0, 5000),
        '5000-15000': (3000, 15000),
        '15000-30000': (10000, 30000),
        '30000+': (20000, float('inf'))
    }
    
    min_price, max_price = budget_scores.get(user_budget, (0, 15000))
    price_match = 1.0 if min_price <= product_cost <= max_price else 0.3
    
    # Discount bonus (higher discount = higher score for budget-conscious users)
    discount_bonus = min(discount_percentage / 50.0, 0.3) if user_budget in ['1000-5000', '5000-15000'] else 0.0
    
    price_score = price_match + discount_bonus
    score += price_score * 0.20
    
    # 4. Category and brand alignment (15% weight)
    user_interests = user_preferences.get('interests', [])
    product_category = product.get('category', '').lower()
    product_brand = product.get('brand', '').lower()
    
    category_match = 1.0 if product_category in [interest.lower() for interest in user_interests] else 0.0
    brand_match = 1.0 if brand_id and str(product.get('productStoreId')) == str(brand_id) else 0.5
    
    alignment_score = (category_match * 0.7 + brand_match * 0.3)
    score += alignment_score * 0.15
    
    return score

def get_collaborative_recommendations(user_id, collection_type, limit=10):
    """Get collaborative filtering recommendations based on similar users."""
    try:
        # Find users with similar behavior patterns
        user = users_collection.find_one({'_id': user_id})
        if not user:
            return []
        
        user_events = user.get('userEvents', {})
        user_interests = user.get('interests', [])
        
        # Find similar users based on interests and behavior
        similar_users = users_collection.find({
            '_id': {'$ne': user_id},
            'interests': {'$in': user_interests}
        }).limit(20)
        
        recommendations = []
        
        for similar_user in similar_users:
            similar_events = similar_user.get('userEvents', {})
            
            if collection_type == 'stores':
                # Get stores that similar users interacted with
                similar_store_clicks = similar_events.get('storeClicks', {})
                for store_id_str, click_count in similar_store_clicks.items():
                    if store_id_str not in user_events.get('storeClicks', {}):
                        store = stores_collection.find_one({'_id': ObjectId(store_id_str)})
                        if store:
                            recommendations.append({
                                'item': store,
                                'score': click_count,
                                'source': 'collaborative'
                            })
            
            elif collection_type == 'products':
                # Get products that similar users interacted with
                similar_product_clicks = similar_events.get('productClicks', {})
                for product_id_str, click_count in similar_product_clicks.items():
                    if product_id_str not in user_events.get('productClicks', {}):
                        product = products_collection.find_one({'_id': ObjectId(product_id_str)})
                        if product:
                            recommendations.append({
                                'item': product,
                                'score': click_count,
                                'source': 'collaborative'
                            })
        
        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return [rec['item'] for rec in recommendations[:limit]]
        
    except Exception as e:
        print(f"Collaborative filtering error: {e}")
        return []

@app.route('/recommend/brands', methods=['POST'])
def recommend_brands():
    """Recommend brands/stores based on user behavior and preferences."""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        number = data.get('number', 10)
        
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        # Convert string ID to ObjectId
        try:
            user_id = ObjectId(user_id)
        except:
            return jsonify({'error': 'Invalid user_id format'}), 400
        
        # Get user data
        user = users_collection.find_one({'_id': user_id})
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user_events = user.get('userEvents', {})
        user_preferences = {
            'interests': user.get('interests', []),
            'budgetRange': user.get('budgetRange', 'Medium'),
            'location': user.get('location', '')
        }
        
        # Get all stores
        stores = list(stores_collection.find({}))
        
        # Calculate scores for each store
        store_scores = []
        for store in stores:
            # Content-based score
            user_preference_score = calculate_user_preference_score(user, store, user_events)
            store_relevance_score = calculate_store_relevance_score(store, user_preferences)
            
            # Combined score with weights
            content_score = (user_preference_score * 0.6 + store_relevance_score * 0.4)
            
            # Add some randomness for diversity
            diversity_factor = random.uniform(0.8, 1.2)
            final_score = content_score * diversity_factor
            
            store_scores.append({
                'store': store,
                'score': final_score,
                'user_preference_score': user_preference_score,
                'store_relevance_score': store_relevance_score
            })
        
        # Sort by score and get top recommendations
        store_scores.sort(key=lambda x: x['score'], reverse=True)
        top_stores = store_scores[:number]
        
        # Add collaborative filtering recommendations if needed
        if len(top_stores) < number:
            collaborative_stores = get_collaborative_recommendations(user_id, 'stores', number - len(top_stores))
            for store in collaborative_stores:
                top_stores.append({
                    'store': store,
                    'score': 0.5,  # Default collaborative score
                    'user_preference_score': 0.0,
                    'store_relevance_score': 0.5,
                    'source': 'collaborative'
                })
        
        # Format response
        recommendations = []
        for item in top_stores:
            store = item['store']
            recommendations.append({
                'store_id': str(store['_id']),
                'store_name': store['storeName'],
                'store_tagline': store['storeTagline'],
                'category': store['category'],
                'location': store['location'],
                'rating': store['rating'],
                'total_reviews': store['totalReviews'],
                'trending_score': store['trendingScore'],
                'engagement_score': store['engagementScore'],
                'popularity_index': store['popularityIndex'],
                'quality_score': store['qualityScore'],
                'recommendation_score': round(item['score'], 3),
                'score_breakdown': {
                    'user_preference_score': round(item['user_preference_score'], 3),
                    'store_relevance_score': round(item['store_relevance_score'], 3)
                }
            })
        
        return jsonify({
            'status': 'success',
            'user_id': str(user_id),
            'recommendations_count': len(recommendations),
            'algorithm': 'Hybrid (Content-based + Collaborative)',
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommend/products', methods=['POST'])
def recommend_products():
    """Recommend products based on user behavior, brand preference, and various metrics."""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        brand_id = data.get('brand_id')  # Optional: filter by specific brand/store
        number = data.get('number', 10)
        
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        # Convert string IDs to ObjectId
        try:
            user_id = ObjectId(user_id)
            if brand_id:
                brand_id = ObjectId(brand_id)
        except:
            return jsonify({'error': 'Invalid ID format'}), 400
        
        # Get user data
        user = users_collection.find_one({'_id': user_id})
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user_events = user.get('userEvents', {})
        user_preferences = {
            'interests': user.get('interests', []),
            'budgetRange': user.get('budgetRange', 'Medium'),
            'location': user.get('location', '')
        }
        
        # Build query for products
        query = {}
        if brand_id:
            query['productStoreId'] = brand_id
        
        # Get products
        products = list(products_collection.find(query))
        
        if not products:
            return jsonify({
                'status': 'success',
                'user_id': str(user_id),
                'brand_id': str(brand_id) if brand_id else None,
                'recommendations_count': 0,
                'message': 'No products found for the specified criteria'
            })
        
        # Calculate scores for each product
        product_scores = []
        for product in products:
            # Content-based score
            product_relevance_score = calculate_product_relevance_score(
                product, user_events, user_preferences, brand_id
            )
            
            # Add recency factor (newer products get slight boost)
            recency_factor = 1.0  # Could be enhanced with product creation date
            
            # Add diversity factor
            diversity_factor = random.uniform(0.9, 1.1)
            
            final_score = product_relevance_score * recency_factor * diversity_factor
            
            product_scores.append({
                'product': product,
                'score': final_score,
                'relevance_score': product_relevance_score
            })
        
        # Sort by score and get top recommendations
        product_scores.sort(key=lambda x: x['score'], reverse=True)
        top_products = product_scores[:number]
        
        # Add collaborative filtering recommendations if needed
        if len(top_products) < number:
            collaborative_products = get_collaborative_recommendations(user_id, 'products', number - len(top_products))
            for product in collaborative_products:
                if brand_id is None or str(product.get('productStoreId')) == str(brand_id):
                    top_products.append({
                        'product': product,
                        'score': 0.4,  # Default collaborative score
                        'relevance_score': 0.4,
                        'source': 'collaborative'
                    })
        
        # Format response
        recommendations = []
        for item in top_products:
            product = item['product']
            recommendations.append({
                'product_id': str(product['_id']),
                'product_name': product['productName'],
                'product_description': product['productDescription'],
                'product_cost': product['productCost'],
                'store_id': str(product['productStoreId']),
                'category': product['category'],
                'brand': product['brand'],
                'rating': product['rating'],
                'total_reviews': product['totalReviews'],
                'discount_percentage': product['discountPercentage'],
                'in_stock': product['inStock'],
                'trending_score': product['trendingScore'],
                'engagement_score': product['engagementScore'],
                'popularity_index': product['popularityIndex'],
                'quality_score': product['qualityScore'],
                'recommendation_score': round(item['score'], 3),
                'relevance_score': round(item['relevance_score'], 3)
            })
        
        return jsonify({
            'status': 'success',
            'user_id': str(user_id),
            'brand_id': str(brand_id) if brand_id else None,
            'recommendations_count': len(recommendations),
            'algorithm': 'Hybrid (Content-based + Collaborative + Multi-metric)',
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 