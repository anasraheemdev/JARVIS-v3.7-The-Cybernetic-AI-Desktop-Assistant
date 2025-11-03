"""
Advanced AI Features Module
Handles document summarization, translation, sentiment analysis, code generation, and debugging
"""

import logging
from typing import Dict, Optional, List
import json

logger = logging.getLogger(__name__)

class AdvancedAIModule:
    """Handles advanced AI-powered features"""
    
    def __init__(self, groq_agent=None, memory_module=None):
        self.groq_agent = groq_agent
        self.memory_module = memory_module
    
    def summarize_document(self, params: Dict) -> str:
        """Summarize a document or text using Groq AI"""
        try:
            text = params.get('text', '')
            max_length = params.get('max_length', 200)
            
            if not text:
                return "Error: No text provided for summarization"
            
            # Use Groq agent to summarize
            if not self.groq_agent:
                return "Groq agent not available for summarization"
            
            prompt = f"""Please provide a concise summary of the following text in approximately {max_length} words:

{text[:4000]}  # Limit input size

Summary:"""
            
            response, _ = self.groq_agent.process_query(prompt, language='en')
            return f"Summary ({max_length} words):\n{response}"
        
        except Exception as e:
            logger.error(f"Error summarizing document: {e}")
            return f"Error: {e}"
    
    def translate_text(self, params: Dict) -> str:
        """Translate text to another language using Groq AI"""
        try:
            text = params.get('text', '')
            target_language = params.get('target_language', 'urdu')
            source_language = params.get('source_language', 'english')
            
            if not text:
                return "Error: No text provided for translation"
            
            if not self.groq_agent:
                return "Groq agent not available for translation"
            
            prompt = f"""Translate the following text from {source_language} to {target_language}:

{text}

Translation:"""
            
            response, _ = self.groq_agent.process_query(prompt, language='en')
            return f"Translation ({source_language} → {target_language}):\n{response}"
        
        except Exception as e:
            logger.error(f"Error translating text: {e}")
            return f"Error: {e}"
    
    def analyze_sentiment(self, params: Dict) -> str:
        """Analyze sentiment of text using Groq AI"""
        try:
            text = params.get('text', '')
            
            if not text:
                return "Error: No text provided for sentiment analysis"
            
            if not self.groq_agent:
                return "Groq agent not available for sentiment analysis"
            
            prompt = f"""Analyze the sentiment of the following text. Respond with:
- Sentiment: positive, negative, or neutral
- Confidence: high, medium, or low
- Brief explanation

Text: {text}

Analysis:"""
            
            response, _ = self.groq_agent.process_query(prompt, language='en')
            return f"Sentiment Analysis:\n{response}"
        
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return f"Error: {e}"
    
    def generate_code(self, params: Dict) -> str:
        """Generate code based on description using Groq AI"""
        try:
            description = params.get('description', '')
            language = params.get('language', 'python')
            
            if not description:
                return "Error: No description provided for code generation"
            
            if not self.groq_agent:
                return "Groq agent not available for code generation"
            
            prompt = f"""Generate {language} code for the following task:

{description}

Provide complete, working code with comments:"""
            
            response, _ = self.groq_agent.process_query(prompt, language='en')
            
            # Return code - can be saved to file using code_module
            return f"Generated {language} code:\n\n{response}"
        
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            return f"Error: {e}"
    
    def debug_code(self, params: Dict) -> str:
        """Help debug code using Groq AI"""
        try:
            code = params.get('code', '')
            error_message = params.get('error', '')
            
            if not code:
                return "Error: No code provided for debugging"
            
            if not self.groq_agent:
                return "Groq agent not available for debugging"
            
            prompt = f"""Help debug the following code. {'Error message: ' + error_message if error_message else 'No specific error provided.'}

Code:
```python
{code}
```

Please identify issues and suggest fixes:"""
            
            response, _ = self.groq_agent.process_query(prompt, language='en')
            return f"Debugging Analysis:\n{response}"
        
        except Exception as e:
            logger.error(f"Error debugging code: {e}")
            return f"Error: {e}"

