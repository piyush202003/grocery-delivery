from datetime import timedelta
from django.utils import timezone
import random

def dummyProducts():
    return [
            {
                "_id": "69c22613ae75a98c7cd13b3b",
                "name": "Butter Croissant 100g",
                "description": "Flaky and buttery",
                "price": 45,
                "originalPrice": 50,
                "image": "https://raw.githubusercontent.com/avinashdm/gs-images/main/greencart/zvoeqbvrbrt7atqj0dbu.png",
                "category": "bakery",    
                "unit": "100g",
                "stock": 100,
                "isOrganic": False,
                "rating": 4.5,
                "reviewCount": 12,
                "__v": 0,
                "createdAt": "2026-03-24T05:50:11.118Z",
                "updatedAt": "2026-03-24T05:50:11.118Z",
                "discount": 10,
                "id": "69c22613ae75a98c7cd13b3b",
            },
            {
                "_id": "69c22613ae75a98c7cd13b37",
                "name": "Organic Quinoa 500g",
                "description": "High protein, Gluten-free",
                "price": 420,
                "originalPrice": 450,
                "image": "https://raw.githubusercontent.com/avinashdm/gs-images/main/greencart/cxrrgnf12xuhkr4dyhi2.png",
                "category": "pantry-staples",
                "unit": "500g",
                "stock":100,
                "isOrganic": True,
                "rating": 4.5,
                "reviewCount": 12,
                "__v": 0,
                "createdAt": "2026-03-24T05:50:11.118Z",
                "updatedAt": "2026-03-24T05:50:11.118Z",
                "discount": 7,
                "id":"69c22613ae75a98c7cd13b37",
            },
            {
                "_id": "69c22613ae75a98c7cd13b3a",
                "name": "Brown Bread 400g",
                "description": "Soft and healthy, Ideal for breakfast",
                "price": 35,
                "originalPrice": 40,
                "image": "https://raw.githubusercontent.com/avinashdm/gs-images/main/greencart/vy1xa7zovcu22smzapzv.png",
                "category": "bakery",
                "unit": "400g",
                "stock": 100,
                "isOrganic": False,
                "rating": 4.5,
                "reviewCount": 12,
                "__v": 0,
                "createdAt": "2026-03-24T05:50:11.118Z",
                "updatedAt": "2026-03-24T05:50:11.118Z",
                "discount": 13,
                "id": "69c22613ae75a98c7cd13b3a",
            },
            {
                "_id": "69c22613ae75a98c7cd13b36",
                "name": "Barley 1kg",
                "description": "Rich in fiber, Helps digestion",
                "price": 140,
                "originalPrice": 150,
                "image": "https://raw.githubusercontent.com/avinashdm/gs-images/main/greencart/spb5sgy8g24rned9nwog.png",
                "category": "pantry-staples",
                "unit": "1kg",
                "stock": 100,
                "isOrganic": False,
                "rating": 4.5,
                "reviewCount": 12,
                "__v": 0,
                "createdAt": "2026-03-24T05:50:11.118Z",
                "updatedAt": "2026-03-24T05:50:11.118Z",
                "discount": 7,
                "id": "69c22613ae75a98c7cd13b36",
            },
            {
                "_id": "69c22613ae75a98c7cd13b39",
                "name": "Knorr Cup Soup 70g",
                "description": "Convenient and tasty",
                "price": 30,
                "originalPrice": 35,
                "image": "https://raw.githubusercontent.com/avinashdm/gs-images/main/greencart/vnzb2qbwtpab5gnqvx0f.png",
                "category": "pantry-staples",
                "unit": "70g",
                "stock": 100,
                "isOrganic": False,
                "rating": 4.5,
                "reviewCount": 12,
                "__v": 0,
                "createdAt": "2026-03-24T05:50:11.118Z",
                "updatedAt": "2026-03-24T05:50:11.118Z",
                "discount": 14,
                "id": "69c22613ae75a98c7cd13b39",
            },
            {
                "_id": "69c22613ae75a98c7cd13b38",
                "name": "Maggi Noodles 280g",
                "description": "Instant and easy to cook",
                "price": 50,
                "originalPrice": 55,
                "image": "https://raw.githubusercontent.com/avinashdm/gs-images/main/greencart/dsep7owmwvfrukzbslqo.png",
                "category": "pantry-staples",
                "unit": "280g",
                "stock": 100,
                "isOrganic": False,
                "rating": 4,
                "reviewCount": 22,
                "__v": 0,
                "createdAt": "2026-03-24T05:50:11.118Z",
                "updatedAt": "2026-03-24T05:50:11.118Z",
                "discount": 9,
                "id": "69c22613ae75a98c7cd13b38",
            },
            {
                "_id": "69c22613ae75a98c7cd13b30",
                "name": "Sprite 1.5L",
                "description": "Chilled and refreshing, Perfect for celebrations",
                "price": 60,
                "originalPrice": 75,
                "image": "https://raw.githubusercontent.com/avinashdm/gs-images/main/greencart/daiglpvgna1dlhjplbve.png",
                "category": "beverages",
                "unit": "1.5L",
                "stock": 100,
                "isOrganic": False,
                "rating": 4.5,
                "reviewCount": 12,
                "__v": 0,
                "createdAt": "2026-03-24T05:50:11.117Z",
                "updatedAt": "2026-03-24T05:50:11.117Z",
                "discount": 20,
                "id": "69c22613ae75a98c7cd13b30",
            },
            {
                "_id": "69c22613ae75a98c7cd13b23",
                "name": "Carrot 500g",
                "description": "Sweet and crunchy, Good for eyesight, Ideal for juices and salads",
                "price": 44,
                "originalPrice": 50,
                "image": "https://raw.githubusercontent.com/avinashdm/gs-images/main/greencart/ceqgisupuizyste9aifg.png",
                "category": "fruits-vegetables",
                "unit": "500g",
                "stock": 100,
                "isOrganic": True,
                "rating": 4.5,
                "reviewCount": 12,
                "__v": 0,
                "createdAt": "2026-03-24T05:50:11.117Z",
                "updatedAt": "2026-03-24T05:50:11.117Z",
                "discount": 12,
                "id": "69c22613ae75a98c7cd13b23",
            },
            {
                "_id": "69c22613ae75a98c7cd13b2f",
                "name": "Coca-Cola 1.5L",
                "description": "Perfect for parties and gatherings, Best served chilled",
                "price": 75,
                "originalPrice": 80,
                "image": "https://raw.githubusercontent.com/avinashdm/gs-images/main/greencart/eljxcdud6fduwfim5rdx.png",
                "category": "beverages",
                "unit": "1.5L",
                "stock": 100,
                "isOrganic": False,
                "rating": 4.5,
                "reviewCount": 12,
                "__v": 0,
                "createdAt": "2026-03-24T05:50:11.117Z",
                "updatedAt": "2026-03-24T05:50:11.117Z",
                "discount": 6,
                "id": "69c22613ae75a98c7cd13b2f",
            },
            {
                "_id": "69c22613ae75a98c7cd13b35",
                "name": "Brown Rice 1kg",
                "description": "Whole grain and nutritious",
                "price": 110,
                "originalPrice": 120,
                "image": "https://raw.githubusercontent.com/avinashdm/gs-images/main/greencart/dboutcrkdjhoxcvbbqne.png",
                "category": "pantry-staples",
                "unit": "1kg",
                "stock": 100,
                "isOrganic": False,
                "rating": 4.5,
                "reviewCount": 12,
                "__v": 0,
                "createdAt": "2026-03-24T05:50:11.117Z",
                "updatedAt": "2026-03-24T05:50:11.117Z",
                "discount": 8,
                "id": "69c22613ae75a98c7cd13b35",
            }
        ]

