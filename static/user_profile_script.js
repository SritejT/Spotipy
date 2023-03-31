function prompt_user() {

    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "/promptuser", false);
    xhttp.send(JSON.stringify({"login" : "true"}));

    var user_recents = JSON.parse(xhttp.response);

    var x = "<ul class=list-group>";

        for (i in user_recents.user_recents) {

            x += "<li class=list-group-item>" + user_recents.user_recents[i][0] + ", by " + user_recents.user_recents[i][1]
                  + "<br><br><img class=recommended_artists src=" + user_recents.user_recents[i][2] + "></li>";

        }

    x += "</ul>";

    document.getElementById("user_details").innerHTML = "<p>Your recommended tracks are:</p><br>" + x;

    var all_recommended_artists = document.getElementsByClassName("recommended_artists");

    for (var i = 0; i < all_recommended_artists.length; i++) {

            all_recommended_artists[i].width = '100';
            all_recommended_artists[i].height = '100';

        }

}

function get_trending() {

    var xhttp = new XMLHttpRequest;

    xhttp.open("POST", "/trending", false);
    xhttp.send(JSON.stringify(""));

    var trending_tracks = xhttp.response;

    document.getElementById("trending_tracks").innerHTML = trending_tracks;

}

