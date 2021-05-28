# imports
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

# define the app
app = Flask(__name__)
CORS( app, supports_credential=True )
# database credentials
hostname = "sql5.freesqldatabase.com"
username = "sql5414485"
password = "GR97uFa79x"
database = "sql5414485"

# define the MySQL connection
conn = pymysql.connect(host=hostname, user=username, passwd=password, db=database)
cursor = conn.cursor()

# user routes
@app.route( "/api/register", methods=["POST"] )
def register():
    if request.method == "POST":

        avatar = request.json.get( 'avatar', None )
        first_name = request.json.get( 'first_name', None )
        last_name = request.json.get( 'last_name', None )
        email = request.json.get( 'email', None )
        password = request.json.get( 'password', None )
        confirm_password = request.json.get( 'confirm_password', None )

        if first_name == "" or last_name == "" or email == "" or password == "" or confirm_password == "" or avatar == "" :
            return jsonify( {'response': False, 'message': 'All fields are required'} )
        else:
            # check if the user is already exists
            SQL = "SELECT * FROM bloggers WHERE email = %s"
            insert_tuple = email
            result = cursor.execute( SQL, insert_tuple )

            # check if user id exists
            if result != 0 :
                return jsonify( {'response': False, 'message': 'User already registered'} )
            else:
                # check passwords are matched
                if password == confirm_password:
                    hash_password = generate_password_hash( password )
                    SQL = "INSERT INTO bloggers (first_name, last_name, email, password, avatar) VALUES (%s, %s, %s, %s, %s)"
                    insert_tuple = (
                        str( first_name ), str( last_name ), str( email ), str( hash_password ), str( avatar ))
                    cursor.execute( SQL, insert_tuple )
                    conn.commit()

                    SQL = "SELECT * FROM bloggers WHERE email = %s"
                    insert_tuple = email
                    cursor.execute( SQL, insert_tuple )
                    result = cursor.fetchall()

                    return jsonify( {'response': True, 'message': 'Registration Successful'} )
                else:
                    return jsonify( {'response': False, 'message': 'password mismatch'} )


@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)


@app.route('/post/', methods=['POST'])
def post_something():
    name = request.json.get('name')
    print(name)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if name:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD": "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
