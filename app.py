from flask import Flask
from flask_restful import Resource, Api, reqparse, abort,fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)

class employeeModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    firstName = db.Column(db.String(200))
    lastName = db.Column(db.String(200))
    mobileNumber = db.Column(db.Integer)

#UNCOMMENT BELOW LINES IF YOU'RE RUNNING THIS FILE FOR THE 1ST TIME

#db.create_all()

# employees = {
#     1: {'firstName':'Chandramohan Reddy','lastName':'Poreddy','mobileNumber':'0928316907'},
#         2: {'firstName':'BalKrishna','lastName':'Vodiboina','mobileNumber':'8862213283'},
#         3: {'firstName':'Arjun Singh','lastName':'Gogineni','mobileNumber':'7867879898'}
# }

insert_employee_details = reqparse.RequestParser()

insert_employee_details.add_argument("firstName", type=str, help="First Name is required", required = True)
insert_employee_details.add_argument("lastName", type=str, help="Last Name is required", required = True)
insert_employee_details.add_argument("mobileNumber", type=int, help="Mobile Number is required", required = True)

update_employee_details = reqparse.RequestParser()

update_employee_details.add_argument("firstName", type=str)
update_employee_details.add_argument("lastName", type=str)
update_employee_details.add_argument("mobileNumber", type=int)

resource_fields = {
    'id' : fields.Integer,
    'firstName' : fields.String,
    'lastName' : fields.String,
    'mobileNumber' : fields.Integer
}

class employee(Resource):

    #RETRIEVING DATA FROM DATABASE
    @marshal_with(resource_fields)
    def get(self,id):
        employee = employeeModel.query.filter_by(id=id).first()
        if not employee:
            abort(409, message="Employee not found with ID")

        return employee

    #INSERTING DATA INTO DATABASE
    @marshal_with(resource_fields)
    def post(self,id):
        employee_details = insert_employee_details.parse_args()
        employee = employeeModel.query.filter_by(id=id).first()
        if employee:
            abort(409,"Employee ID already taken, Please change the ID")
        employee = employeeModel(id=id,firstName=employee_details['firstName'],lastName=employee_details['lastName'],mobileNumber=employee_details['mobileNumber'])
        db.session.add(employee)
        db.session.commit()
        return employee, 201


        # if id in employees:
        #     abort(409,"Employee ID already taken, Please change the ID")
        # employees[id] = {"firstName":employee_details["firstName"],"lastName":employee_details["lastName"],"mobileNumber":employee_details["mobileNumber"]}
        # return employees[id]


    #UPDATING DATA IN THE DATABASE
    @marshal_with(resource_fields)
    def put(self,id):
        employee_details = update_employee_details.parse_args()
        employee = employeeModel.query.filter_by(id=id).first()
        if not employee:
            abort(404, message="Employee doesn't exist, Cannot update")
        if employee_details['firstName']:
            employee.firstName = employee_details['firstName']
        if employee_details['lastName']:
            employee.lastName = employee_details['lastName']
        if employee_details['mobileNumber']:
            employee.mobileNumber = employee_details['mobileNumber']
        db.session.commit()
        return employee
            

            

    #DELETING DATA FROM DATABASE
    def delete(self,id):
        employee = employeeModel.query.filter_by(id=id).first()
        db.session.delete(employee)
        db.session.commit()
        return 'Employee Deleted', 204



class employeeList(Resource):
    def get(self):
        employees = employeeModel.query.all()
        employeees = {}
        for employee in employees:
            employeees[employee.id] = {"firstName": employee.firstName, "lastName": employee.lastName, "mobileNumber": employee.mobileNumber}
        return employeees



api.add_resource(employee,'/employees/<int:id>')
api.add_resource(employeeList,'/employees')

if __name__ == '__main__':
    app.run(debug=True)