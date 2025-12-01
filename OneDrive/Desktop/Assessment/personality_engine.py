"""
Personality Engine Module

Rewrites responses in different personality styles:
- Calm Mentor: Supportive, wise, encouraging
- Witty Friend: Playful, humorous, casual
- Therapist Style: Empathetic, reflective, non-judgmental
"""

from typing import Dict, Any, Optional


class PersonalityEngine:
    """Transforms responses based on different personality styles."""
    
    def __init__(self, memory: Optional[Dict[str, Any]] = None):
        """
        Initialize personality engine with optional user memory.
        
        Args:
            memory: Extracted memory dictionary for personalized responses
        """
        self.memory = memory or {}
    
    def get_user_name(self) -> str:
        """Get user's name from memory if available."""
        if self.memory and 'personal_facts' in self.memory:
            name = self.memory['personal_facts'].get('name')
            if name:
                return name
        return "there"
    
    def calm_mentor_style(self, base_response: str) -> str:
        """
        Transform response into calm mentor style.
        
        Characteristics:
        - Supportive and encouraging
        - Uses wisdom and experience
        - Calm, measured tone
        - Offers guidance without being pushy
        """
        user_name = self.get_user_name()
        
        # Add mentor-like opening phrases
        openings = [
            "I understand where you're coming from, and I'd like to share some perspective.",
            "That's a thoughtful observation. Let me offer some guidance.",
            "I appreciate you sharing that. Here's what I've learned that might help.",
            "You're on the right track. Consider this approach:"
        ]
        
        # Transform the response
        transformed = f"{openings[0]}\n\n{base_response}"
        
        # Add mentor-like closing
        closings = [
            "Remember, progress takes time, and you're doing great.",
            "Take it one step at a time, and trust the process.",
            "You have the strength to handle this. I believe in you.",
            "Keep moving forward, and don't hesitate to reach out if you need support."
        ]
        
        transformed += f"\n\n{closings[0]}"
        
        # Adjust tone: make it more supportive
        transformed = transformed.replace("I think", "I believe")
        # Handle "You should [verb]" -> "You might consider [verb]ing" for common verbs
        transformed = transformed.replace("You should break", "You might consider breaking")
        transformed = transformed.replace("You should take", "You might consider taking")
        transformed = transformed.replace("You should create", "You might consider creating")
        transformed = transformed.replace("You should", "You might consider")
        transformed = transformed.replace("You need to", "It would be helpful to")
        
        return transformed
    
    def witty_friend_style(self, base_response: str) -> str:
        """
        Transform response into witty friend style.
        
        Characteristics:
        - Playful and humorous
        - Casual and friendly
        - Uses jokes and light-hearted comments
        - Relatable and down-to-earth
        """
        user_name = self.get_user_name()
        
        # Add witty opening phrases
        openings = [
            f"Hey {user_name}! So here's the thing...",
            f"Okay {user_name}, let me break this down for you (in the most fun way possible):",
            f"Alright, {user_name}, time for some real talk (but make it fun):",
            f"Hey {user_name}! *cracks knuckles* Let's dive into this:"
        ]
        
        # Transform the response
        transformed = f"{openings[0]}\n\n{base_response}"
        
        # Add humor and casual language
        transformed = transformed.replace("I understand", "I totally get it")
        transformed = transformed.replace("You should", "You could totally")
        transformed = transformed.replace("It is important", "Here's the deal")
        transformed = transformed.replace("I recommend", "My two cents?")
        
        # Add witty closing
        closings = [
            "Hope that helps! You've got this!",
            "There you go! Now go be awesome!",
            "That's my take on it! Feel free to hit me up if you need anything else!",
            "Hope that made sense! You're doing great, keep it up!"
        ]
        
        transformed += f"\n\n{closings[0]}"
        
        return transformed
    
    def therapist_style(self, base_response: str) -> str:
        """
        Transform response into therapist style.
        
        Characteristics:
        - Empathetic and understanding
        - Reflective and non-judgmental
        - Uses open-ended questions
        - Validates feelings
        - Encourages self-discovery
        """
        user_name = self.get_user_name()
        
        # Add therapist-like opening phrases
        openings = [
            f"I hear you, {user_name}. Let's explore this together.",
            f"Thank you for sharing that with me, {user_name}. I want to understand better.",
            f"That sounds important to you, {user_name}. Can we unpack this a bit?",
            f"I appreciate you opening up about this, {user_name}. Let's look at what's happening here."
        ]
        
        # Transform the response
        transformed = f"{openings[0]}\n\n{base_response}"
        
        # Add validation and reflection
        transformed = transformed.replace("I think", "It seems like")
        transformed = transformed.replace("You should", "You might find it helpful to")
        transformed = transformed.replace("You need to", "What would it be like if you")
        
        # Add reflective questions
        reflective_questions = [
            "How does that feel to you?",
            "What comes up for you when you think about that?",
            "What would it mean for you if that changed?",
            "How would you like to move forward with this?"
        ]
        
        transformed += f"\n\n{reflective_questions[0]}"
        
        # Add therapist-like closing
        closings = [
            "There's no right or wrong answer here. What matters is what feels authentic to you.",
            "Take your time with this. There's no rush, and your feelings are valid.",
            "I'm here to support you as you navigate this. How would you like to proceed?",
            "Remember, this is your journey, and you're in control of the pace."
        ]
        
        transformed += f"\n\n{closings[0]}"
        
        return transformed
    
    def rewrite_response(self, base_response: str, style: str) -> str:
        """
        Rewrite a response in the specified personality style.
        
        Args:
            base_response: The original response to transform
            style: One of 'calm_mentor', 'witty_friend', 'therapist'
        
        Returns:
            Transformed response in the specified style
        """
        style = style.lower().replace(' ', '_')
        
        if style == 'calm_mentor':
            return self.calm_mentor_style(base_response)
        elif style == 'witty_friend':
            return self.witty_friend_style(base_response)
        elif style == 'therapist':
            return self.therapist_style(base_response)
        else:
            raise ValueError(f"Unknown style: {style}. Choose from: 'calm_mentor', 'witty_friend', 'therapist'")
    
    def demonstrate_improvement(self, base_response: str) -> Dict[str, str]:
        """
        Demonstrate before and after personality improvement.
        
        Args:
            base_response: The original response to transform
        
        Returns:
            Dictionary with 'before' and all style variations
        """
        return {
            'before': base_response,
            'calm_mentor': self.calm_mentor_style(base_response),
            'witty_friend': self.witty_friend_style(base_response),
            'therapist': self.therapist_style(base_response)
        }

