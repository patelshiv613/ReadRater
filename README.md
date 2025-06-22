# ReadRater# ReadRater - PDF Readability Analyzer

ReadRater is a web application that analyzes the readability and writing quality of PDF documents. It provides detailed feedback on sentence structure, passive voice usage, filler words, and overall readability scores.

## Features

- PDF text extraction and analysis
- Flesch-Kincaid readability scoring
- Passive voice detection
- Filler word identification
- Sentence-by-sentence analysis
- Interactive visualization of readability scores
- Modern, responsive web interface

## Requirements

- Python 3.8 or higher
- Flask
- PyPDF2
- NLTK
- textstat
- plotly
- Other dependencies listed in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd readrater
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download required NLTK data:
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Upload a PDF file by either:
   - Dragging and dropping it onto the upload area
   - Clicking the "Choose File" button

4. Wait for the analysis to complete. The results will show:
   - Overall document statistics
   - Interactive visualization of sentence readability
   - Detailed sentence-by-sentence analysis

## Analysis Metrics

- **Flesch Reading Ease Score**: Higher scores indicate easier reading (0-100)
- **Flesch-Kincaid Grade Level**: Approximate U.S. grade level required to understand the text
- **Passive Voice Percentage**: Percentage of sentences using passive voice
- **Filler Words**: Percentage of filler words in the text
- **Sentence Length**: Average number of words per sentence

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
