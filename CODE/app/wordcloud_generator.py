# app/wordcloud_generator.py
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import send_file
from wordcloud import WordCloud
from .data_loader import load_csv_data
from .constants import state_abbreviations
from collections import defaultdict
import ast

# created_image path
image_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'created_images')


def generate_wordcloud(state, business_id):
    state = state_abbreviations[state]   

    df = load_csv_data(state)
    # use index instead of filter for speed
    df = df.loc[business_id]
    business_name = df['business_name'].iloc[0]
    combined_reviews = "".join(df["review"])

    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(combined_reviews)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title(f"Document Level Word Count scaled by Frequency: {business_name}")
    plt.axis("off")

    image_filename =  os.path.join(image_folder, f"wordcloud_{business_name}_{business_id}.png")
    fig = plt.gcf()  # Get the current figure
    fig.savefig(image_filename)
    plt.close(fig)  # Explicitly close the figure

    return send_file(image_filename, mimetype='image/png')

def generate_polarity_wordcloud(state, business_id):
    state = state_abbreviations[state]

    df = load_csv_data(state)
        # use index instead of filter for speed
    df = df.loc[business_id]
    business_name = df['business_name'].iloc[0]
    # Initialize dictionaries to store keyword frequency and score for each category
    people_dict = defaultdict(list)
    product_dict = defaultdict(list)
    org_dict = defaultdict(list)

    def process_row(row):
        aspect_sentiments_str = row['aspect_sentiments']
        aspect_sentiments = ast.literal_eval(aspect_sentiments_str) if isinstance(aspect_sentiments_str, str) else aspect_sentiments_str
        for aspect, sentiment_info in aspect_sentiments.items():
            for keyword, score in sentiment_info.items():
                if aspect == 'PERSON':
                    people_dict[keyword].append(score)
                elif aspect == 'PRODUCT':
                    product_dict[keyword].append(score)
                elif aspect == 'ORG':
                    org_dict[keyword].append(score)

    # Apply the function to each row of the DataFrame, which save to dict
    df.apply(process_row, axis=1)
    
    def generate_wordcloud(data_dict, title, ax):
        avg_score = {keyword: sum(scores) / len(scores) for keyword, scores in data_dict.items()}
        positive_words = {k: v for k, v in avg_score.items() if v > 0}
        negative_words = {k: -v for k, v in avg_score.items() if v < 0}

        # Check if there are words for positive word cloud
        if positive_words:
            # Plot the positive word cloud
            wordcloud_pos = WordCloud(width=400, height=200, background_color='white').generate_from_frequencies(positive_words)
            
            ax[0].imshow(wordcloud_pos, interpolation='bilinear')
            ax[0].set_title(f'{title} (Positive)')
            ax[0].axis('off')
        else:
            ax[0].axis('off')
            ax[0].set_title(f'{title} (Positive) - No words to display')

        # Check if there are words for negative word cloud
        if negative_words:
            # Plot the positive word clouds
            wordcloud_neg = WordCloud(width=400, height=200, background_color='white', colormap='Reds').generate_from_frequencies(negative_words)
            
            ax[1].imshow(wordcloud_neg, interpolation='bilinear')
            ax[1].set_title(f'{title} (Negative)')
            ax[1].axis('off')
        else:
            ax[1].axis('off')
            ax[1].set_title(f'{title} (Negative) - No words to display')

    # Create a subplot with three rows and two columns
    fig, axs = plt.subplots(3, 2, figsize=(15, 13))
    fig.subplots_adjust(hspace=0.3)

    # Generate word clouds for each category
    generate_wordcloud(people_dict, 'People', axs[0, :])
    generate_wordcloud(product_dict, 'Product', axs[1, :])
    generate_wordcloud(org_dict, 'Organization', axs[2, :])

    fig.suptitle(f'Polarity Wordcloud Scaled by Aspect Score and Frequency: {business_name}', fontsize=20)

    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
    image_filename = os.path.join(image_folder, f"polarity_wordcloud_{business_name}_{business_id}.png")
    fig = plt.gcf()  # Get the current figure
    fig.savefig(image_filename)
    plt.close(fig)  # Explicitly close the figure
    
    return send_file(image_filename, mimetype='image/png')