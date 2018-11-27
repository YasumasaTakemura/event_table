import datetime
from flask import Blueprint,request,jsonify
from infra.users.users import Users
app = Blueprint('users',__name__,url_prefix='/user')
print(__name__)

@app.route('/add/<string:user_name>',methods=['POST','GET'])
def add_user(user_name):
    u = Users({'user_name':user_name})
    result = u.add()
    return jsonify(result)

@app.route('/update',methods=['POST'])
def update_user():
    payload = request.json
    u = Users()
    key = u.update(payload)
    print(key)
    return jsonify({'user_id':key})

@app.route('/delete',methods=['POST'])
def delete_user():

    return ''