# backend.py (Your backend logic)
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch

# Initialize Elasticsearch and the Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')
es = Elasticsearch(
    "https://my-elasticsearch-project-a610a8.es.us-west-2.aws.elastic.cloud:443",
    api_key="TzRYd09wVUJzNHJ1TnVZQ2VTQWE6dU5TUmhEaGZDX2xTa0NSVjQteWhydw==")  # Assuming Elasticsearch is already running

transactions = [
    {"user_id": 2, "description": "reusable water bottle", "cost": 20.0},
    {"user_id": 2, "description": "organic cotton t-shirt", "cost": 25.0},
    {"user_id": 2, "description": "solar-powered charger", "cost": 50.0},
    {"user_id": 2, "description": "bamboo toothbrush", "cost": 5.0},
    {"user_id": 2, "description": "composting bin", "cost": 40.0},
    {"user_id": 2, "description": "eco-friendly laundry detergent", "cost": 15.0},
    {"user_id": 2, "description": "recycled paper notebooks", "cost": 10.0},
    {"user_id": 2, "description": "plant-based protein powder", "cost": 30.0},
    {"user_id": 2, "description": "electric car charging station subscription", "cost": 100.0},
    {"user_id": 2, "description": "LED light bulbs", "cost": 10.0},
    {"user_id": 2, "description": "rainwater harvesting system", "cost": 300.0},
    {"user_id": 2, "description": "organic vegetable seeds", "cost": 8.0},
    {"user_id": 2, "description": "sustainable food wrap (beeswax wraps)", "cost": 12.0},
    {"user_id": 2, "description": "eco-friendly cleaning products", "cost": 20.0},
    {"user_id": 2, "description": "carbon offset donation", "cost": 50.0},
    {"user_id": 1, "description": "running shoes", "cost": 150.0},
    {"user_id": 1, "description": "gym membership", "cost": 150.0},
    {"user_id": 1, "description": "protein powder", "cost": 150.0},
    {"user_id": 1, "description": "bcaa", "cost": 150.0},
    {"user_id": 1, "description": "lifting straps", "cost": 150.0},
    {"user_id": 1, "description": "shaker bottle", "cost": 150.0},
    {"user_id": 1, "description": "badminton shoes", "cost": 150.0},
    {"user_id": 3, "description": "Jay Chou concert", "cost": 150.0},
    {"user_id": 3, "description": "Eric Chou concert", "cost": 150.0},
    {"user_id": 3, "description": "IVE music album", "cost": 150.0},
    {"user_id": 3, "description": "IU photocards", "cost": 150.0},
    {"user_id": 3, "description": "IU merchandise", "cost": 150.0},
    {"user_id": 3, "description": "Twice concert ticket", "cost": 150.0},
    {"user_id": 3, "description": "Limited edition shoes endorsed by G-dragon", "cost": 150.0},
    {"user_id": 3, "description": "Puma x Some pop star collab", "cost": 150.0},
    {"user_id": 3, "description": "Gentle monster endorsed by Jennie", "cost": 150.0},
]

# Predefined Profile Categories (same as before)
categories = [
    {"category": "Health Conscious", "description": "A Fitness Guru is someone who prioritizes physical fitness and well-being, often engaging in regular workouts, sports activities, and wellness practices. They are passionate about maintaining an active lifestyle and improving their health through exercise, nutrition, and self-care."},
    {"category": "Star Chaser", "description": "A Pop Star Chaser is someone who is deeply fascinated by celebrities, particularly pop stars, and tailors their lifestyle and spending habits around their favorite idols. They follow the latest news, social media updates, and public appearances of pop stars, attending concerts, meet-and-greet events, and exclusive fan gatherings."},
    {"category": "Political", "description": "Includes political discussions, debates, government policies, and social issues."},
    {"category": "Save the earth", "description": "A Save the Earth enthusiast's transactions reflect a lifestyle centered around environmental sustainability and conservation efforts. For instance, they might purchase a solar-powered charger to reduce reliance on non-renewable energy sources or a compost bin to promote organic waste recycling. Their shopping basket could include biodegradable cleaning products, organic cotton clothing, or sustainable fashion items, all aimed at reducing their environmental impact. They may also buy eco-friendly home appliances, such as energy-efficient refrigerators or LED lighting to lower energy consumption.In addition, this individual is likely to invest in electric vehicles or bicycles to minimize their carbon footprint, as well as reusable shopping bags and water bottles to avoid single-use plastics. They may regularly donate to environmental organizations or purchase tickets to eco-conscious events and green tech conferences. Supporting plant-based food options could also be a major part of their routine, reflecting a commitment to reducing the environmental impact of food production. They might attend beach cleanups, buy carbon offsets, or participate in tree planting activities. These purchases and actions demonstrate a consistent, conscious effort to promote sustainability and make a tangible difference in the fight against climate change."},
    {"category": "Judgemental", "description": "Includes anything related to trading, stocks, options, investments, prices of gold, silver, investment products, housing, crypto."}
]

