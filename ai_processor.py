from transformers import pipeline

# Load models
def load_models():
    try:
        print("Loading models...")
        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        print("Models loaded successfully!")
        return classifier, summarizer
    except Exception as e:
        print(f"Error loading models: {e}")
        return None, None

# Initialize models
classifier, summarizer = load_models()

def post_process_classification(description, ai_label):
    """
    Reinforce AI classification with manual rules for better accuracy.
    """
    if "promotion" in description.lower() or "raise" in description.lower():
        return "Promotion Request"
    elif "schedule" in description.lower() or "work hours" in description.lower():
        return "Change of Work Schedule Request"
    return ai_label

# Function to classify a document
def classify_document(description):
    try:
        print("Classifying document...")
        candidate_labels = ["Promotion Request", "Change of Work Schedule Request", "Report", "Invoice"]
        
        if not description or len(description.strip()) < 5:
            print("Invalid description provided.")
            return "Uncategorized"

        result = classifier(description, candidate_labels)
        print("Classification Result:", result)

        # Use the top-scoring label
        top_label = result['labels'][0]
        top_score = result['scores'][0]

        # Apply post-processing rules
        processed_label = post_process_classification(description, top_label)
        print(f"Top Label: {processed_label}, Confidence: {top_score}")

        return processed_label if top_score >= 0.5 else "Uncategorized"
    except Exception as e:
        print(f"Error during classification: {e}")
        return "Uncategorized"

# Function to summarize a document
'''
def summarize_document(description):
    try:
        print("Summarizing document...")
        if len(description.split()) < 30:
            return description  # No need for summarization

        summary = summarizer(description, max_length=50, min_length=20, do_sample=False)
        return summary[0]['summary_text'] if 'summary_text' in summary[0] else "Summary not available"
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Summary not available"
'''
#  to summarize a document
def summarize_document(description):
    try:
        if len(description.split()) < 30:
            return description  # Return description directly for short text
        summary = summarizer(description, max_length=50, min_length=20, do_sample=False)
        if summary and isinstance(summary, list) and 'summary_text' in summary[0]:
            return summary[0]['summary_text']
        else:
            return "Summary not available"
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Summary not available"
