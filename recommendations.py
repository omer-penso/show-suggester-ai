import numpy as np
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def get_user_vectors(user_shows, embeddings):
    """
    Retrieve the embedding vectors of the user-selected shows.
    """
    user_vectors = []
    for show in user_shows:
        vector = embeddings.get(show)
        if vector:
            user_vectors.append(vector)
        else:
            logger.error(f"Show '{show}' not found in embeddings dictionary.")
    return user_vectors


def compute_average_vector(vectors):
    """
    Compute the average of a list of vectors.
    """
    if not vectors:
        raise ValueError("No vectors provided to compute the average.")
    return np.mean(vectors, axis=0)


def cosine_similarity(vec1, vec2):
    """
    Compute the cosine similarity between two vectors.
    """
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)


def find_top_recommendations(average_vector, embeddings, user_shows, top_n=5):
    """
    Find the top N recommendations based on cosine similarity.
    """
    distances = []
    for show, vector in embeddings.items():
        if show in user_shows:  # Exclude user-selected shows
            continue
        similarity = cosine_similarity(average_vector, vector)
        distances.append((show, similarity))
    
    # Sort by similarity (highest first) and take the top N
    distances.sort(key=lambda x: x[1], reverse=True)
    top_recommendations = distances[:top_n]
    
    # Convert similarity to percentages
    recommendations_with_percentages = [
        (show, int(similarity * 100)) for show, similarity in top_recommendations
    ]
    return recommendations_with_percentages
