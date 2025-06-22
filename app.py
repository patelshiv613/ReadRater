from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from pdf_processor import PDFProcessor
from text_analyzer import TextAnalyzer
from text_editor import TextEditor
import plotly.graph_objects as go
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

pdf_processor = PDFProcessor()
text_analyzer = TextAnalyzer()
text_editor = TextEditor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are supported'}), 400
    
    text = pdf_processor.extract_text(file)
    if not text:
        return jsonify({'error': 'Could not extract text from PDF'}), 400
    
    analysis = text_analyzer.analyze_text(text)
    
    suggestions = text_editor.analyze_text(text)
    
    fig = create_visualization(analysis)
    
    return jsonify({
        'analysis': analysis,
        'suggestions': suggestions,
        'visualization': fig.to_json()
    })

@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    """Endpoint for live text analysis."""
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    suggestions = text_editor.analyze_text(text)
    
    return jsonify(suggestions)

def create_visualization(analysis):
    """Create a bar chart of sentence clarity scores."""
    sentences = analysis['sentence_analysis']
    scores = [s['readability_score'] for s in sentences]
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(range(1, len(sentences) + 1)),
            y=scores,
            marker_color=['green' if s >= 80 else 'orange' if s >= 60 else 'red' for s in scores]
        )
    ])
    
    fig.update_layout(
        title='Sentence Readability Scores',
        xaxis_title='Sentence Number',
        yaxis_title='Flesch Reading Ease Score',
        showlegend=False
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True) 
