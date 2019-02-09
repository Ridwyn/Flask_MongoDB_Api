from flask import Flask, request, jsonify
from os import environ
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import json
import sys

# Init servver

app = Flask(__name__)

# set an environment varible 
app.config['NAME'] = environ.get('USERNAME')
app.config['KEY'] = environ.get('PASSWORD')


# Configure MongoDB
mongo = PyMongo(app, uri='mongodb+srv://'+app.config['NAME']+':'+app.config['KEY']+'@rscluster-6us0v.mongodb.net/FlaskEmployeeApi?retryWrites=true')

# Setting JSOnEncoder to decode and encode JSON
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)





# Checking for db
@app.route('/')
def get_employees():
    employees=[]
    employeesResult = mongo.db.Employees.find()
    for employee in employeesResult:
        employees.append(employee)
        # print(employee, file=sys.stderr)

    
    return JSONEncoder().encode(employees)




# Run server
if __name__ == '__main__':
    app.run(debug=True)