def dummyCategoriesData():
    return [
            { "slug": "fruits-vegetables", "name": "Fruits & Vegetables", "image": "fruits_vegetables" },
            { "slug": "personal-care", "name": "Personal Care", "image": "personal_care" },
            { "slug": "pantry-staples", "name": "Pantry Staples", "image": "pantry_staples" },
            { "slug": "bakery", "name": "Bakery", "image": "bakery" },
            { "slug": "beverages", "name": "Beverages", "image": "drinks" },
            { "slug": "meat-seafood", "name": "Meat & Seafood", "image": "meat_seafood" },
            { "slug": "snacks", "name": "Snacks", "image": "snacks" },
            { "slug": "frozen-foods", "name": "Frozen Foods", "image": "frozen_foods" },
            { "slug": "baby-care", "name": "Baby Care", "image": "baby_care" },
            { "slug": "dairy-eggs", "name": "Dairy & Eggs", "image": "dairy_eggs" },
        ]


REVIEWERS = [
    { "name": "Ananya S.", "avatar": "AS" },
    { "name": "Rahul M.", 'avatar': "RM" },
    { "name": "Priya K.", "avatar": "PK" },
    { "name": "Vikram J.", "avatar": "VJ" },
    { "name": "Meera D.", "avatar": "MD" },
    { "name": "Arjun R.", 'avatar': "AR" },
    { "name": "Sneha T.", 'avatar': "ST" },
    { "name": "Karan P.", 'avatar': "KP" },
]

