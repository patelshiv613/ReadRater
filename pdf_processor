from PyPDF2 import PdfReader
import re
from typing import Optional

class PDFProcessor:
    def __init__(self):
        self.page_number_pattern = re.compile(r'^\s*\d+\s*$')
        self.header_footer_pattern = re.compile(r'^\s*[A-Za-z\s]+\s*$')
    
    def extract_text(self, pdf_file) -> Optional[str]:
     
        try:
            pdf_reader = PdfReader(pdf_file)
            
            if len(pdf_reader.pages) == 0:
                return None
            
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            cleaned_text = self._clean_text(text)
            return cleaned_text if cleaned_text.strip() else None
            
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return None
    
    def _clean_text(self, text: str) -> str:
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            if not line.strip():
                continue
                
            if self.page_number_pattern.match(line):
                continue
                
            if self.header_footer_pattern.match(line):
                continue
                
            cleaned_lines.append(line)
        
        cleaned_text = ' '.join(cleaned_lines)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        
        return cleaned_text.strip() 