# Predefined News Genres (same as before)
news_genres = [
    {"genre": "Entertainment", "description": "Covers movies, music, celebrity news, TV shows, and all things related to entertainment."},
    {"genre": "Politics", "description": "In-depth coverage of political news, elections, government policies, and political events."},
    {"genre": "Environment", "description": "overs topics related to the natural world, climate change, sustainability, and environmental conservation efforts. It highlights the latest developments in global and local environmental issues, such as the impact of human activities on ecosystems, wildlife conservation, deforestation, pollution, and the depletion of natural resources. Environmental news also focuses on efforts to combat climate change, including renewable energy initiatives, conservation programs, and governmental policies aimed at reducing carbon emissions. This genre covers cutting-edge research on alternative energy, environmental activism, climate policy, as well as community-driven sustainability efforts. It often includes updates on eco-friendly technologies, environmental regulations, and corporate efforts to go green. With the rising awareness of climate change and environmental degradation, this genre plays a crucial role in informing the public about how actions today can affect the planet’s future and what steps are being taken to protect it."},
    {"genre": "Health & Fitness", "description": "Focuses on the latest developments in exercise, nutrition, wellness trends, and overall well-being."},
    {"genre": "Technology", "description": "Covers tech news, gadgets, innovations, software, and the world of technology."}
]

# Sample News Articles (you can add more)
news_articles = [
    {"message": "New studies show the increasing effects of climate change on coastal cities.", "category": "Environment"},
    {"message": "Renewable energy technologies are advancing rapidly and promise a greener future.", "category": "Environment"},
    {"message": "Hollywood stars gather to discuss sustainable fashion at global event.", "category": "Entertainment"},
    {"message": "Political leaders debate new laws to protect the environment from corporate polluters.", "category": "Politics"},
    {"message": "The latest advancements in health and fitness technology are revolutionizing the industry.", "category": "Health & Fitness"},
    {"message": "Tech companies announce new AI-driven tools for environmental protection.", "category": "Technology"}
]

# Elasticsearch Indexing Functions
# Create News Article Index
def create_news_article_index():
    news_article_mapping = {
        "mappings": {
            "properties": {
                "message": {"type": "text"},
                "category": {"type": "keyword"},
                "article_vector": {
                    "type": "dense_vector",
                    "dims": 384  # Sentence Transformer embedding dimensionality
                }
            }
        }
    }

    if not es.indices.exists(index="news_articles"):
        es.indices.create(index="news_articles", body=news_article_mapping)
        print("News articles index created.")

def create_transaction_index():
    transaction_mapping = {
        "mappings": {
            "properties": {
                "user_id": {"type": "keyword"},
                "description": {"type": "text"},
                "cost": {"type": "float"},
                "transaction_vector": {
                    "type": "dense_vector",
                    "dims": 384  # Sentence Transformer embedding dimensionality
                }
            }
        }
    }

    if not es.indices.exists(index="user_transactions"):
        es.indices.create(index="user_transactions", body=transaction_mapping)
        print("Transactions index created.")

def create_category_index():
    category_mapping = {
        "mappings": {
            "properties": {
                "category": {"type": "keyword"},
                "category_description": {"type": "text"},
                "category_vector": {
                    "type": "dense_vector",
                    "dims": 384  # Sentence Transformer embedding dimensionality
                }
            }
        }
    }

    if not es.indices.exists(index="user_categories"):
        es.indices.create(index="user_categories", body=category_mapping)
        print("Category index created.")

def create_news_genre_index():
    news_genre_mapping = {
        "mappings": {
            "properties": {
                "genre": {"type": "keyword"},
                "genre_description": {"type": "text"},
                "genre_vector": {
                    "type": "dense_vector",
                    "dims": 384  # Sentence Transformer embedding dimensionality
                }
            }
        }
    }

    if not es.indices.exists(index="user_news_genres"):
        es.indices.create(index="user_news_genres", body=news_genre_mapping)
        print("News genres index created.")

# Generate Embeddings for Transaction Descriptions
def generate_transaction_embedding(description):
    return model.encode(description)

# Generate Embeddings for Category Descriptions
def generate_category_description_embedding(description):
    return model.encode(description)

