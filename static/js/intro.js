var app = angular.module('myApp', []);
app.controller('customersCtrl', function ($scope, $http) {
  $http.get("http://127.0.0.1:5000/get-intro").then(function (response) {
    $scope.title = response.data.title;
    $scope.intro = response.data.intro;
  });
});

var ttl = 3000;
var xhr = new XMLHttpRequest();

function getRSS() {
  xhr.open("GET", "http://127.0.0.1:5000/rssfeed", true);
  xhr.onreadystatechange = this.showResults;
  xhr.send();
}

function showResults() {
  if (this.readyState == 4 && this.status == 200) {
    var algoList = document.getElementById("algo-lists");
    algoList.innerHTML = "";
    root = this.responseXML.documentElement;
    // root = root.getElementsByTagName("rss")[0];
    console.log(root);
    main = root.getElementsByTagName("channel");
    ttl = root.getElementsByTagName("ttl")[0].firstChild.nodeValue;

    setInterval(getRSS, ttl);

    title_channel = main[0].getElementsByTagName("title")[0].firstChild.nodeValue;

    itemi = main[0].getElementsByTagName("item");

    for (var i = 0; i < 5; i++) {
      title = itemi[i].getElementsByTagName("title")[0].firstChild.nodeValue;
      link = itemi[i].getElementsByTagName("link")[0].firstChild.nodeValue;
      desc = itemi[i].getElementsByTagName("description")[0].firstChild.nodeValue;
      br = document.createElement("br");
      algoList.appendChild(br);
      
      pre = document.createElement("pre");
      pre.innerHTML = toString(i);

      anchor = document.createElement("a");
      anchor.href = link;
      anchor.innerHTML = (i + 1).toString() + ".  " + title;
      algoList.appendChild(anchor);

      para = document.createElement("div");
      para.innerHTML = desc;
      algoList.appendChild(para);

      para = document.createElement("div");
      para.style = "font-size: smaller !important;    color: rgb(42, 66, 104); "
      para.innerHTML = "Authored by " + itemi[i].getElementsByTagName("creator")[0].firstChild.nodeValue + ".";
      algoList.appendChild(para);

      br = document.createElement("br");
      algoList.appendChild(br);
    }

  }
}

