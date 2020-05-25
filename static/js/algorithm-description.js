function getXML() {
    var contentXhr = new XMLHttpRequest();
    contentXhr.open("GET", "http://127.0.0.1:5000/get-decription/" + algorithm, true);
    contentXhr.onreadystatechange = addContent;
    contentXhr.send();

    var algoXhr = new XMLHttpRequest();
    algoXhr.open("GET", "http://127.0.0.1:5000/get-algorithm/" + algorithm, true);
    algoXhr.onreadystatechange = addAlgo;
    algoXhr.send();
}

function addContent() {
    if (this.readyState == 4 && this.status == 200) {
        root = this.responseXML.documentElement;
        console.log(root);

        var description = document.getElementById("description");
        description.innerHTML = root.getElementsByTagName("description")[0].innerHTML;

        var algoDescriptionPre = document.getElementById("algo-description-pre");
        algoDescriptionPre.innerHTML = root.getElementsByTagName("algo-description-pre")[0].innerHTML;

        var application = document.getElementById("application");
        var list = document.createElement("ol");
        var applis = root.getElementsByTagName("application")[0].children;
        for (var i = 0; i < applis.length; i += 1) {
            var appli = document.createElement("li");
            appli.innerText = applis[i].innerHTML;
            list.appendChild(appli);
        }
        application.appendChild(list);

        var author = document.getElementById("author");
        author.href = root.getElementsByTagName("author-link")[0].innerHTML;
        author.innerHTML = root.getElementsByTagName("author")[0].innerHTML;

        var ytXhr = new XMLHttpRequest();
        ytXhr.open("GET", "http://127.0.0.1:5000/get-recommendations/" + name.replace(" ", "-"), true);
        ytXhr.onreadystatechange = addYoutube;
        ytXhr.send()
        }
        if (root.getElementsByTagName("input")[0].innerHTML) {
            var inpXhr = new XMLHttpRequest();
            inpXhr.open("GET", "http://127.0.0.1:5000/get-format/" + algorithm, true);
            inpXhr.onreadystatechange = addFormat;
            inpXhr.send();
        }

}   

function addAlgo() {
    if (this.readyState == 4 && this.status == 200) {
        var algorithm = document.getElementById("algorithm");
        algorithm.innerHTML = this.responseText;
        algorithm.className += "prettyprint language-python linenums"
        PR.prettyPrint()
    }
}

function addYoutube() {
    if (this.readyState == 4 && this.status == 200) {
        var jsonResponse = JSON.parse(this.responseText)["result"];
        if(jsonResponse.length)
        {
            var recc = document.getElementById("youtube");
                 br = document.createElement("br");
                recc.appendChild(br);
            var heading = document.createElement("h2");
            heading.innerText = "Recommended Videos";
            recc.appendChild(heading)
            br = document.createElement("br");
            recc.appendChild(br);
            var i;
            for (i = 0; i < jsonResponse.length; i++) {
                var heading = document.createElement("h6");
                heading.innerHTML = jsonResponse[i][1];
                recc.appendChild(heading)

                var iframe = document.createElement("iframe");
                iframe.width = "100%";
                iframe.height = "500";
                iframe.src = jsonResponse[i][0];
                recc.appendChild(iframe);

                br = document.createElement("br");
                recc.appendChild(br);   
                 br = document.createElement("br");
                recc.appendChild(br);
                
            }

        }
    }
}
function addFormat() {
    if (this.readyState == 4 && this.status == 200) {
        var example = document.getElementById("example");
        // example.className = "col-lg-8 col-md-10 mx-auto";


        var heading = document.createElement("h2");
        heading.innerText = "Example Demonstration";
        example.appendChild(heading)

        var filler = document.createElement("p");
        filler.innerHTML = "For a step by step demonstration of " + name  + " algorithm, enter an input in accordance to the format specified below and click submit.";
        example.appendChild(filler)

        var inputHead = document.createElement("h6");
        inputHead.innerText = "Input Format";
        example.appendChild(inputHead)

        var inputCode = document.createElement("pre");
        inputCode.id = "input-code";
        example.appendChild(inputCode);
        inputCode.innerHTML = this.responseText;

        var form = document.createElement("div");
        form.innerHTML = "<form action= 'http://127.0.0.1:4200/" + algorithm +  "' method = 'POST'><textarea type = 'text' name='input'>Enter input here.</textarea><br><br><input class='btn' type='submit'></form>";
        example.appendChild(form);

        PR.prettyPrint()

    }

}