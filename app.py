from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from os import environ
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import json
import sys

# Init servver

app = Flask(__name__)
cors = CORS(app)


# set an environment varible 
app.config['NAME'] = environ.get('USERNAME')
app.config['KEY'] = environ.get('PASSWORD')


# Configure MongoDB
mongo = PyMongo(app, uri='mongodb+srv://'+app.config['NAME']+':'+app.config['KEY']+'@rscluster-6us0v.mongodb.net/FlaskEmployeeApi?retryWrites=true')

# Setting JSOnEncoder to decode and encode JSON for BSONobjectID
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)




# Api Request of All  Employees
@app.route('/api/employees', methods=['GET'])
def get_employees():
    employees=[]
    # Collect data  from database
    employeesResult = mongo.db.Employees.find()
    # put data in a python dictionary 
    for employee in employeesResult:
        employees.append(employee)
        # print(employee, file=sys.stderr)  
    return  JSONEncoder().encode(employees)


# MAKE A POST TO THE API
@app.route('/api/add', methods=['POST'])
def add_employee():
    # Get  new employee details
    firstname= request.json['firstname']
    lastname=request.json['lastname']
    role=request.json['role']
    department=request.json['department']

    # Perform an insert into the database
    new_employee = mongo.db.Employees.insert({'firstname':firstname, 'lastname':lastname, 'role':role, 'department': department})

    return  JSONEncoder().encode(new_employee)


# GET SINGLE EMPLOYEE ROUTE
@app.route('/api/get/<string:id>', methods=['GET'])
def get_employee(id):
    
    employee= mongo.db.Employees.find_one({'_id':ObjectId(id)})
    return  JSONEncoder().encode(employee)
   

# DELETE SINGLE EMPLOYEE ROUTE
@app.route('/api/delete/<string:id>', methods=['DELETE'])
def delete_employee(id):    
    employee= mongo.db.Employees.delete_one({'_id':ObjectId(id)})
    # Get all employees and retrun 
    employees=[]
    # Collect data  from database
    employeesResult = mongo.db.Employees.find()
    # put data in a python dictionary 
    for employee in employeesResult:
        employees.append(employee)
    return  JSONEncoder().encode( employees)






# Run server
if __name__ == '__main__':
    app.run(debug=True)