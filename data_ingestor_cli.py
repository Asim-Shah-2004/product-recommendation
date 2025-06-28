#!/usr/bin/env python3
"""
Data Ingestor CLI for Bazaar Recommendation System
This script helps populate the database with mock data for testing and development.
"""

import sys
import json
import random
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import time
from bson import ObjectId

# MongoDB Connection
MONGO_URI = "mongodb+srv://bazaar:bazaar123@cluster-1.o2duhip.mongodb.net/bazaar"

# Sample data templates
FIRST_NAMES = [
    "Alex", "Sam", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Quinn",
    "Avery", "Blake", "Cameron", "Drew", "Emery", "Finley", "Gray", "Harper",
    "Indigo", "Jamie", "Kendall", "Logan", "Mason", "Noah", "Oakley", "Parker",
    "Quincy", "River", "Sage", "Tatum", "Unity", "Vale", "Winter", "Xander",
    "Yuki", "Zara", "Aria", "Bella", "Chloe", "Diana", "Eva", "Fiona", "Grace"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green"
]

CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata",
    "Pune", "Ahmedabad", "Jaipur", "Surat", "Lucknow", "Kanpur", "Nagpur",
    "Indore", "Thane", "Bhopal", "Visakhapatnam", "Pimpri-Chinchwad",
    "Patna", "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik"
]

STATES = [
    "Maharashtra", "Delhi", "Karnataka", "Telangana", "Tamil Nadu",
    "West Bengal", "Gujarat", "Rajasthan", "Uttar Pradesh", "Madhya Pradesh",
    "Andhra Pradesh", "Bihar", "Punjab", "Haryana", "Kerala", "Odisha"
]

OCCUPATIONS = [
    "Software Engineer", "Data Scientist", "Product Manager", "Designer",
    "Marketing Manager", "Sales Executive", "Teacher", "Doctor", "Lawyer",
    "Accountant", "Business Analyst", "Project Manager", "Consultant",
    "Entrepreneur", "Student", "Freelancer", "Artist", "Writer"
]

INTERESTS = [
    "technology", "fitness", "travel", "cooking", "photography", "music",
    "reading", "gaming", "sports", "fashion", "art", "movies", "dancing",
    "hiking", "swimming", "yoga", "meditation", "gardening", "painting"
]

CATEGORIES = [
    "electronics", "fashion", "home", "sports", "books", "beauty",
    "automotive", "health", "toys", "food", "jewelry", "furniture"
]

BRAND_NAMES = [
    "TechHub", "SportsArena", "FashionForward", "HomeEssentials", "BeautyGlow",
    "FitnessPro", "GadgetWorld", "StyleStudio", "LifestylePlus", "WellnessHub",
    "SmartTech", "ActiveWear", "EcoFriendly", "PremiumBrand", "TrendSetter"
]

PRODUCT_NAMES = [
    "Wireless Headphones", "Smart Fitness Tracker", "Premium Smartphone",
    "Laptop Pro", "Wireless Earbuds", "Smart Watch", "Gaming Console",
    "Bluetooth Speaker", "Camera DSLR", "Tablet Pro", "Wireless Mouse",
    "Mechanical Keyboard", "Gaming Headset", "Power Bank", "USB Cable"
]

def connect_to_mongodb():
    """Connect to MongoDB and return client and database objects."""
    try:
        client = MongoClient(MONGO_URI)
        # Test the connection
        client.admin.command('ping')
        db = client.bazaar
        print("✅ Successfully connected to MongoDB!")
        return client, db
    except ConnectionFailure as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        sys.exit(1)

def confirm_database_deletion():
    """Ask user to confirm database deletion."""
    print("\n⚠️  WARNING: This will delete ALL collections except 'Auth'!")
    print("   The following collections will be deleted:")
    print("   - users")
    print("   - stores") 
    print("   - products")
    print("   - Any other collections except 'Auth'")
    print("   This action cannot be undone.")
    
    while True:
        confirmation = input("\nAre you sure you want to proceed? (yes/no): ").lower().strip()
        if confirmation in ['yes', 'y']:
            return True
        elif confirmation in ['no', 'n']:
            print("Operation cancelled.")
            return False
        else:
            print("Please enter 'yes' or 'no'.")

