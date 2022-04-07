from website import createApp
import uuid

app = createApp()

if __name__ == "__main__":
    print(uuid.uuid4)
    app.run(debug=True)

