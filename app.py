from src.models.database import initialize_db
from web import create_app

app = create_app()

if __name__ == "__main__":
    initialize_db()
    app.run(debug=True)