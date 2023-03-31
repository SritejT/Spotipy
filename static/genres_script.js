function get_artists_by_genre() {

    var xhttp = new XMLHttpRequest;

    var genre = document.getElementById("artist_by_genre").value;

    var data_to_send = {"genre": genre};

    xhttp.open("POST", "/genre", false);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.send(JSON.stringify(data_to_send));

    var genre_artists_dict = JSON.parse(xhttp.response);

    var x = "<ul class=list-group>";

        for (i in genre_artists_dict.content) {

            x += "<li class=list-group-item>" + genre_artists_dict.content[i][0] + "<br><br><img class=img-thumbnail src=" + genre_artists_dict.content[i][1] + ">" + "</li>";

        }

    x += "</ul>";

    document.getElementById("genre_artists").innerHTML = x;

    var all_genre_artists = document.getElementsByClassName('img-thumbnail');

        for (var i = 0; i < all_genre_artists.length; i++) {

            all_genre_artists[i].width = '100';
            all_genre_artists[i].height = '100';

        }

}
