from flask import Flask, render_template, request
from flask_cors import CORS
import requests
URL = "http://127.0.0.1:5000/get-result/"
app = Flask(__name__)
CORS(app)


@app.route('/algorithm-description/<algorithm>', methods=["GET"])
def algo_desc(algorithm):
    case_sensitive_name = algorithm
    if algorithm == "dijkstra":
        case_sensitive_name = "Dijkstras"
    else:
        case_sensitive_name.replace("-", " ")
        case_sensitive_name = case_sensitive_name.title()
        algorithm = algorithm.split("-")[0]
    return render_template('algorithm-description.html', algorithm=algorithm, name=case_sensitive_name)

@app.route('/home', methods=["GET"])
def home():
    return render_template('home.html')

@app.route('/publish', methods=["GET"])
def publish():
    return render_template('publish.html')


@app.route('/dijkstra', methods=["POST"])
def dijkstra():
    inp = request.form.get("input")

    dij_response = requests.get(
        url="{}dijkstra".format(URL), json={"input": inp})
    result = dij_response.json()["result"]
    input_graph = result[-1]
    result = result[:-1]
    return render_template('dijkstra.html', result=result, input_graph=input_graph)


if __name__ == "__main__":
    app.run("127.0.0.1", "4200", debug=True)
