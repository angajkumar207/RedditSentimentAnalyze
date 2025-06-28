import os
import matplotlib
import seaborn as sns
from wordcloud import WordCloud
import base64
from io import BytesIO
from collections import Counter
import re

matplotlib.use('Agg')
import matplotlib.pyplot as plt

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def generate_graphs(sentiment_results, topic):
    # Extract sentiment labels and scores
    sentiment = [result['sentiment'] for result in sentiment_results]
    scores = [result['score'] for result in sentiment_results]

    # Setup image output directory
    image_dir = os.path.join('static', 'image')
    create_directory(image_dir)

    bar_chart_path = os.path.join(image_dir, 'sentiment_bar_chart.png')
    word_chart_path = os.path.join(image_dir, 'word_cloud.png')

    # Generate sentiment bar chart
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=sentiment, y=scores, palette='coolwarm')
    plt.title(f'Sentiment Scores for Reddit Posts on "{topic}"', fontsize=16)
    plt.xlabel('Sentiment', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height:.2f}', 
                    (p.get_x() + p.get_width() / 2., height),
                    ha="center", va="bottom", fontsize=10,
                    xytext=(0, 5), textcoords='offset points')

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(bar_chart_path)
    plt.close()

    # Convert bar chart to base64
    bar_img_b64 = encode_image_to_base64(bar_chart_path)

    # Prepare text for word cloud
    text = ' '.join([result.get('content', '') for result in sentiment_results])
    text = re.sub(r'[^a-z\s]', '', text.lower())
    words = text.split()
    word_counts = Counter(words)

    # If word_counts is empty, skip word cloud
    if word_counts:
        wc = WordCloud(width=800, height=400, background_color='white',
                       max_words=200, colormap='viridis')
        wc.generate_from_frequencies(word_counts)
        wc.to_file(word_chart_path)
        word_cloud_b64 = encode_image_to_base64(word_chart_path)
    else:
        word_cloud_b64 = None  # or ''

    return bar_img_b64, word_cloud_b64

def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            img_64 = base64.b64encode(img_file.read()).decode('utf-8')
        return img_64
    except FileNotFoundError:
        print(f"⚠️ File not found: {image_path}")
        return ''
