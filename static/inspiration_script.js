function search_popular() {

    var xhttp = new XMLHttpRequest();

    xhttp.open("GET", "/search", false);
    xhttp.send(JSON.stringify({"login": "true"}));

    var returned_data = JSON.parse(xhttp.response);

    document.getElementById("popular").innerHTML = returned_data['items'][0] + ", by " + returned_data['items'][1];

    document.getElementById("artist_img").src = returned_data['items'][2];

    document.getElementById("add_button").innerHTML = "<button onclick=add_popular() class=btn-success>Add this to my playlist</button>"

    var song_name =  returned_data['items'][0]

}

function add_popular() {

    song_name = document.getElementById("popular");

    var xhttp = new XMLHttpRequest();

    xhttp.open("GET", "/addpopsong", false);
    xhttp.send(JSON.stringify({"song_to_add": song_name}));

}