from website import create_app, create_db

app = create_app()

if __name__ == "__main__":
    create_db(app)
    app.run(debug=True)