# Generate Embeddings for News Genres Descriptions
def generate_news_genre_embedding(description):
    return model.encode(description)

# Index Sample Transactions
def index_transactions():
    for transaction in transactions:
        description = transaction["description"]
        user_id = transaction["user_id"]  # Extract user_id
        embedding = generate_transaction_embedding(description)

        es.index(index="user_transactions", document={
            "user_id": user_id,  # Include user_id in the document
            "description": description,
            "cost": transaction["cost"],
            "transaction_vector": embedding.tolist()
        })
    print("Transactions indexed.")

# Index Profile Categories with Descriptions
def index_categories():
    for category in categories:
        embedding = generate_category_description_embedding(category["description"])

        es.index(index="user_categories", document={
            "category": category["category"],
            "category_description": category["description"],
            "category_vector": embedding.tolist()
        })
    print("Profile categories indexed.")

# Index News Genres with Descriptions
def index_news_genres():
    for genre in news_genres:
        embedding = generate_news_genre_embedding(genre["description"])

        es.index(index="user_news_genres", document={
            "genre": genre["genre"],
            "genre_description": genre["description"],
            "genre_vector": embedding.tolist()
        })
    print("News genres indexed.")

# Index Sample News Articles
def index_news_articles():
    for article in news_articles:
        message = article["message"]
        category = article["category"]
        embedding = model.encode(message)  # Generate embedding for the article message

        es.index(index="news_articles", document={
            "message": message,
            "category": category,
            "article_vector": embedding.tolist()
        })
    print("News articles indexed.")

# Step 1: Aggregate a User's Transactions
def aggregate_user_transactions(user_id):
    # Filter transactions by user_id
    user_transactions = [t["description"] for t in transactions if t["user_id"] == user_id]

    # Combine all transaction descriptions for the user into one string
    aggregated_description = " ".join(user_transactions)

    return aggregated_description

# Step 2: Find the most relevant category based on aggregated transaction descriptions
def find_relevant_category(user_id):
    aggregated_description = aggregate_user_transactions(user_id)

    # Generate embedding for aggregated description
    user_embedding = generate_transaction_embedding(aggregated_description)

    # Query Elasticsearch for categories and calculate cosine similarity with category embeddings
    query = {
        "size": 1000,  # Fetch all categories
        "_source": ["category", "category_description", "category_vector"]
    }
    response = es.search(index="user_categories", body=query)

    category_embeddings = []
    for hit in response["hits"]["hits"]:
        category = hit["_source"]["category"]
        category_description = hit["_source"]["category_description"]
        embedding = np.array(hit["_source"]["category_vector"])
        category_embeddings.append((category, category_description, embedding))

    # Find the most relevant category based on cosine similarity
    similarities = []
    for category, category_description, embedding in category_embeddings:
        similarity = cosine_similarity([user_embedding], [embedding])[0][0]
        similarities.append((category, similarity))

    # Return the category with the highest similarity
    similarities.sort(key=lambda x: x[1], reverse=True)
    most_relevant_category = similarities[0][0]

    return most_relevant_category

# Step 3: Find the most relevant news genre based on the selected category's embedding
def find_relevant_news_genre(category):
    category_description = next(c['description'] for c in categories if c['category'] == category)
    category_embedding = generate_category_description_embedding(category_description)

    query = {
        "size": 1000,  # Fetch all genres
        "_source": ["genre", "genre_description", "genre_vector"]
    }
    response = es.search(index="user_news_genres", body=query)

    genre_embeddings = []
    for hit in response["hits"]["hits"]:
        genre = hit["_source"]["genre"]
        genre_description = hit["_source"]["genre_description"]
        embedding = np.array(hit["_source"]["genre_vector"])
        genre_embeddings.append((genre, genre_description, embedding))

    similarities = []
    for genre, genre_description, embedding in genre_embeddings:
        similarity = cosine_similarity([category_embedding], [embedding])[0][0]
        similarities.append((genre, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)
    most_relevant_genre = similarities[0][0]

    return most_relevant_genre
# Step 4: Fetch News Articles Based on Genre
def find_news_articles_by_genre(genre):
    # Query Elasticsearch for articles in the given genre
    query = {
        "size": 1000,  # Fetch all articles
        "_source": ["message", "category", "article_vector"],
        "query": {
            "match": {
                "category": genre
            }
        }
    }
    response = es.search(index="news_articles", body=query)

    # Collect matching articles
    articles = []
    for hit in response["hits"]["hits"]:
        message = hit["_source"]["message"]
        category = hit["_source"]["category"]
        articles.append({"message": message, "category": category})

    return articles