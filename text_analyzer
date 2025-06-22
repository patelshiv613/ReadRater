import nltk
import textstat
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
import re
from typing import Dict, List, Tuple
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

class TextAnalyzer:
    def __init__(self):
        self.filler_words = {
            'very', 'really', 'just', 'actually', 'basically', 'literally',
            'simply', 'totally', 'completely', 'absolutely', 'definitely',
            'certainly', 'probably', 'possibly', 'somewhat', 'rather'
        }
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        
    def analyze_text(self, text: str) -> Dict:
        sentences = sent_tokenize(text)
        
        # Basic metrics
        total_sentences = len(sentences)
        total_words = len(word_tokenize(text))
        avg_sentence_length = total_words / total_sentences if total_sentences > 0 else 0
        
        # Readability scores
        flesch_score = textstat.flesch_reading_ease(text)
        flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
        
        # Generate word cloud
        word_cloud = self._generate_word_cloud(text)
        
        sentence_analysis = []
        passive_count = 0
        filler_count = 0
        
        for sentence in sentences:
            words = word_tokenize(sentence)
            pos_tags = pos_tag(words)
            
            is_passive = self._is_passive_voice(pos_tags)
            if is_passive:
                passive_count += 1
            
            sentence_filler_count = sum(1 for word in words if word.lower() in self.filler_words)
            filler_count += sentence_filler_count
            
            sentence_length = len(words)
            sentence_score = textstat.flesch_reading_ease(sentence)
            
            sentence_analysis.append({
                'text': sentence,
                'length': sentence_length,
                'is_passive': is_passive,
                'filler_words': sentence_filler_count,
                'readability_score': sentence_score,
                'clarity': self._get_clarity_level(sentence_score)
            })
        
        passive_percentage = (passive_count / total_sentences * 100) if total_sentences > 0 else 0
        filler_percentage = (filler_count / total_words * 100) if total_words > 0 else 0
        
        return {
            'summary': {
                'total_sentences': total_sentences,
                'total_words': total_words,
                'avg_sentence_length': round(avg_sentence_length, 2),
                'flesch_score': round(flesch_score, 2),
                'flesch_kincaid_grade': round(flesch_kincaid_grade, 2),
                'passive_percentage': round(passive_percentage, 2),
                'filler_percentage': round(filler_percentage, 2)
            },
            'sentence_analysis': sentence_analysis,
            'word_cloud': word_cloud
        }
    
    def _generate_word_cloud(self, text: str) -> str:
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalnum() and word not in self.stop_words]
        
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            max_words=100,
            contour_width=3,
            contour_color='steelblue'
        ).generate(' '.join(words))
        
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        plt.close()
        buf.seek(0)
        
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        return img_str
    
    def _is_passive_voice(self, pos_tags: List[Tuple[str, str]]) -> bool:
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
    
    def _get_clarity_level(self, score: float) -> str:
        if score >= 80:
            return 'High'
        elif score >= 60:
            return 'Medium'
        else:
            return 'Low' 
