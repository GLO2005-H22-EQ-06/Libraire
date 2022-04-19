from flask import session
from website import createApp
import bcrypt


app = createApp()


if __name__ == "__main__":
    app.run(debug=True)
    for key in list(session.keys()):
        session.pop(key)
