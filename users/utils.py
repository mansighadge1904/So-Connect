HOBBY_SYNONYMS = {
    "roaming": "travelling",
    "pics": "photography",
    "cinema": "movies",
    "reading": "books",
    "music": "songs",
    "swimming": "water sports",
    "painting": "art",
    "dancing": "ballet",
    "fishing": "angling",
    "cycling": "biking",
    "hiking": "trekking",
    "gaming": "video games",
    "skateboarding": "skating",
    "baking": "cooking",
    "camping": "outdoor activities",
    "coding": "programming",
    "blogging": "writing",
    "gardening": "plant care",
    "surfing": "water sports",
    "volunteering": "charity work",
    "photography": "pictures",
    "sailing": "boating",
    "horse riding": "equestrian",
    "rock climbing": "mountaineering",
    "skiing": "snow sports",
    "yoga": "meditation",
    "martial arts": "self-defense",
    "vlogging": "video blogging",
    "fashion": "style",
    "collecting": "hobby collecting",
    "bird watching": "ornithology",
    "language learning": "learning languages",
    "astronomy": "stargazing",
    "pottery": "clay crafting",
    "chess": "board games",
    "fencing": "sword fighting",
}

def normalize_hobbies(hobby_list):
    """
    Accepts a list of user-entered hobby names.
    Returns a list of (normalized, display) tuples.
    """
    normalized = []
    for hobby in hobby_list:
        key = hobby.lower()
        normalized_name = HOBBY_SYNONYMS.get(key, key)
        normalized.append((normalized_name, hobby))
    return normalized