def delete_collections_except_auth(db):
    """Delete all collections except Auth."""
    collections_to_delete = []
    
    # Get all collection names
    all_collections = db.list_collection_names()
    
    # Filter out Auth collection
    for collection_name in all_collections:
        if collection_name != "Auth":
            collections_to_delete.append(collection_name)
    
    if collections_to_delete:
        print(f"🗑️  Deleting collections: {', '.join(collections_to_delete)}")
        for collection_name in collections_to_delete:
            try:
                db[collection_name].drop()
                print(f"   ✅ Deleted collection: {collection_name}")
            except Exception as e:
                print(f"   ❌ Error deleting {collection_name}: {e}")
    else:
        print("ℹ️  No collections to delete (only Auth collection exists)")

def generate_user_data(count):
    """Generate mock user data."""
    users = []
    
    for i in range(count):
        user = {
            "userFirstName": random.choice(FIRST_NAMES),
            "userLastName": random.choice(LAST_NAMES),
            "userEmail": f"user{i+1}@example.com",
            "userPassword": "password123",
            "gender": random.choice(["male", "female", "other"]),
            "age": random.randint(18, 65),
            "location": f"{random.choice(CITIES)}, {random.choice(STATES)}",
            "occupation": random.choice(OCCUPATIONS),
            "interests": random.sample(INTERESTS, random.randint(2, 5)),
            "budgetRange": random.choice(["1000-5000", "5000-15000", "15000-30000", "30000+"]),
            "userEvents": {
                "storeClicks": {},
                "productClicks": {},
                "purchases": [],
                "wishlist": [],
                "searchHistory": []
            }
        }
        users.append(user)
    
    return users

def generate_store_data(count):
    """Generate mock store data."""
    stores = []
    
    for i in range(count):
        # Generate base metrics
        click_count = random.randint(100, 10000)
        view_count = random.randint(1000, 50000)
        follower_count = random.randint(500, 20000)
        product_count = random.randint(50, 1000)
        rating = round(random.uniform(3.5, 5.0), 1)
        total_reviews = random.randint(50, 2000)
        
        # Calculate derived metrics
        trending_score = calculate_trending_score(click_count, view_count, 0, 0, rating, total_reviews)
        engagement_score = calculate_engagement_score(click_count, view_count, 0, 0, follower_count)
        popularity_index = calculate_popularity_index(view_count, click_count, 0, follower_count, product_count)
        quality_score = calculate_quality_score(rating, total_reviews, 0, 0)
        
        store = {
            "storeName": f"{random.choice(BRAND_NAMES)} {i+1}",
            "storeTagline": f"Quality products for everyone - Store {i+1}",
            "storeOfficialUrl": f"https://store{i+1}.com",
            "storeImageUrl": f"https://images.unsplash.com/photo-{random.randint(1000000000, 9999999999)}?w=400",
            "category": random.choice(CATEGORIES),
            "subcategory": f"subcategory_{random.randint(1, 5)}",
            "location": f"{random.choice(CITIES)}, {random.choice(STATES)}",
            "rating": rating,
            "totalReviews": total_reviews,
            "foundedYear": random.randint(2010, 2023),
            "description": f"Premium {random.choice(CATEGORIES)} store offering quality products.",
            "specialties": random.sample(CATEGORIES, random.randint(2, 4)),
            "brands": random.sample(BRAND_NAMES, random.randint(2, 5)),
            "services": ["online_store", "physical_store"],
            "socialMedia": {
                "instagram": f"@store{i+1}",
                "facebook": f"Store{i+1}Official",
                "twitter": f"@store{i+1}"
            },
            "contactInfo": {
                "phone": f"+91-{random.randint(7000000000, 9999999999)}",
                "email": f"info@store{i+1}.com",
                "address": f"{random.randint(1, 999)} Street, {random.choice(CITIES)}"
            },
            "clickCount": click_count,
            "viewCount": view_count,
            "followerCount": follower_count,
            "productCount": product_count,
            "trendingScore": trending_score,
            "engagementScore": engagement_score,
            "popularityIndex": popularity_index,
            "qualityScore": quality_score
        }
        stores.append(store)
    
    return stores

