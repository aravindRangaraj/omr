import flask
from flask import request, jsonify, render_template, make_response, Response
from flask_cors import CORS, cross_origin
import omr
import os

app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def index():
    return render_template("UI.html")

@app.route("/omrvalidate/", methods=["GET", "POST"])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def omrvalidate():
    print("hiii")
    isthisFile=request.files['x1']
    file2 = request.files['x2']
    # print(file2.filename)
    # print(isthisFile.filename)
    isthisFile.save("./key/"+isthisFile.filename)
    answers=omr.omr('./key/'+isthisFile.filename,0,0)
    # return render_template("UI.html",msg="upload successful");
    score={}
    for f in request.files.getlist('x2'):
        f.save("./ans/"+f.filename)
        score[f.filename]=omr.omr('./ans/'+f.filename,1,answers)
    # print("onstep close")
    

    
    print(score,"heyyyy")
    dir = './key/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    dir ="./ans/"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    # oput ='['
    # for s in score:
    #     oput += '{"reg":"'+s+'","score":"'+ score[s]+'"},'
    # oput = oput[:-1]
    # oput +=']'
    # print(oput)
    # return send_csv(oput,"score.csv", ["reg", "score"])
    oput ='reg,score\n'
    for s in score:
        oput += s+','+ score[s]+'\n'
    
    return Response(
        oput,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})
    # return output

    

# Driver code
if __name__ == "__main__":
    app.run(host='127.0.0.1', port = 5000)