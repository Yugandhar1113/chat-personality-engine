"""
Main Application Runner

Demonstrates the memory extraction and personality engine system.
Shows extracted memory, before/after personality transformations, and outputs JSON.
"""

from messages import MESSAGES
from memory_extractor import MemoryExtractor
from personality_engine import PersonalityEngine


def print_section(title: str, char: str = "=", width: int = 80):
    """Print a formatted section header."""
    print("\n" + char * width)
    print(f"  {title}")
    print(char * width + "\n")


def print_memory(memory: dict):
    """Print extracted memory in a readable format."""
    print("[MEMORY] EXTRACTED MEMORY")
    print("-" * 80)
    
    # Personal Facts
    if 'personal_facts' in memory and memory['personal_facts']:
        print("\n[PERSON] Personal Facts:")
        facts = memory['personal_facts']
        for key, value in facts.items():
            if value:
                if isinstance(value, list):
                    if value:
                        print(f"   * {key.replace('_', ' ').title()}: {', '.join(str(v) for v in value)}")
                else:
                    print(f"   * {key.replace('_', ' ').title()}: {value}")
    
    # Preferences
    if 'preferences' in memory:
        print("\n[PREFERENCES] Preferences:")
        prefs = memory['preferences']
        if prefs.get('likes'):
            print(f"   * Likes: {', '.join(prefs['likes'][:5])}")  # Show first 5
        if prefs.get('dislikes'):
            print(f"   * Dislikes: {', '.join(prefs['dislikes'][:5])}")  # Show first 5
        if prefs.get('favorites'):
            print(f"   * Favorites: {', '.join(prefs['favorites'][:5])}")  # Show first 5
    
    # Emotional Patterns
    if 'emotional_patterns' in memory:
        print("\n[EMOTIONS] Emotional Patterns:")
        emotions = memory['emotional_patterns']
        if emotions.get('emotion_counts'):
            print(f"   * Emotion Counts: {emotions['emotion_counts']}")
        if emotions.get('dominant_emotion'):
            print(f"   * Dominant Emotion: {emotions['dominant_emotion']}")
        if emotions.get('total_emotional_messages'):
            print(f"   * Total Emotional Messages: {emotions['total_emotional_messages']}")


def demonstrate_personality_improvement():
    """Demonstrate before and after personality transformations."""
    print_section("PERSONALITY ENGINE DEMONSTRATION")
    
    # Sample base response (before personality)
    base_response = """I understand you're feeling stressed about your upcoming deadline. 
You should break down your project into smaller tasks and prioritize them. 
It's important to take breaks and manage your time effectively. 
I recommend creating a schedule and sticking to it."""
    
    print("[BEFORE] Generic Response:")
    print("-" * 80)
    print(base_response)
    print()
    
    # Extract memory first
    extractor = MemoryExtractor()
    memory = extractor.extract_all(MESSAGES)
    
    # Initialize personality engine with memory
    engine = PersonalityEngine(memory)
    
    # Get all personality variations
    variations = engine.demonstrate_improvement(base_response)
    
    # Display each style
    styles = [
        ('calm_mentor', '[CALM MENTOR] Calm Mentor Style'),
        ('witty_friend', '[WITTY FRIEND] Witty Friend Style'),
        ('therapist', '[THERAPIST] Therapist Style')
    ]
    
    for style_key, style_name in styles:
        print_section(style_name, char="-", width=80)
        print(variations[style_key])
        print()


def main():
    """Main application entry point."""
    print_section("MEMORY EXTRACTION & PERSONALITY ENGINE DEMO")
    
    # Step 1: Extract memory from messages
    print_section("STEP 1: EXTRACTING MEMORY FROM 30 CHAT MESSAGES")
    
    extractor = MemoryExtractor()
    memory = extractor.extract_all(MESSAGES)
    
    # Display extracted memory
    print_memory(memory)
    
    # Step 2: Output memory as JSON
    print_section("STEP 2: MEMORY IN JSON FORMAT")
    json_output = extractor.to_json(memory)
    print(json_output)
    
    # Step 3: Demonstrate personality improvements
    print_section("STEP 3: PERSONALITY ENGINE - BEFORE & AFTER")
    demonstrate_personality_improvement()
    
    # Summary
    print_section("SUMMARY")
    print("[SUCCESS] Successfully extracted memory from 30 chat messages")
    print("[SUCCESS] Identified personal facts, preferences, and emotional patterns")
    print("[SUCCESS] Demonstrated personality engine with 3 different styles:")
    print("   * Calm Mentor: Supportive and wise")
    print("   * Witty Friend: Playful and humorous")
    print("   * Therapist: Empathetic and reflective")
    print("\n[COMPLETE] Demo complete!")


if __name__ == "__main__":
    main()