COMMENTS = [
    "Absolutely love this product! Fresh and great quality. Will definitely order again.",
    "Good value for the price. Packaging was neat and delivery was on time.",
    "Quality is decent but I expected it to be a bit fresher. Still a solid buy overall.",
    "This has become a staple in my kitchen now. Highly recommended for everyone!",
    "Exceeded my expectations. The taste and freshness were top-notch. Five stars!",
    "Pretty good! Not the absolute best I've had, but definitely worth the price.",
    "Arrived in perfect condition. Very satisfied with the purchase, ordering more soon.",
    "Great product, my family loved it. The organic quality really shows in the taste.",
]

def generate_dummy_reviews(product):
    
    # Create a local random generator
    # based on product ID
    rng = random.Random(product.id)
    # rng = random.Random(str(product.id))

    # count = min(product['reviewCount'], 6)
    # count = min(product.review_count, 6)
    count = product.review_count

    days_ago = [
        3,
        7,
        14,
        21,
        35,
        48,
    ]

    reviews = []

    for i in range(count):

        reviewer = REVIEWERS[
            (rng.randint(0, len(REVIEWERS) - 1) + i)
            % len(REVIEWERS)
        ]

        # Generate rating around product rating

        rating = round(product.rating+(rng.random()-0.5)*2)
        # rating = round(
        #     product.rating + (rng.random() - 0.5) * 2
        # )

        # Keep rating between 3 and 5
        rating = max(
            3,
            min(5, rating)
        )

        date = timezone.now() - timedelta(
            days=days_ago[i % len(days_ago)]
        )

        comment = COMMENTS[
            (rng.randint(0, len(COMMENTS) - 1) + i)
            % len(COMMENTS)
        ]

        helpful = rng.randint(1, 20)

        reviews.append({
            "id": i,
            "name": reviewer["name"],
            "avatar": reviewer["avatar"],
            "rating": rating,
            "date": date,
            "comment": comment,
            "helpful": helpful,
        })

    return reviews

def get_rating_breakdown(reviews):

    counts = [0, 0, 0, 0, 0]

    for review in reviews:

        rating = review["rating"]

        counts[rating - 1] += 1

    # 5 → 1
    return counts[::-1]

