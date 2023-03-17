from website import create_app, socketio

app = create_app()

if __name__ == "__main__":
    socketio.run(app, use_reloader=True, debug=True, host='0.0.0.0')
