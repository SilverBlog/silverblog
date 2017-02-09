from flask import Flask, request
import newpost
app = Flask(__name__)

@app.route('/newpost', methods=['POST'])
def newpost():
    newpost.new_post("",request.json["title"],"",request.json["content"])
    print(request.json["encode"])
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
