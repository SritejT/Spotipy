function get_rising_artists() {

    var xhttp = new XMLHttpRequest();

    var famous_artist = document.getElementById("famous_artist").value;

    xhttp.open("POST", "/risingartists", false);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.send(JSON.stringify({"data": {"famous_artist": famous_artist}}));

    var rising_artists_dict = JSON.parse(xhttp.response);

    var x = "<ul class=list-group>";

        for (i in rising_artists_dict.content) {

            x += "<li class=list-group-item>" + rising_artists_dict.content[i][0] + "<br><br><img class=artists_img src=" + rising_artists_dict.content[i][1] + ">" + "</li>";

        }

    x += "</ul>";

    document.getElementById("user_analysis").innerHTML = x;

    var all = document.getElementsByClassName('artists_img');

        for (var i = 0; i < all.length; i++) {

            all[i].width = '100';
            all[i].height = '100';

        }

}