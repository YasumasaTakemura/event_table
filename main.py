from flask import Flask
from app import users
app = Flask(__name__)
app.register_blueprint(users.app)



# if __name__ == '__main__':
#     app.run(debug=True)