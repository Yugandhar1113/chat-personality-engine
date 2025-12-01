"""
Memory Extractor Module

Extracts structured memory from user chat messages including:
- User preferences (likes, dislikes, favorites)
- Emotional patterns (dominant emotions, emotion counts)
- Important personal facts (name, city, job role, birthday, etc.)
"""

import re
from collections import Counter
from typing import Dict, List, Any
import json


class MemoryExtractor:
    """Extracts and structures memory from chat messages."""
    
    def __init__(self):
        # Emotion keywords mapping
        self.emotion_keywords = {
            'happy': ['happy', 'excited', 'proud', 'grateful', 'joy', 'joyful', 'thrilled', 'delighted'],
            'sad': ['sad', 'miss', 'depressed', 'down', 'unhappy', 'melancholy'],
            'anxious': ['anxious', 'worried', 'stressed', 'nervous', 'fear', 'afraid', 'concerned'],
            'frustrated': ['frustrated', 'annoyed', 'irritated', 'angry', 'mad', 'upset'],
            'calm': ['calm', 'peaceful', 'relaxed', 'serene', 'tranquil', 'content']
        }
        
        # Preference indicators
        self.like_indicators = ['love', 'enjoy', 'like', 'prefer', 'favorite', 'favourite', 'adore', 'appreciate']
        self.dislike_indicators = ['hate', 'dislike', 'don\'t like', 'can\'t stand', 'detest', 'loathe']
    
    def extract_personal_facts(self, messages: List[str]) -> Dict[str, Any]:
        """
        Extract personal facts from messages.
        
        Looks for:
        - Name
        - City/Location
        - Job role/occupation
        - Birthday
        - Age
        - Allergies/Medical info
        - Dietary preferences
        """
        facts = {
            'name': None,
            'city': None,
            'location': None,
            'job_role': None,
            'company': None,
            'birthday': None,
            'age': None,
            'allergies': [],
            'dietary_preferences': [],
            'other_facts': []
        }
        
        # Name extraction (usually in first message or "My name is..." pattern)
        name_patterns = [
            r"my name is ([A-Z][a-z]+)",
            r"i'm ([A-Z][a-z]+)",
            r"i am ([A-Z][a-z]+)",
            r"name is ([A-Z][a-z]+)"
        ]
        
        # Location extraction
        location_patterns = [
            r"from ([A-Z][a-zA-Z\s]+)",
            r"live in ([A-Z][a-zA-Z\s]+)",
            r"in ([A-Z][a-zA-Z\s]+),"
        ]
        
        # Job extraction
        job_patterns = [
            r"work as (?:a |an )?([a-z\s]+) (?:at|for) ([A-Z][a-zA-Z\s]+)",
            r"i'm (?:a |an )?([a-z\s]+) (?:at|for) ([A-Z][a-zA-Z\s]+)",
            r"i am (?:a |an )?([a-z\s]+) (?:at|for) ([A-Z][a-zA-Z\s]+)"
        ]
        
        # Birthday extraction
        birthday_patterns = [
            r"birthday is (?:on )?([A-Z][a-z]+\s\d{1,2}(?:st|nd|rd|th)?,?\s\d{4})",
            r"born (?:on )?([A-Z][a-z]+\s\d{1,2}(?:st|nd|rd|th)?,?\s\d{4})"
        ]
        
        # Age extraction
        age_patterns = [
            r"turning (\d+)",
            r"i'm (\d+)",
            r"i am (\d+)",
            r"age of (\d+)"
        ]
        
        for message in messages:
            message_lower = message.lower()
            
            # Extract name
            if not facts['name']:
                for pattern in name_patterns:
                    match = re.search(pattern, message, re.IGNORECASE)
                    if match:
                        facts['name'] = match.group(1)
                        break
            
            # Extract location
            if not facts['city']:
                for pattern in location_patterns:
                    match = re.search(pattern, message, re.IGNORECASE)
                    if match:
                        location = match.group(1).strip()
                        # Filter out common false positives
                        if location not in ['The', 'A', 'An'] and len(location) > 2:
                            facts['city'] = location
                            facts['location'] = location
                            break
            
            # Extract job
            if not facts['job_role']:
                for pattern in job_patterns:
                    match = re.search(pattern, message, re.IGNORECASE)
                    if match:
                        facts['job_role'] = match.group(1).strip()
                        if len(match.groups()) > 1:
                            facts['company'] = match.group(2).strip()
                        break
            
            # Extract birthday
            if not facts['birthday']:
                for pattern in birthday_patterns:
                    match = re.search(pattern, message, re.IGNORECASE)
                    if match:
                        facts['birthday'] = match.group(1).strip()
                        break
            
            # Extract age
            if not facts['age']:
                for pattern in age_patterns:
                    match = re.search(pattern, message, re.IGNORECASE)
                    if match:
                        try:
                            facts['age'] = int(match.group(1))
                        except:
                            pass
                        break
            
            # Extract allergies
            if 'allergic' in message_lower:
                allergy_match = re.search(r"allergic to ([^.]+)", message_lower)
                if allergy_match:
                    allergies = [a.strip() for a in allergy_match.group(1).split('and')]
                    facts['allergies'].extend(allergies)
            
            # Extract dietary preferences
            if 'vegetarian' in message_lower or 'vegan' in message_lower:
                if 'vegetarian' in message_lower:
                    facts['dietary_preferences'].append('vegetarian')
                if 'vegan' in message_lower:
                    facts['dietary_preferences'].append('vegan')
        
        # Clean up None values
        facts = {k: v for k, v in facts.items() if v or (isinstance(v, list) and len(v) > 0)}
        
        return facts
    
    def extract_preferences(self, messages: List[str]) -> Dict[str, List[str]]:
        """
        Extract user preferences (likes, dislikes, favorites) from messages.
        
        Returns:
            Dictionary with 'likes', 'dislikes', and 'favorites' lists
        """
        preferences = {
            'likes': [],
            'dislikes': [],
            'favorites': []
        }
        
        for message in messages:
            message_lower = message.lower()
            
            # Extract likes
            for indicator in self.like_indicators:
                if indicator in message_lower:
                    # Extract the object of liking
                    pattern = rf"{indicator}(?:\s+(?:the|a|an))?\s+([^.!?]+?)(?:\.|!|$)"
                    match = re.search(pattern, message_lower)
                    if match:
                        liked_item = match.group(1).strip()
                        # Clean up common phrases
                        liked_item = re.sub(r'\s+(especially|like|such as)', '', liked_item)
                        if len(liked_item) > 2 and liked_item not in preferences['likes']:
                            preferences['likes'].append(liked_item)
            
            # Extract dislikes
            for indicator in self.dislike_indicators:
                if indicator in message_lower:
                    pattern = rf"{indicator}(?:\s+(?:the|a|an))?\s+([^.!?]+?)(?:\.|!|$)"
                    match = re.search(pattern, message_lower)
                    if match:
                        disliked_item = match.group(1).strip()
                        if len(disliked_item) > 2 and disliked_item not in preferences['dislikes']:
                            preferences['dislikes'].append(disliked_item)
            
            # Extract favorites
            if 'favorite' in message_lower or 'favourite' in message_lower:
                pattern = r"favorite(?:ite)? (?:is|are)?\s+([^.!?]+?)(?:\.|!|$)"
                match = re.search(pattern, message_lower)
                if match:
                    favorite_item = match.group(1).strip()
                    if len(favorite_item) > 2:
                        preferences['favorites'].append(favorite_item)
        
        return preferences
    
    def extract_emotions(self, messages: List[str]) -> Dict[str, Any]:
        """
        Extract emotional patterns from messages.
        
        Returns:
            Dictionary with emotion counts and dominant emotion
        """
        emotion_counts = Counter()
        
        for message in messages:
            message_lower = message.lower()
            
            # Check for each emotion type
            for emotion, keywords in self.emotion_keywords.items():
                for keyword in keywords:
                    if keyword in message_lower:
                        emotion_counts[emotion] += 1
                        break  # Count each message only once per emotion
        
        # Determine dominant emotion
        dominant_emotion = emotion_counts.most_common(1)[0][0] if emotion_counts else None
        
        return {
            'emotion_counts': dict(emotion_counts),
            'dominant_emotion': dominant_emotion,
            'total_emotional_messages': sum(emotion_counts.values())
        }
    
    def extract_all(self, messages: List[str]) -> Dict[str, Any]:
        """
        Extract all memory components from messages.
        
        Returns:
            Complete memory structure with personal facts, preferences, and emotions
        """
        memory = {
            'personal_facts': self.extract_personal_facts(messages),
            'preferences': self.extract_preferences(messages),
            'emotional_patterns': self.extract_emotions(messages)
        }
        
        return memory
    
    def to_json(self, memory: Dict[str, Any], indent: int = 2) -> str:
        """Convert memory dictionary to JSON string."""
        return json.dumps(memory, indent=indent, ensure_ascii=False)