def generate_product_data(count, store_ids):
    """Generate mock product data."""
    products = []
    
    for i in range(count):
        # Generate base metrics
        click_count = random.randint(50, 5000)
        view_count = random.randint(500, 25000)
        purchase_count = random.randint(10, 1000)
        wishlist_count = random.randint(5, 500)
        rating = round(random.uniform(3.0, 5.0), 1)
        total_reviews = random.randint(10, 2000)
        discount_percentage = random.randint(0, 50)
        
        # Calculate derived metrics
        trending_score = calculate_trending_score(click_count, view_count, purchase_count, wishlist_count, rating, total_reviews)
        engagement_score = calculate_engagement_score(click_count, view_count, purchase_count, wishlist_count)
        popularity_index = calculate_popularity_index(view_count, click_count, purchase_count)
        quality_score = calculate_quality_score(rating, total_reviews, purchase_count, wishlist_count, discount_percentage)
        
        product = {
            "productName": f"{random.choice(PRODUCT_NAMES)} {i+1}",
            "productImageUrl": f"https://images.unsplash.com/photo-{random.randint(1000000000, 9999999999)}?w=600",
            "productDescription": f"High-quality {random.choice(PRODUCT_NAMES).lower()} with amazing features.",
            "productCost": random.randint(500, 50000),
            "productUrl": f"https://product{i+1}.com",
            "productStoreId": random.choice(store_ids),  # This will be an ObjectId
            "category": random.choice(CATEGORIES),
            "subcategory": f"subcategory_{random.randint(1, 5)}",
            "brand": random.choice(BRAND_NAMES),
            "rating": rating,
            "totalReviews": total_reviews,
            "inStock": random.choice([True, True, True, False]),  # 75% chance of being in stock
            "discountPercentage": discount_percentage,
            "originalPrice": random.randint(1000, 60000),
            "tags": random.sample(["premium", "wireless", "smart", "portable", "durable", "eco-friendly"], random.randint(2, 4)),
            "features": random.sample(["High Quality", "Durable", "Wireless", "Smart", "Portable"], random.randint(2, 4)),
            "specifications": {
                "weight": f"{random.randint(100, 2000)}g",
                "batteryLife": f"{random.randint(5, 100)} hours",
                "connectivity": random.choice(["Bluetooth", "WiFi", "USB", "Wireless"]),
                "warranty": f"{random.randint(1, 3)} years"
            },
            "clickCount": click_count,
            "viewCount": view_count,
            "purchaseCount": purchase_count,
            "wishlistCount": wishlist_count,
            "trendingScore": trending_score,
            "engagementScore": engagement_score,
            "popularityIndex": popularity_index,
            "qualityScore": quality_score
        }
        products.append(product)
    
    return products

def populate_user_events(users, store_ids, product_ids):
    """Populate user events with realistic click data."""
    for user in users:
        # Generate store clicks
        num_store_clicks = random.randint(1, min(5, len(store_ids)))
        selected_stores = random.sample(store_ids, num_store_clicks)
        for store_id in selected_stores:
            user["userEvents"]["storeClicks"][str(store_id)] = random.randint(1, 100)
        
        # Generate product clicks
        num_product_clicks = random.randint(1, min(8, len(product_ids)))
        selected_products = random.sample(product_ids, num_product_clicks)
        for product_id in selected_products:
            user["userEvents"]["productClicks"][str(product_id)] = random.randint(1, 150)
        
        # Generate some purchases
        num_purchases = random.randint(0, 3)
        if num_purchases > 0:
            purchased_products = random.sample(product_ids, min(num_purchases, len(product_ids)))
            for product_id in purchased_products:
                purchase = {
                    "productId": product_id,
                    "storeId": random.choice(store_ids),
                    "purchaseDate": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
                    "amount": random.randint(500, 10000)
                }
                user["userEvents"]["purchases"].append(purchase)
        
        # Generate wishlist
        num_wishlist = random.randint(0, 5)
        if num_wishlist > 0:
            user["userEvents"]["wishlist"] = random.sample(product_ids, min(num_wishlist, len(product_ids)))
        
        # Generate search history
        search_terms = random.sample(PRODUCT_NAMES + ["smartphone", "laptop", "headphones", "fitness"], random.randint(2, 6))
        user["userEvents"]["searchHistory"] = search_terms

def calculate_trending_score(click_count, view_count, purchase_count, wishlist_count, rating, total_reviews):
    """Calculate trending score based on real metrics"""
    if view_count == 0: view_count = 1
    if click_count == 0: click_count = 1
    
    ctr_score = min(click_count / view_count, 1.0)
    conversion_score = min(purchase_count / click_count, 1.0)
    wishlist_score = min(wishlist_count / view_count, 1.0)
    rating_score = rating / 5.0
    review_score = min(total_reviews / 1000, 1.0)
    
    trending_score = (
        ctr_score * 0.25 +
        conversion_score * 0.30 +
        wishlist_score * 0.15 +
        rating_score * 0.20 +
        review_score * 0.10
    )
    return round(trending_score, 3)

