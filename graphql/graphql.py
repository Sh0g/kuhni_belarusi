from flask import Flask, request
from ariadne import load_schema_from_path, make_executable_schema, graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in production
jwt = JWTManager(app)

engine = create_engine('sqlite:///database.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Define your database models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

Base.metadata.create_all(engine)

# Load the GraphQL schema
type_defs = load_schema_from_path('schema.graphql')

# Define the GraphQL resolvers
@query.field('users')
@jwt_required()
def resolve_users(_, info):
    session = Session()
    users = session.query(User).all()
    session.close()
    return users

# Create the GraphQL schema
schema = make_executable_schema(type_defs, [query, mutation])

# GraphQL endpoint
@app.route('/graphql', methods=['GET'])
def graphql_playgroud():
    return PLAYGROUND_HTML, 200

@app.route('/graphql', methods=['POST'])
@jwt_required()
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value={'session': Session()})
    return result

# Authentication endpoints
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # Authenticate the user and generate the access token
    access_token = create_access_token(identity=username)
    return {'access_token': access_token}

if __name__ == '__main__':
    app.run(debug=True)