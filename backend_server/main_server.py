from flask import Flask, make_response, render_template, request, Response
from flask_cors import CORS
from dijkstra import dijkstra_helper
import json
import requests 

app = Flask(__name__)
CORS(app,  allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True)

@app.route('/get-recommendations/<query>', methods=["GET", "POST"])
def get_recommendations(query):
    query.replace("-", " ")
    PARAMS = {
    'part':'snippet',
    'maxResults' : 3,
    'q' : query,
    'key' : ""
    } 
    
    req = requests.get(url = "https://www.googleapis.com/youtube/v3/search", params = PARAMS) 
    data = req.json()
    itemlist = []
    for item in data["items"]:

        itemlist.append(["https://www.youtube.com/embed/" +  item["id"]["videoId"], item["snippet"]["title"]])

    return Response(json.dumps({"result" : itemlist}), status = 200, mimetype = 'application/json')


@app.route('/get-decription/<algorithm>', methods=["GET"])
def description(algorithm):
    desc_handler = open("res/desc/{}.xml".format(algorithm), 'r')
    response = make_response(desc_handler.read())
    response.headers.set('Content-Type', 'application/xml')
    desc_handler.close()
    return response


@app.route('/get-algorithm/<algorithm>', methods=["GET"])
def algorithm(algorithm):
    file_handler = open("res/algo/{}.txt".format(algorithm), 'r')
    contents = file_handler.read()
    file_handler.close()
    return make_response(contents)

@app.route('/get-format/<algorithm>', methods=["GET"])
def inp_format(algorithm):
    file_handler = open("res/inp_format/{}.txt".format(algorithm), 'r')
    contents = file_handler.read()
    file_handler.close()
    return make_response(contents)

@app.route('/get-result/<algorithm>', methods=["GET"])
def result(algorithm):
    print("\n\n\n\n", request.get_json())
    return Response(json.dumps({"result" : dijkstra_helper(request.get_json()["input"])}), status = 200, mimetype = 'application/json')

@app.route('/get-intro', methods=["GET"])
def intro():
    file_handler = open("res/home/intro.json", 'r')
    contents = file_handler.read()
    file_handler.close()
    return Response(contents, status = 200, mimetype = 'application/json')

@app.route('/rssfeed', methods=["GET"])
def feed():
    desc_handler = open("res/home/bloglist-rss.xml", 'r')
    response = make_response(desc_handler.read())
    response.headers.set('Content-Type', 'text/xml')
    return response

@app.route('/publish', methods=["POST"])
def publish():
        title = request.form.get("title")
        if title != "":
            description = request.form.get("description")
            algo_description = request.form.get("algo-description-pre")
            applications = request.form.get("applications").split("\n")
            author_name = request.form.get("author-name")
            author_link = request.form.get("author-link")
            apps = ""
            for appli in applications:
                apps += '\t\t\t<app>{}</app>'.format(appli.replace("\n", ""))

            desc = '<?xml version="1.0" encoding="UTF-8"?>\n\t<article> \n\t' + \
            '<title>{}</title>\n\t'.format(title) + \
            '<description>{}</description>\n\t'.format(description) + \
            '<algo-description-pre>{}</algo-description-pre>\n\t'.format(algo_description) + \
            '<application>{}</application>\n\t'.format(apps) + \
            '<author>{}</author>\n\t'.format(author_name) + \
            '<author-link>{}</author-link>\n\t'.format(author_link) + \
            '\n</article>'

            desc_handler = open("res/desc/{}.xml".format(title.split()[0]).lower(), 'w')
            desc_handler.write(desc)
            desc_handler.close()

            algo_handler = open("res/algo/{}.txt".format(title.split()[0]).lower(), 'w')
            algo_handler.write(request.form.get("algo"))
            algo_handler.close()

            rss_handler = open("res/home/bloglist-rss.xml", 'r')
            rss = ""
            for line in rss_handler.readlines():
                if "</channel>" in line:
                    break
                else:
                    rss += line 
            
            rss += "\t\t<item>\n"
            rss += "\t\t\t<title>{}</title>\n".format(title)
            rss += "\t\t\t<link>http://127.0.0.1:4200/algorithm-description/{}</link>\n".format(title.lower().replace(" ","-"))
            rss += "\t\t\t<description>{}</description>\n".format(description)            
            rss += "\t\t\t<creator>{}</creator>\n".format(author_name)            
            rss = rss + "\t\t</item>\t\n</channel>\n</rss>"
            rss_handler.close();

            rss_handler = open("res/home/bloglist-rss.xml", 'w')
            rss_handler.write(rss);
            rss_handler.close();
            return "<h6>Submitted!</h6>"
        else:
            return "<h5>Fill Form correctly!</h5>"

@app.route('/test', methods=["GET"])
def test():
    return Response(json.dumps({"title" : "Graph Algorithms"}), status = 200, mimetype = 'application/json')

if __name__ == "__main__":
    app.run("127.0.0.1", "5000", debug=True)
