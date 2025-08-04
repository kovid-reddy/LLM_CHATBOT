"""
Multi-Language Translator Tool for Agentic AI System
Handles translations between English and multiple languages using Gemini API
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()



class MultiLanguageTranslator:
    """
    Multi-language translator class that uses Gemini API for real-time translation
    with fallback to static dictionary
    """
    
    def __init__(self):
        """Initialize the translator with Gemini API"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.use_gemini = False
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.use_gemini = True
                print("✅ Multi-language Gemini translator initialized successfully")
            except Exception as e:
                print(f"⚠  Gemini initialization failed: {e}")
                print("📚 Falling back to static dictionary")
        else:
            print("📚 Using static dictionary (no API key found)")
    
    def translate_with_gemini(self, text: str, target_language: str) -> str:
        """
        Translate text to target language using Gemini API
        
        Args:
            text (str): Text to translate
            target_language (str): Target language (e.g., "German", "Japanese", "Spanish")
            
        Returns:
            str: Translation
        """
        try:
            prompt = f"""Translate the following English text to {target_language}. 
            Provide only the {target_language} translation, nothing else.
            
            English: "{text}"
            {target_language}:"""
            
            response = self.model.generate_content(prompt)
            translation = response.text.strip()
            
            # Clean up the response (remove quotes if present)
            translation = translation.strip('"\'')
            
            return translation
            
        except Exception as e:
            print(f"⚠  Gemini translation failed: {e}")
            return None
    
    def translate_to_language(self, english_text: str, target_language: str = "German") -> str:
        """
        Translate English text to target language using Gemini API
        
        Args:
            english_text (str): English text to translate
            target_language (str): Target language (default: German)
            
        Returns:
            str: Translation
        """
        if not english_text:
            return ""
        
        # Clean and normalize the input
        cleaned_text = english_text.strip()
        
        # Use Gemini API for translation
        if self.use_gemini:
            gemini_translation = self.translate_with_gemini(cleaned_text, target_language)
            if gemini_translation:
                return gemini_translation
        
        # If Gemini API is not available, return error message
        return f"Translation failed: Gemini API not available"
    
    def translate_to_german(self, english_text: str) -> str:
        """
        Translate English text to German (backward compatibility)
        
        Args:
            english_text (str): English text to translate
            
        Returns:
            str: German translation
        """
        return self.translate_to_language(english_text, "German")
    
    def translate_to_japanese(self, english_text: str) -> str:
        """
        Translate English text to Japanese
        
        Args:
            english_text (str): English text to translate
            
        Returns:
            str: Japanese translation
        """
        return self.translate_to_language(english_text, "Japanese")
    
    def translate_to_spanish(self, english_text: str) -> str:
        """
        Translate English text to Spanish
        
        Args:
            english_text (str): English text to translate
            
        Returns:
            str: Spanish translation
        """
        return self.translate_to_language(english_text, "Spanish")
    
    def translate_to_french(self, english_text: str) -> str:
        """
        Translate English text to French
        
        Args:
            english_text (str): English text to translate
            
        Returns:
            str: French translation
        """
        return self.translate_to_language(english_text, "French")
    
    def get_available_translations(self) -> list:
        """
        Get a list of all available English phrases that can be translated.
        
        Returns:
            list: List of available English phrases (empty since using Gemini API)
        """
        return []
    
    def add_translation(self, english: str, german: str) -> None:
        """
        Add a new translation to the dictionary (deprecated - using Gemini API).
        
        Args:
            english (str): English phrase
            german (str): German translation
        """
        print("⚠  Dictionary translations are deprecated. Using Gemini API for all translations.")
    
    def get_translation_method(self) -> str:
        """
        Get the current translation method being used
        
        Returns:
            str: "Gemini API" or "Static Dictionary"
        """
        return "Gemini API" if self.use_gemini else "Static Dictionary"
    
    def get_supported_languages(self) -> list:
        """
        Get list of supported languages
        
        Returns:
            list: List of supported languages
        """
        return ["German", "Japanese", "Spanish", "French", "Italian", "Portuguese", "Russian", "Chinese", "Korean", "Arabic"]

# Global translator instance
translator = MultiLanguageTranslator()

# Convenience functions for backward compatibility
def translate_to_german(english_text: str) -> str:
    """Translate English text to German"""
    return translator.translate_to_german(english_text)

def translate_to_japanese(english_text: str) -> str:
    """Translate English text to Japanese"""
    return translator.translate_to_japanese(english_text)

def translate_to_language(english_text: str, target_language: str) -> str:
    """Translate English text to any supported language"""
    return translator.translate_to_language(english_text, target_language)

def get_available_translations() -> list:
    """Get available translations"""
    return translator.get_available_translations()

def add_translation(english: str, german: str) -> None:
    """Add a new translation"""
    translator.add_translation(english, german)

if __name__ == "__main__":
    # Test the translator functions
    print("Testing Multi-Language Translator Tool:")
    print(f"Translation Method: {translator.get_translation_method()}")
    print(f"Supported Languages: {', '.join(translator.get_supported_languages())}")
    print()
    
    test_phrases = [
        "Good Morning",
        "Hello",
        "Thank you",
        "How are you today?",
        "I love this weather"
    ]
    
    languages = ["German", "Japanese", "Spanish", "French"]
    
    for language in languages:
        print(f"\n🌍 {language} Translations:")
        for phrase in test_phrases:
            result = translate_to_language(phrase, language)
            print(f"  '{phrase}' → {result}")
    
    print(f"\nUsing Gemini API for all translations")