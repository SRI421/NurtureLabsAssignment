from flask import Flask, request, jsonify,session
import os
import python_jwt as jwt, jwcrypto.jwk as jwk, datetime
from pymongo import MongoClient
import pymongo

client = pymongo.MongoClient("mongodb+srv://srikanth:sri974213@cluster0.5gjaf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mydb=client["nlabs"]
mycol1=mydb["advisor"]
mycol2=mydb["booking"]
mycol3=mydb["user"]

key = jwk.JWK.generate(kty='RSA', size=2048)

app = Flask('app')
uid=None
@app.route('/')
def hello_world():
    return 'Thank you Nurturelabs. I completed this assignment given by you and deployed in heroku and saved repository in github'

@app.route('/admin/advisor/', methods=['POST'])
def admin():
    content=request.json
    
    try:
        if content['advisor_name'] and content['advisor_photo_url']:
            advisorName=content['advisor_name']
            advisorPic=content['advisor_photo_url']

            mydict={"id":advisorName+str(len(advisorName)), "advisorName":advisorName, "advisorPic":advisorPic}
            mycol1.insert_one(mydict)
            return jsonify({"status":"200_OK"})
    except:
        return jsonify({"status":"400_BAD_REQUEST"})    
        

@app.route('/user/register/', methods=['POST'])
def userRegistration():
    content=request.json
    
    try:
        if content['name'] and content['email'] and content['password']:
            name=content['name']
            email=content['email']
            password=content['password']

            payload = { 'email': email, 'password': password  };

            token = jwt.generate_jwt(payload, key, 'PS256', datetime.timedelta(minutes=5))
            userid=name+str(len(email))
            mydict={"id":userid, "name":name, "email":email, "password":password}
            mycol3.insert_one(mydict)

            return jsonify({"status":"200_OK", "body":{"token":token,"userid":userid}})
    except:
        return jsonify({"status":"400_BAD_REQUEST"})

@app.route('/user/login/', methods=['POST'])
def login():
    content=request.json
    
    try:
        if content['email'] and content['password']:
            
            email=content['email']
            password=content['password']

            payload = { 'email': email, 'password': password  };

            token = jwt.generate_jwt(payload, key, 'PS256', datetime.timedelta(minutes=5))
            
            b=mycol3.find()
            rows=[]
            for i in b:
                rows.append(i)

            for i in rows:
                if i['email']==email and i['password']==password:
                    id=i['id']
                    session['id']=email
                    return jsonify({"status":"200_OK", "body":{"token":token,"userid":id}})
            
            return jsonify({"status":"401_AUTHENTICATION_ERROR"})
    except:
        return jsonify({"status":"400_BAD_REQUEST"})

@app.route('/user/<userid>/advisor', methods=['GET'])
def userAdvisor(userid):
    try:
        b=mycol1.find({}, {"_id":0})
        rows=[]
        for i in b:
            rows.append(i)
        print(rows)
        return jsonify({"status":"200_OK","body":rows})
    except:
        return jsonify({"status":"400_BAD_REQUEST"})

@app.route('/user/<userid>/advisor/<advisorid>', methods=['POST'])
def advisorbooking(userid,advisorid):
    content=request.json
    try:
        if content['booking_time']:
            c=mycol1.find_one({"id":advisorid})

            mydict={"userid":userid, "advisorName":c["advisorName"], "advisorProfilePic":c["advisorPic"], "advisorId":advisorid, "bookingTime":content['booking_time'], "bookingId":getbookingid()}
            mycol2.insert_one(mydict)
            return jsonify({"status":"200_OK"})
    except:
        return jsonify({"status":"400_BAD_REQUEST"})

@app.route('/user/<userid>/advisor/booking/', methods=['POST'])
def bookinglist(userid):
    try:
        c=mycol2.find({"userid":userid},{"_id":0,"userid":0})
        rows=[]
        for i in c:
            rows.append(i)
        return jsonify({"status":"200_OK","body":rows})
    except:
        return jsonify({"status":"400_BAD_REQUEST"})


def getbookingid():
    b=mycol2.find()
    count=0
    for i in b:
        if count<int(i["bookingId"]):
            count=int(i["bookingId"])
    return count+1

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
