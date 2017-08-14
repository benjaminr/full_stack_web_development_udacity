# Neighbourhood App
Built using Flask, an app to lookup local gigs in your area!

Integrates SONGKICK with Google Maps!

The live public version can be found at https://bens-blog.appspot.com

## Prereqs
Depends on Python and libraries specified in requirements. Easily deployed to Heroku.

## Usage

Visit https://calm-spire-17879.herokuapp.com/

The buttons in the bottom right filter concerts and festivals.

Clicking a card will show its marker on the map.

Cards link through to Songkick pages.

### Local
Clone this repo, cd into the cloned repo directory and execute the following:
```bash
python app.py
```
This will launch a local Flask webserver at 127.0.0.1.

You may need to enable unsecure scripts to load in Chrome, as the Songkick API is currently issued over HTTP and everything else is HTTPS.

