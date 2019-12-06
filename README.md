# Moodset

This repository contains the code for the backend REST API of the Moodset application.




## RESTful API functionalities

The Moodset REST API provides the following functionalities:
- User Registration with token authentication
- User log in
- Search songs
- User create playlist
- User generate playlist


## API Setup

First make sure you have `pipenv` installed and run:

    pipenv install
    pipenv shell

This should install all needed libraries for the project and start the moodset virtual environment. Now setup up the local PostgresQL database and configure `moodset_api/settings.py`. Use [this](https://medium.com/agatha-codes/painless-postgresql-django-d4f03364989) guide. After you have made the migrations, run:

    python manage.py populate_db
    python manage.py runserver

The server is hosted at [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Append the following url paths to access different API endpoints.



### Registration

    POST api/v1/rest-auth/registration/
 Save the token returned from this registration.

### Log in

    POST api/v1/rest-auth/
Returns a token used in subsequent requests.

### Search songs

    GET moodapi/songs/?search=[songname]
While logged in, song names can be searched via the above endpoint.

### Create Playlist

    POST moodapi/playlists/
This should be requested programmatically, as the following headers and body are needed:


#### Headers
| KEY |VALUE  |
|--|--|
| Content-Type | application/json |
| Authorization | Token [token] |

#### Body

    {
    "playlist_name": "Coldplay Playlist",
    "songs": [
        "1mea3bSkSGXuIRvnydlB5b",
        "75JFxkI2RXiU7L9VXzMkle",
        "0BCPKOYdS2jbQ8iyB56Zns",
        "3AJwUDP919kvQ9QcozQPxg",
        "7LVHVU3tWfcxj5aiPFEW4Q",
        "2QhURnm7mQDxBb5jWkbDug",
        "2nvC4i2aMo4CzRjRflysah",
        "0R8P9KfGJCDULmlEoBagcO",
        "7clUVcSOtkNWa58Gw5RfD4",
        "1ZqHjApl3pfzwjweTfMi0g"
    ]
    }

**Note**: other songs can be selected by collecting their Spotify id with the search songs endpoint.

### Get Playlist

    GET moodapi/playlists/
   Use the above headers to make this query.

### Generate Moodset Playlist

    POST moodapi/generate/
Use the above headers and the following body:

    {
	"vsv":0.5,
	"vse":0.3,
	"vev":0.3,
	"vee":0.7,
	"duration":60
	}
Here `vsv` and `vse` are the starting valence and energy values respectively. And `vev` and `vee` are the ending valence and energy values respectively. All of these values are in range [0,1]. `duration` is in minutes.