def calculate_engagement_score(click_count, view_count, purchase_count, wishlist_count, follower_count=0):
    """Calculate engagement score based on user interaction depth"""
    if view_count == 0: view_count = 1
    if click_count == 0: click_count = 1
    
    interaction_rate = (click_count + purchase_count + wishlist_count) / view_count
    completion_rate = (purchase_count + wishlist_count) / click_count
    social_score = min(follower_count / 10000, 1.0) if follower_count > 0 else 0
    
    engagement_score = (
        min(interaction_rate, 1.0) * 0.40 +
        min(completion_rate, 1.0) * 0.40 +
        social_score * 0.20
    )
    return round(engagement_score, 3)

def calculate_popularity_index(view_count, click_count, purchase_count, follower_count=0, product_count=0):
    """Calculate popularity index based on overall visibility and reach"""
    total_reach = view_count + follower_count
    total_engagement = click_count + purchase_count
    scale_factor = min(product_count / 500, 1.0) if product_count > 0 else 1.0
    
    reach_score = min(total_reach / 50000, 1.0)
    engagement_score = min(total_engagement / 5000, 1.0)
    
    popularity_index = (
        reach_score * 0.50 +
        engagement_score * 0.40 +
        scale_factor * 0.10
    )
    return round(popularity_index, 3)

def calculate_quality_score(rating, total_reviews, purchase_count, wishlist_count, discount_percentage=0):
    """Calculate quality score based on user satisfaction and value perception"""
    review_credibility = min(total_reviews / 500, 1.0)
    rating_score = (rating / 5.0) * review_credibility
    
    total_interest = purchase_count + wishlist_count
    satisfaction_rate = purchase_count / total_interest if total_interest > 0 else 0
    
    value_score = 1.0 - (discount_percentage / 100.0)
    
    quality_score = (
        rating_score * 0.50 +
        satisfaction_rate * 0.30 +
        value_score * 0.20
    )
    return round(quality_score, 3)

def main():
    """Main function to run the data ingestion CLI."""
    print("🚀 Bazaar Recommendation System - Data Ingestor CLI")
    print("=" * 60)
    
    # Connect to MongoDB
    client, db = connect_to_mongodb()
    
    # Get user input for data quantity
    while True:
        try:
            count = int(input("\nHow much mock data do you want to generate? (recommended: 100-1000): "))
            if count > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Confirm database deletion
    if not confirm_database_deletion():
        client.close()
        return
    
    # Delete collections except Auth
    delete_collections_except_auth(db)
    
    print(f"\n📊 Generating {count} records for each collection...")
    
    # Generate stores first (needed for products)
    stores = generate_store_data(count)
    
    # Insert stores and get real ObjectIds
    print("   Inserting stores...")
    store_result = db.stores.insert_many(stores)
    store_ids = store_result.inserted_ids
    print(f"   ✅ Inserted {len(stores)} stores")
    
    # Generate products with real store ObjectIds
    products = generate_product_data(count, store_ids)
    
    # Insert products and get real ObjectIds
    print("   Inserting products...")
    product_result = db.products.insert_many(products)
    product_ids = product_result.inserted_ids
    print(f"   ✅ Inserted {len(products)} products")
    
    # Generate users
    users = generate_user_data(count)
    
    # Populate user events with real ObjectIds
    print("🔗 Populating user events...")
    populate_user_events(users, store_ids, product_ids)
    
    # Insert users
    print("   Inserting users...")
    db.users.insert_many(users)
    print(f"   ✅ Inserted {len(users)} users")
    
    print(f"\n🎉 Successfully generated and inserted {count} records for each collection!")
    
    # Display summary
    print("\n📈 Database Summary:")
    print(f"   Stores: {db.stores.count_documents({})}")
    print(f"   Products: {db.products.count_documents({})}")
    print(f"   Users: {db.users.count_documents({})}")
    print(f"   Auth collection: {db.Auth.count_documents({})} (preserved)")
    
    # Display sample derived metrics
    print("\n📊 Sample Derived Metrics:")
    sample_store = db.stores.find_one()
    if sample_store:
        print(f"   Store '{sample_store['storeName']}':")
        print(f"     Trending Score: {sample_store['trendingScore']}")
        print(f"     Engagement Score: {sample_store['engagementScore']}")
        print(f"     Popularity Index: {sample_store['popularityIndex']}")
        print(f"     Quality Score: {sample_store['qualityScore']}")
    
    sample_product = db.products.find_one()
    if sample_product:
        print(f"   Product '{sample_product['productName']}':")
        print(f"     Trending Score: {sample_product['trendingScore']}")
        print(f"     Engagement Score: {sample_product['engagementScore']}")
        print(f"     Popularity Index: {sample_product['popularityIndex']}")
        print(f"     Quality Score: {sample_product['qualityScore']}")
    
    client.close()
    print("\n👋 Database connection closed.")

if __name__ == "__main__":
    main() 