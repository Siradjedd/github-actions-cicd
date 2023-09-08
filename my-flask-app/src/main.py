from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy

# Instantiate Flask functionality
app = Flask(__name__)

# Set SQLAlchemy URI in application config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Define the SQLAlchemy db object, but don't create tables yet
db = SQLAlchemy(app)  # Instance of SQLAlchemy

# Define the TodoList model
class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.Text, nullable=False)

    def __str__(self):
        return f"{self.id} {self.todo}"

# Create a function to initialize the database
def initialize_database():
    with app.app_context():
        db.create_all()

# Create the database tables within the Flask app context
initialize_database()

# Define the todo_serializer function to convert TodoList objects to JSON
def todo_serializer(todo):
    return {"id": todo.id, "todo": todo.todo}

@app.route("/", methods=["GET"])
def home():
    # Serialize and return all items in TodoList as JSON
    todo_items = TodoList.query.all()
    serialized_todo_items = [todo_serializer(item) for item in todo_items]
    return jsonify(serialized_todo_items)


@app.route("/todo-create", methods=["POST"])
def todo_create():
    # Add todo to the database
    request_data = json.loads(request.data)
    todo = TodoList(todo=request_data["todo"])

    db.session.add(todo)
    db.session.commit()

    return {"201": "Todo created successfully"}

@app.route("/update/<int:id>", methods=["PUT"])
def update_todo(id):
    # Edit todo item based on ID
    item = TodoList.query.get(id)
    request_data = request.get_json()
    todo = request_data["todo"]
    item.todo = todo
    db.session.commit()

    return {"200": "Updated successfully"}

@app.route("/<int:id>", methods=["DELETE"])
def delete_todo(id):
    # Delete todo item from todo list
    request_data = request.json
    TodoList.query.filter_by(id=request_data["id"]).delete()
    db.session.commit()
    return {"204": "Delete successfully"}
# Define the rest of your routes and functions here

# Rest of your routes and functions...
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
