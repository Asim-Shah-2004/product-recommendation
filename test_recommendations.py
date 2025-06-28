#!/usr/bin/env python3
"""
Test script for the Bazaar Recommendation API endpoints
This script demonstrates how to use the recommendation endpoints
"""

import requests
import json
from pymongo import MongoClient
from bson import ObjectId

# API Configuration
API_BASE_URL = "http://localhost:5000"
MONGO_URI = "mongodb+srv://bazaar:bazaar123@cluster-1.o2duhip.mongodb.net/bazaar"

def get_sample_user_id():
    """Get a sample user ID from the database for testing."""
    try:
        client = MongoClient(MONGO_URI)
        db = client.bazaar
        user = db.users.find_one({})
        client.close()
        return str(user['_id']) if user else None
    except Exception as e:
        print(f"Error getting sample user: {e}")
        return None

def get_sample_store_id():
    """Get a sample store ID from the database for testing."""
    try:
        client = MongoClient(MONGO_URI)
        db = client.bazaar
        store = db.stores.find_one({})
        client.close()
        return str(store['_id']) if store else None
    except Exception as e:
        print(f"Error getting sample store: {e}")
        return None

def test_brand_recommendations():
    """Test the brand recommendation endpoint."""
    print("🔍 Testing Brand Recommendations...")
    print("=" * 50)
    
    user_id = get_sample_user_id()
    if not user_id:
        print("❌ No users found in database. Please run the data ingestor first.")
        return
    
    payload = {
        "user_id": user_id,
        "number": 5
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/recommend/brands", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {data['recommendations_count']} brand recommendations")
            print(f"📊 Algorithm: {data['algorithm']}")
            print(f"👤 User ID: {data['user_id']}")
            print("\n🏪 Top Brand Recommendations:")
            
            for i, rec in enumerate(data['recommendations'], 1):
                print(f"\n{i}. {rec['store_name']}")
                print(f"   📍 Location: {rec['location']}")
                print(f"   🏷️  Category: {rec['category']}")
                print(f"   ⭐ Rating: {rec['rating']} ({rec['total_reviews']} reviews)")
                print(f"   📈 Recommendation Score: {rec['recommendation_score']}")
                print(f"   📊 Metrics:")
                print(f"      - Trending Score: {rec['trending_score']}")
                print(f"      - Engagement Score: {rec['engagement_score']}")
                print(f"      - Popularity Index: {rec['popularity_index']}")
                print(f"      - Quality Score: {rec['quality_score']}")
                print(f"   🎯 Score Breakdown:")
                print(f"      - User Preference: {rec['score_breakdown']['user_preference_score']}")
                print(f"      - Store Relevance: {rec['score_breakdown']['store_relevance_score']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_product_recommendations():
    """Test the product recommendation endpoint."""
    print("\n🔍 Testing Product Recommendations...")
    print("=" * 50)
    
    user_id = get_sample_user_id()
    store_id = get_sample_store_id()
    
    if not user_id:
        print("❌ No users found in database. Please run the data ingestor first.")
        return
    
    # Test 1: General product recommendations
    print("\n📦 Test 1: General Product Recommendations")
    payload = {
        "user_id": user_id,
        "number": 5
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/recommend/products", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {data['recommendations_count']} product recommendations")
            print(f"📊 Algorithm: {data['algorithm']}")
            print(f"👤 User ID: {data['user_id']}")
            print("\n🛍️ Top Product Recommendations:")
            
            for i, rec in enumerate(data['recommendations'], 1):
                print(f"\n{i}. {rec['product_name']}")
                print(f"   💰 Price: ₹{rec['product_cost']}")
                print(f"   🏷️  Category: {rec['category']}")
                print(f"   🏪 Brand: {rec['brand']}")
                print(f"   ⭐ Rating: {rec['rating']} ({rec['total_reviews']} reviews)")
                print(f"   🏷️  Discount: {rec['discount_percentage']}%")
                print(f"   📦 In Stock: {'Yes' if rec['in_stock'] else 'No'}")
                print(f"   📈 Recommendation Score: {rec['recommendation_score']}")
                print(f"   📊 Metrics:")
                print(f"      - Trending Score: {rec['trending_score']}")
                print(f"      - Engagement Score: {rec['engagement_score']}")
                print(f"      - Popularity Index: {rec['popularity_index']}")
                print(f"      - Quality Score: {rec['quality_score']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    # Test 2: Brand-specific product recommendations
    if store_id:
        print(f"\n📦 Test 2: Brand-Specific Product Recommendations (Store: {store_id})")
        payload = {
            "user_id": user_id,
            "brand_id": store_id,
            "number": 3
        }
        
        try:
            response = requests.post(f"{API_BASE_URL}/recommend/products", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success! Found {data['recommendations_count']} brand-specific recommendations")
                print(f"🏪 Brand ID: {data['brand_id']}")
                print("\n🛍️ Brand-Specific Product Recommendations:")
                
                for i, rec in enumerate(data['recommendations'], 1):
                    print(f"\n{i}. {rec['product_name']}")
                    print(f"   💰 Price: ₹{rec['product_cost']}")
                    print(f"   🏷️  Category: {rec['category']}")
                    print(f"   🏪 Brand: {rec['brand']}")
                    print(f"   📈 Recommendation Score: {rec['recommendation_score']}")
                    print(f"   🎯 Relevance Score: {rec['relevance_score']}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Request failed: {e}")

def test_api_health():
    """Test the API health endpoint."""
    print("🏥 Testing API Health...")
    print("=" * 30)
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/health")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data['status']}")
            print(f"📊 Database: {data['database']}")
            print(f"🕒 Timestamp: {data['timestamp']}")
        else:
            print(f"❌ API Health Check Failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Health check failed: {e}")

def main():
    """Main function to run all tests."""
    print("🚀 Bazaar Recommendation API Test Suite")
    print("=" * 60)
    
    # Test API health first
    test_api_health()
    
    # Test recommendation endpoints
    test_brand_recommendations()
    test_product_recommendations()
    
    print("\n🎉 Test suite completed!")
    print("\n📝 Usage Examples:")
    print("1. Brand Recommendations:")
    print('   curl -X POST http://localhost:5000/recommend/brands \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"user_id": "your_user_id", "number": 5}\'')
    print("\n2. Product Recommendations:")
    print('   curl -X POST http://localhost:5000/recommend/products \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"user_id": "your_user_id", "brand_id": "optional_brand_id", "number": 5}\'')

if __name__ == "__main__":
    main() 