def dummyDashboardOrdersData():
    return [
    {
        "shippingAddress": {
            "label": "Home",
            "address": "New Market Road",
            "city": "New York",
            "state": "NY",
            "zip": "876543",
            "lat": 40.7128,
            "lng": -74.006,
        },
        "liveLocation": {
            "lat": 40.7128,
            "lng": -74.006,
            "updatedAt": "2026-04-06T08:41:27.211Z",
        },
        "id": "69d366617ed7e54198d67dac",
        "user": {
            "id": "69bb6caf448f2d818db59122",
            "name": "Admin",
            "email": "admin@example.com",
        },
        "items": [
            {
                "product": "69c22613ae75a98c7cd13b3b",
                "name": "Butter Croissant 100g",
                "image": "https://raw.githubusercontent.com/avinashdm/gs-images/main/greencart/zvoeqbvrbrt7atqj0dbu.png",
                "price": 45,
                "quantity": 2,
                "unit": "100g",
                "id": "69d366617ed7e54198d67dad",
            },
            {
                "product": "69c22613ae75a98c7cd13b36",
                "name": "Barley 1kg",
                "image": "https://raw.githubusercontent.com/avinashdm/gs-images/main/greencart/spb5sgy8g24rned9nwog.png",
                "price": 140,
                "quantity": 1,
                "unit": "1kg",
                "id": "69d366617ed7e54198d67dae",
            },
            
        ],
        "paymentMethod": "cash",
        "subtotal": 230,
        "deliveryFee": 0,
        "tax": 18.4,
        "total": 248.4,
        "status": "Delivered",
        "statusHistory": [
            {
                "status": "Placed",
                "note": "Order placed successfully",
                "id": "69d366617ed7e54198d67daf",
                "timestamp": "2026-04-06T07:53:05.769Z",
            },
            {
                "status": "Assigned",
                "note": "Assigned to Rahul",
                "id": "69d366ab7ed7e54198d67dbe",
                "timestamp": "2026-04-06T07:54:19.796Z",
            },
            {
                "status": "Packed",
                "note": "Status updated to Packed",
                "id": "69d366b37ed7e54198d67ddc",
                "timestamp": "2026-04-06T07:54:27.171Z",
            },
            {
                "status": "Out for Delivery",
                "note": "Status updated to Out for Delivery",
                "id": "69d366b57ed7e54198d67e00",
                "timestamp": "2026-04-06T07:54:29.226Z",
            },
            {
                "status": "Delivered",
                "note": "Delivered by partner",
                "id": "69d373207ed7e54198d681b1",
                "timestamp": "2026-04-06T08:47:28.983Z",
            },
        ],
        "deliveryPartner": {
            "id": "69bbfc3866db7c6cdea47ede",
            "name": "Rahul",
            "email": "rahul@example.com",
            "phone": "987654321",
            'vehicleType': 'van',
        },
        "deliveryOtp": "",
        "isPaid": False,
        "createdAt": "2026-04-06T07:53:05.774Z",
        "updatedAt": "2026-04-06T08:47:28.984Z",
        "__v": 4,
    },

    {
        "shippingAddress": {
            "label": "Home",
            "address": "New Market Road",
            "city": "New York",
            "state": "NY",
            "zip": "876543",
            "lat": 40.7128,
            "lng": -74.006,
        },
        "liveLocation": {
            "lat": 40.7120,
            "lng": -74.006,
            "updatedAt": "2026-04-06T08:41:27.211Z",
        },
        "id": "69d366617ed7e54198d67dad",
        "user": {
            "id": "69bb6caf448f2d818db59122",
            "name": "Admin",
            "email": "admin@example.com",
        },
        "items": [
            {
                "product": "69c22613ae75a98c7cd13b3b",
                "name": "Butter Croissant 100g",
                "image": "https://raw.githubusercontent.com/avinashdm/gs-images/main/greencart/zvoeqbvrbrt7atqj0dbu.png",
                "price": 45,
                "quantity": 2,
                "unit": "100g",
                "id": "69d366617ed7e54198d67dad",
            },
            {
                "product": "69c22613ae75a98c7cd13b36",
                "name": "Barley 1kg",
                "image": "https://raw.githubusercontent.com/avinashdm/gs-images/main/greencart/spb5sgy8g24rned9nwog.png",
                "price": 140,
                "quantity": 1,
                "unit": "1kg",
                "id": "69d366617ed7e54198d67dae",
            },
        ],
        "paymentMethod": "cash",
        "subtotal": 230,
        "deliveryFee": 0,
        "tax": 18.4,
        "total": 248.4,
        "status": "Out for Delivery",
        "statusHistory": [
            {
                "status": "Placed",
                "note": "Order placed successfully",
                "id": "69d366617ed7e54198d67daf",
                "timestamp": "2026-04-06T07:53:05.769Z",
            },
            {
                "status": "Assigned",
                "note": "Assigned to Rahul",
                "id": "69d366ab7ed7e54198d67dbe",
                "timestamp": "2026-04-06T07:54:19.796Z",
            },
            {
                "status": "Packed",
                "note": "Status updated to Packed",
                "id": "69d366b37ed7e54198d67ddc",
                "timestamp": "2026-04-06T07:54:27.171Z",
            },
            {
                "status": "Out for Delivery",
                "note": "Status updated to Out for Delivery",
                "id": "69d366b57ed7e54198d67e00",
                "timestamp": "2026-04-06T07:54:29.226Z",
            },
        ],
        "deliveryPartner": {
            "id": "69bbfc3866db7c6cdea47ede",
            "name": "Rahul",
            "email": "rahul@example.com",
            "phone": "987654321",
            'vehicleType': 'bike',
        },
        "deliveryOtp": "754730",
        "isPaid": False,
        "createdAt": "2026-04-06T07:53:05.774Z",
        "updatedAt": "2026-04-06T08:47:28.984Z",
        "__v": 4,
    },
]

def statusColors():
    return {
        'Placed': "bg-blue-100 text-blue-700",
        'Confirmed': "bg-indigo-100 text-indigo-700",
        'Packed': "bg-purple-100 text-purple-700",
        "Out for Delivery": "bg-orange-400/10 text-orange-400",
        'Delivered': "bg-green-100 text-green-700",
        'Cancelled': "bg-red-100 text-red-700",
    }

def dummyAddressData(): 
    return [
        { 'label': "Home", 'address': "123 Main St ", 'city': "New York ", 'state': "NY", 'zip': "10001", 'isDefault': True, 'lat': 40.7128, 'lng': -74.006, 'id': "69d3652df9a340288f1a0f8c" },
        { 'label': "Work", 'address': "456 Market St ", 'city': "New York ", 'state': "NY", 'zip': "10002", 'isDefault': False, 'lat': 40.7128, 'lng': -74.006, 'id': "69d3652df9a340288f1a0f8d" },
    ]