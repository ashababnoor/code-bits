// console.log("Inside Data Ingestor!");

/*
TO-DO:
- Populate score table with fake data and check design
- Decide on data storing structure on text file
- Create generator and parser for text file 
- Decide how to give points 
- Add point calculation to game.js
*/

window.load = loadData();

function loadData() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("data-div").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", "data.txt", true);
    xhttp.send();
}