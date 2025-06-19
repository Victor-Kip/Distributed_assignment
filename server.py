from flask import Flask,jsonify
import os
# server
app = Flask(__name__)
server_id = os.getenv("SERVER_ID","unknown")

@app.route('/home',methods = ["GET"])
def home():
    return jsonify({
        "message":f"hello from server {server_id}",
        "status":"successful"

    }),200
#heartbeat
@app.route("/heartbeat",methods = ["GET"])
def heartbeat():
    return "",200

if __name__ == "__main__":
    app.run(host = "0.0.0.0",port= 5000)