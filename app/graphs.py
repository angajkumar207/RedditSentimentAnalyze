import os
import matplotlib
import seaborn as sns
from wordcloud import wordcloud
import base64
from io import BytesIO
from collections import Counter
import re
matplotlib.use('Agg')
import matplotlib.pyplot as pit

def create_directory(path):
    if not os.exists(path):
        os.makedirs(path)

def generate_graphs(sentiment_results, topic):
    sentiment = [result['sentiment']for result in sentiment_results]
    scores = [result['score'] for result in sentiment_results]

    image_dir = os.path.join('static', 'image')
    create_directory(image_dir)

    bar_chart_path = os.path.join(image_dir, 'sentiment_bar_chart.png')
    word_chart_path = os.path.join(image_dir, 'word_cloud.pnge')

    pit.figure(figsize=(10,16))
    ax = sns.barplot(x= sentiment, y=scores, palette='Coolwarm')
    pit.title('Sentiment Scores for reddit Posts on "{topic}"',fontsize=16)
    pit.xlabel('Sentiment', fontsize=12)
    pit.ylabel('Score', fontsize=12)
    pit.xticks(rotation=45, ha = "right")
    pit.tight_layout()

    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}',
                    (p.get_x() + p.get_width()/2., p.get_hight()),
                    ha = "center", va = "conter", fontsize=12, colore="black",
                    xytext=(0,5), textcoords='offest points')
        pit.grid(True, linestyle='--',alpha=0.7)
        pit.savefig(bar_chart_path)
        pit.close()
    
    # converting bar chart
    bar_ing_64 = encode_image_to_base64(bar_chart_path)
    text = ' '.join([result['content'] for result in sentiment_results])

    #clean the text 
    text = re.sub(r'[A-Za-z\s]', '', text.lower())

    # token size
    words = text.split()
    word_counts = Counter(words)

    # generative the word cloud
    word_counts = wordcloud(width=800, hight=400, background_color='white', max_words=200, colormap='viridis'.genrate_from_frequencies(word_counts))
    # save wordcloud as png file

    wordcloud.to_file(word_chart_path)    

    # convert the word ing to bassed
    word_cloud_b64 = encode_image_to_base64(word_chart_path)
    return bar_ing_64, word_cloud_b64

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        img_64 = base64.b64decode(img_file.read()).decode('utf-8')
    return img_64  
    