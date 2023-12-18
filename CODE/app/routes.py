# app/routes.py
from flask import Blueprint
from .wordcloud_generator import generate_wordcloud, generate_polarity_wordcloud

wordcloud_bp = Blueprint('wordcloud', __name__)

@wordcloud_bp.route('/wordcloud/<state>/<business_id>', methods=['GET'])
def wordcloud_route(state, business_id):
    return generate_wordcloud(state, business_id)

@wordcloud_bp.route('/polarity_wordcloud/<state>/<business_id>', methods=['GET'])
def polarity_wordcloud_route(state, business_id):
    return generate_polarity_wordcloud(state, business_id)
