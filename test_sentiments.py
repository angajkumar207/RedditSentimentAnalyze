from msvcrt import getch
import pytest
from flask import Flask
from unittest.mock import patch
from requests import patch
from app.models import create_app, db
from app.analysis import analyze_sentiment
from app.fetch_reddit_data import fetch_reddit_data
from app.models import SentimentAnalysis

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test_sentiment.db"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_analyze_sentiment():
    posts = [
        {
            "content": "i am looking for subcontracting job in computer programming and data science. i have many.....",
            "title": "looking for subcontracting job in computer programming and data science."

        },
        {
            "title": "[Hirring] [india] - software Engineeri\n",
            "content": "Experince : 1+ years\n skills : Golang, python, Java, NodeJS, Typecripts, REST API\n\n"
        }
    ]
    results = analyze_sentiment(posts)
    assert len(results) == 2
    assert results[0]['sentiment'] == 'POSITIVE'
    assert results[1]['sentiment'] == 'POSITIVE'

def test_analyze_route(client):
    with patch('app. fetch_raddit_data. fetch_raddit_data') as mock_fetch:
        mock_fetch.return_value = [
        {
            "title": " i go to loyola maryland and dont know what to major",
            "content": " i enjoy finace and tech. i was aiming to make the most money out of the collage and was stock...."
        }]
        response =  client.post('/api/sentiment/analyze', data = {'topic': 'science', 'num_records':1})
        assert response.status_code == 200

def test_database_integration(client):
    with client.application.app_context():
        new_record = SentimentAnalysis(
            topic= 'science', sentiment='POSTIVE', score = 0.5994,
            title= " i go loyola maryland and doesn't know what to major",
            content = " i enjoy finance and tech. i was animing............"

        )
        db.session.add(new_record)
        db.session.commit()
        record = SentimentAnalysis.query.filter_by(topic='science').first()
        assert record is not None
        assert record.sentiment == 'POSSTIVE'

def test_invalid_input(client):
    responce = client.post("/api/sentiment/analyze", data = {})
    assert responce.status_code == 400
    assert 'Topic is required ' in responce.data.decode('utf-8')



