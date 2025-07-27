#!/usr/bin/env python3
"""
Test script for bilingual keyword extraction
"""

import re

def extract_keywords(query):
    """Extract relevant keywords from user query with multilingual support"""
    # Remove common words and extract meaningful terms
    stop_words = {
        # English stop words
        'the', 'is', 'at', 'which', 'on', 'what', 'where', 'when', 'how', 'why', 'who', 
        'a', 'an', 'and', 'or', 'but', 'in', 'of', 'to', 'for', 'with', 'by', 'me', 'show',
        'tell', 'about', 'from', 'all', 'any', 'some', 'data', 'information',
        # Telugu common words (basic ones)
        'అని', 'కి', 'ను', 'లో', 'నా', 'మా', 'వాళ్ళ', 'గురించి', 'చెప్పు'
    }
    
    # Clean and split query - preserve Telugu characters
    query_clean = re.sub(r'[^\w\s\u0C00-\u0C7F]', ' ', query.lower())
    words = [word.strip() for word in query_clean.split() if len(word.strip()) > 1]
    
    # Filter out stop words
    keywords = [word for word in words if word not in stop_words]
    
    # Add the full query for exact matching
    keywords.append(query.lower().strip())
    
    # Enhanced bilingual keyword mapping
    query_variations = []
    query_lower = query.lower()
    
    # Comprehensive plant/tree translations
    plant_translations = {
        # Jammi tree variations
        'jammi': ['jammi', 'జమ్మి', 'prosopis', 'cineraria', 'shami', 'khejri'],
        'జమ్మి': ['jammi', 'జమ్మి', 'prosopis', 'cineraria', 'shami', 'khejri'],
        'prosopis': ['jammi', 'జమ్మి', 'prosopis', 'cineraria'],
        'shami': ['jammi', 'జమ్మి', 'shami', 'prosopis'],
        
        # Neem tree variations
        'neem': ['neem', 'వేప', 'vepa', 'azadirachta', 'indica', 'margosa'],
        'వేప': ['neem', 'వేప', 'vepa', 'azadirachta', 'indica', 'margosa'],
        'vepa': ['neem', 'వేప', 'vepa', 'azadirachta', 'indica'],
        'azadirachta': ['neem', 'వేప', 'azadirachta', 'indica'],
    }
    
    # Add plant-specific translations
    for word in keywords:
        if word in plant_translations:
            query_variations.extend(plant_translations[word])
    
    # Generic tree/plant keywords with translations
    tree_keywords = ['చెట్టు', 'tree', 'plant', 'వృక్షం', 'మొక్క']
    if any(keyword in query_lower for keyword in tree_keywords):
        query_variations.extend(tree_keywords)
    
    # Media request keywords with translations
    media_keywords = {
        'image': ['image', 'images', 'photo', 'picture', 'చిత్రం', 'ఫోటో'],
        'images': ['image', 'images', 'photo', 'picture', 'చిత్రాలు', 'ఫోటోలు'],
        'photo': ['image', 'images', 'photo', 'picture', 'చిత్రం', 'ఫోటో'],
        'picture': ['image', 'images', 'photo', 'picture', 'చిత్రం', 'ఫోటో'],
        'చిత్రం': ['image', 'images', 'photo', 'picture', 'చిత్రం', 'ఫోటో'],
        'చిత్రాలు': ['image', 'images', 'photo', 'picture', 'చిత్రాలు', 'ఫోటోలు'],
        'ఫోటో': ['image', 'images', 'photo', 'picture', 'చిత్రం', 'ఫోటో'],
    }
    
    for word in keywords:
        if word in media_keywords:
            query_variations.extend(media_keywords[word])
    
    keywords.extend(query_variations)
    
    return list(set(keywords))  # Remove duplicates

if __name__ == "__main__":
    # Test queries
    test_queries = [
        ("Telugu: జమ్మి చెట్టు చిత్రాలు చూపించు", "జమ్మి చెట్టు చిత్రాలు చూపించు"),
        ("English: show jammi tree images", "show jammi tree images"),
        ("Telugu: వేప చెట్టు ఫోటోలు", "వేప చెట్టు ఫోటోలు"),
        ("English: neem tree photos", "neem tree photos"),
    ]
    
    print("🧪 Testing Bilingual Keyword Extraction\n")
    
    for description, query in test_queries:
        print(f"Query: {description}")
        keywords = extract_keywords(query)
        print(f"Keywords: {keywords}")
        print("-" * 50)
    
    # Test if Telugu and English queries for same thing share keywords
    telugu_jammi = extract_keywords("జమ్మి చెట్టు చిత్రాలు చూపించు")
    english_jammi = extract_keywords("show jammi tree images")
    
    common_jammi = set(telugu_jammi) & set(english_jammi)
    
    print(f"\n🔍 Comparison for Jammi Tree Images:")
    print(f"Telugu keywords: {telugu_jammi}")
    print(f"English keywords: {english_jammi}")
    print(f"Common keywords: {list(common_jammi)}")
    
    if len(common_jammi) >= 3:
        print("✅ Good bilingual coverage - both queries share multiple keywords!")
    else:
        print("❌ Poor bilingual coverage - queries don't share enough keywords")
