from typing import Dict, List, Tuple
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
import re

class TextEditor:
    def __init__(self):
        self.filler_words = {
            'very', 'really', 'just', 'actually', 'basically', 'literally',
            'simply', 'totally', 'completely', 'absolutely', 'definitely',
            'certainly', 'probably', 'possibly', 'somewhat', 'rather'
        }
        
        self.writing_issues = {
            'passive_voice': {
                'pattern': r'\b(am|is|are|was|were|be|been|being)\s+\w+ed\b',
                'suggestion': 'Consider using active voice for clearer writing.'
            },
            'long_sentence': {
                'pattern': r'^.{50,}$',
                'suggestion': 'This sentence might be too long. Consider breaking it into smaller parts.'
            },
            'filler_word': {
                'pattern': r'\b(' + '|'.join(self.filler_words) + r')\b',
                'suggestion': 'Consider removing this filler word for more concise writing.'
            },
            'repeated_word': {
                'pattern': r'\b(\w+)\b.*\b\1\b',
                'suggestion': 'This word is repeated. Consider using a synonym.'
            }
        }
    
    def analyze_text(self, text: str) -> Dict:
        sentences = sent_tokenize(text)
        suggestions = []
        
        for sentence in sentences:
            sentence_suggestions = self._analyze_sentence(sentence)
            if sentence_suggestions:
                suggestions.extend(sentence_suggestions)
        
        return {
            'suggestions': suggestions,
            'total_suggestions': len(suggestions)
        }
    
    def _analyze_sentence(self, sentence: str) -> List[Dict]:
        suggestions = []
        
        if self._is_passive_voice(sentence):
            suggestions.append({
                'type': 'passive_voice',
                'text': sentence,
                'suggestion': self.writing_issues['passive_voice']['suggestion'],
                'severity': 'warning'
            })
        
        if len(sentence) > 50:
            suggestions.append({
                'type': 'long_sentence',
                'text': sentence,
                'suggestion': self.writing_issues['long_sentence']['suggestion'],
                'severity': 'info'
            })
        
        words = word_tokenize(sentence.lower())
        filler_words = [word for word in words if word in self.filler_words]
        if filler_words:
            suggestions.append({
                'type': 'filler_word',
                'text': sentence,
                'suggestion': f'Consider removing these filler words: {", ".join(filler_words)}',
                'severity': 'info'
            })
        
        repeated_words = self._find_repeated_words(sentence)
        if repeated_words:
            suggestions.append({
                'type': 'repeated_word',
                'text': sentence,
                'suggestion': f'These words are repeated: {", ".join(repeated_words)}',
                'severity': 'info'
            })
        
        return suggestions
    
    def _is_passive_voice(self, sentence: str) -> bool:
        words = word_tokenize(sentence)
        pos_tags = pos_tag(words)
        
        for i in range(len(pos_tags) - 2):
            if (pos_tags[i][1] == 'VBD' and
                pos_tags[i][0].lower() in {'was', 'were'} and
                i + 1 < len(pos_tags) and
                pos_tags[i + 1][1].startswith('V')):
                return True
            
            if (pos_tags[i][1] == 'VBZ' and
                pos_tags[i][0].lower() in {'is', 'are'} and
                i + 1 < len(pos_tags) and
                pos_tags[i + 1][1].startswith('V')):
                return True
            
            if (pos_tags[i][1] == 'VBZ' and
                pos_tags[i][0].lower() in {'has', 'have'} and
                i + 1 < len(pos_tags) and
                pos_tags[i + 1][0].lower() == 'been' and
                i + 2 < len(pos_tags) and
                pos_tags[i + 2][1].startswith('V')):
                return True
        
        return False
    
    def _find_repeated_words(self, sentence: str) -> List[str]:
        words = word_tokenize(sentence.lower())
        word_count = {}
        repeated = []
        
        for word in words:
            if word.isalnum(): 
                word_count[word] = word_count.get(word, 0) + 1
                if word_count[word] == 2: 
                    repeated.append(word)
        
        return repeated 
