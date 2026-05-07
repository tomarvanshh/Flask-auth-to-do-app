from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()  # Create tables based on the models defined in app/models.py and app/task.py

if __name__ == '__main__':
    app.run(debug=True)