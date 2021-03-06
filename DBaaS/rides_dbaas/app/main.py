from flask import Flask, render_template,\
jsonify,request,abort,redirect
import requests
import json
from datetime import datetime
from flask_mysqldb import MySQL

def is_sha1(maybe_sha):
    if len(maybe_sha) != 40:
        return False
    try:
        sha_int = int(maybe_sha, 16)
    except ValueError:
        return False
    return True

app= Flask(__name__)

app.config['MYSQL_HOST']	 = 'db_rides' 
app.config['MYSQL_USER']	 = 'user'
app.config['MYSQL_PASSWORD']     = '123'
app.config['MYSQL_DB'] 		 = 'rides'
app.config['MYSQL_PORT']=3306;

mysql=MySQL(app)

#Users={}
Rides={}
rideId=0
avail=[]
@app.route("/api/v1/rides/count", methods=["GET"])
def countrides():
                dic={'type':6}
                res=requests.post('http://52.4.146.61:80/api/v1/db/read',json=dic)
                re=res.json()
                cur=mysql.connection.cursor()
                cur.execute("UPDATE counter SET count = count + 1")
                mysql.connection.commit()
                cur.close()
                return jsonify(list(re["val"])),200

@app.route("/api/v1/rides/count", methods=["POST","DELETE","PUT"])
def countrides1():
	cur=mysql.connection.cursor()
	cur.execute("UPDATE counter SET count = count + 1")
	mysql.connection.commit()
	cur.close()
	return jsonify(),405


@app.route("/api/v1/_count")
def count():
		cur=mysql.connection.cursor()
		cur.execute("SELECT count FROM counter")
		l = cur.fetchall()
		print(l)
		mysql.connection.commit()
		cur.close()
		return jsonify(l[0]),200

@app.route("/api/v1/_count",methods=["DELETE"])
def reset():
		cur=mysql.connection.cursor()
		cur.execute("UPDATE counter SET count = 0")
		mysql.connection.commit()
		cur.close()
		return jsonify(),200



@app.route("/api/v1/rides",methods=["POST"])
def create_ride():
	if(request.method == 'POST'):
		global rideId
		user=request.get_json()["created_by"]
		check={"type":1,"user":user}
		timest=request.get_json()["timestamp"]
		source=request.get_json()["source"]
		destination=request.get_json()["destination"]
		dic={}
		dic["type"]=3
		dic["ride"]=[user,timest,source,destination]
		send=requests.get('http://load-balancer-1955007695.us-east-1.elb.amazonaws.com/api/v1/users',json=check)
		res=send.json()
		print(res)
		if (int(source)>190 or int(destination)>190 or int(source)<0 or int(destination)<0):
			print("qwe")
			cur=mysql.connection.cursor()
			cur.execute("UPDATE counter SET count = count + 1")
			mysql.connection.commit()
			cur.close()
			return jsonify(),400
		if(len(str(res))== 0):
			cur=mysql.connection.cursor()
			cur.execute("UPDATE counter SET count = count + 1")
			mysql.connection.commit()
			cur.close()
			print("asd")
			return jsonify(),400
		else:
			cur=mysql.connection.cursor()
			cur.execute("UPDATE counter SET count = count + 1")
			mysql.connection.commit()
			cur.close()
			r=requests.post('http://52.4.146.61:80/api/v1/db/write',json=dic)
			
			if(r.status_code== 400):
				print("zxcv")
				return jsonify(),400	
			rideId+=1
			return jsonify(),201
	else:
		cur=mysql.connection.cursor()
		cur.execute("UPDATE counter SET count = count + 1")
		mysql.connection.commit()
		cur.close()
		return jsonify(),405

@app.route("/api/v1/rides",methods=['PUT'])
def get_rides1():
	cur=mysql.connection.cursor()
	cur.execute("UPDATE counter SET count = count + 1")
	mysql.connection.commit()
	cur.close()
	return jsonify(),405

