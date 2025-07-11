import os
from dotenv import load_dotenv
from app import create_app, db

load_dotenv()
app = create_app()
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7070))
    app.run(host = '0.0.0.0', port=port, debug=True)