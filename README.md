# Overview

**Playlisty** is a web application in which, for the time being, you can generate Spotify’s playlists by selecting artists. In the long term, it will be able to generate playlists with various inputs (artists, songs, genres…) and modes.

### Implementation

This application is being develped with **[python](https://www.python.org/)** and **[Django’s](https://www.djangoproject.com/)** Framework. For the thime being, it is hosted by **[railway.app](https://railway.app/)** using **[PostgreSQL](https://www.postgresql.org/)** as database.

### Links

[Playlisty](https://playlisty.up.railway.app/)

[https://github.com/osoyinas/playlisty](https://github.com/osoyinas/playlisty)

# Getting started

First, make sure you have installed **[Git](https://git-scm.com/)** and a [**Github**](https://github.com/) account. To clone the repository execute:

```bash
git clone https://github.com/osoyinas/playlisty.git
```

Then, install the project’s dependencies written in `requirements.txt`. It is highly recommended to work with a virtual environment like virtualenv. See how it works [here](https://docs.python.org/3/library/venv.html).

```bash
pip install -r requirements.txt
```

Now, you will have to configure a `.env` config file. In this file we will append tokens, keys and options that modifies the behaviour of the app. This file cannot be shared with anyone but developers of this project. See how it works [here](https://levelup.gitconnected.com/what-are-env-files-and-how-to-use-them-in-nuxt-7f194f083e3d).

```bash
DJANGO_SECRET_KEY = djangosecretkeyexample
SPOTIFY_CLIENT_ID = spotifyid
SPOTIFY_CLIENT_SECRET = spotifysecret
HOST_URL = http://127.0.0.1:8000/
DEBUG = 1
DATABASE_DEBUG = 1
```

After all, you should be able to run Playlisty in a local server. Execute:

```bash
python3 manage.py runserver
```

If everything is correct, you will get:

```bash
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 12, 2023 - 16:05:06
Django version 4.1.4, using settings 'DjangoPlaylisty.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Now you can visit your local server by connecting to `http://127.0.0.1:8000/` . If you had any problem, do not hesitate to contact osoyinas@gmail.com.