@app.route("/api/v1/rides",methods=["GET"])
def get_rides():
	if(1==1):
		source=request.args.get('source')
		destination=request.args.get('destination')
		dic={}
		dic["type"]=2
		dic["ride"]=[source,destination]
		send=requests.post('http://52.4.146.61:80/api/v1/db/read',json=dic)
		res=send.json()
		curr_time=datetime.now()
		cur_time=curr_time.strftime("%Y-%m-%d:%H-%M-%S")
		ans=[]
		cur=mysql.connection.cursor()
		cur.execute("UPDATE counter SET count = count + 1")
		mysql.connection.commit()
		cur.close()		
		if(len(res['val'])==0):
			return jsonify(),204
		else:
			for i in res['val']:
				r=datetime.strptime(i[2],"%d-%m-%Y:%S-%M-%H")
				time=datetime.strftime(r,"%Y-%m-%d:%H-%M-%S")
				if(not(cur_time>time)):
					ans.append({"rideId":i[0],"username":i[1],"timestamp":i[2]})
		return jsonify(ans),200
	else:
		cur=mysql.connection.cursor()
		cur.execute("UPDATE counter SET count = count + 1")
		mysql.connection.commit()
		cur.close()
		return jsonify(),405

@app.route("/api/v1/rides/<rideId>",methods=["GET"])
def ride_details(rideId):
	if(request.method == 'GET'):
		temp = {'type':4, 'ride':int(rideId)}
		res = requests.post('http://52.4.146.61:80/api/v1/db/read', json = temp)
		r = res.json()['val']
		cur=mysql.connection.cursor()
		cur.execute("UPDATE counter SET count = count + 1")
		mysql.connection.commit()
		cur.close()
		if(len(r)==0):
			return jsonify(),204
		else:
			return jsonify(r),200
	else:
		cur=mysql.connection.cursor()
		cur.execute("UPDATE counter SET count = count + 1")
		mysql.connection.commit()
		cur.close()
		return jsonify(),405

@app.route("/api/v1/rides/<rideId>",methods=['PUT'])
def join_ride1(rideId):
	cur=mysql.connection.cursor()
	cur.execute("UPDATE counter SET count = count + 1")
	mysql.connection.commit()
	cur.close()
	return jsonify(),405

@app.route("/api/v1/rides/<rideId>",methods=["POST"])
def join_ride(rideId):
	if(request.method == 'POST'):
		dic = request.get_json()
		username = dic["username"]
		temp = {'type':3, 'ride':int(rideId)}
		users = requests.post('http://52.4.146.61:80/api/v1/db/read', json = temp)
		val = users.json()
		if(len(val['val']) == 0):
			cur=mysql.connection.cursor()
			cur.execute("UPDATE counter SET count = count + 1")
			mysql.connection.commit()
			cur.close()	
			return jsonify(),204
		temp = {'type':1, 'user':username}
		user_list = requests.post('http://52.4.146.61:80/api/v1/db/read', json = temp)
		val = user_list.json()
		if(len(val['val']) == 0):
			cur=mysql.connection.cursor()
			cur.execute("UPDATE counter SET count = count + 1")
			mysql.connection.commit()
			cur.close()			
			return jsonify(),204
		cur=mysql.connection.cursor()
		cur.execute("UPDATE counter SET count = count + 1")
		mysql.connection.commit()
		cur.close()		
		t1 = (username,rideId)
		temp = {'type':4, 'ride':t1}
		resp = requests.post('http://52.4.146.61:80/api/v1/db/write', json = temp)
		val = user_list.json()['val']
		return jsonify(),200
	else:
		cur=mysql.connection.cursor()
		cur.execute("UPDATE counter SET count = count + 1")
		mysql.connection.commit()
		cur.close()
		return jsonify(),405



@app.route("/api/v1/rides/<rideId>",methods=["DELETE"])
def delete_ride(rideId):
	if(request.method=="DELETE"):
		cur=mysql.connection.cursor()
		cur.execute("UPDATE counter SET count = count + 1")
		mysql.connection.commit()
		cur.close()
		temp={'type':3,'ride':int(rideId)}
		res=requests.post('http://52.4.146.61:80/api/v1/db/read',json=temp)
		r=res.json()
		if(len(r['val'])==0):
			return jsonify(),400
		temp={"type":5,'ride':[rideId]}
		resp=requests.post('http://52.4.146.61:80/api/v1/db/write',json=temp)
		d=resp.json()
		if(resp.status_code== 400):
			return jsonify(),400
		else:
			return jsonify(),200
	else:
		cur=mysql.connection.cursor()
		cur.execute("UPDATE counter SET count = count + 1")
		mysql.connection.commit()
		cur.close()
		return jsonify(),400

if __name__ =="__main__":
	app.run(host='0.0.0.0',debug=True,port=80)
