# SocialAuto - Booking App

[Demo site](http://socialauto.ddns.net) on Oracle Cloud Free Tier VM

## Installation

Clone the repo:

```sh
$ git clone https://github.com/flistell/pw-booking.git
```

Create Python venv and install requirements:

```sh
$ cd pw-booking/backend
$ python3 -mvenv .venv
$ . .venv/bin/activate
<.venv> $ pip3 install -r requirements.txt
<.venv> $ flask --app booking init-db
```

Install npm modules:

```sh
$ cd pw-booking/frontend-vue
$ npm install
```

## Run in dev mode

Run the Flask backend in dev mode:

```sh
$ cd pw-booking/backend
$ . .venv/bin/activate
<.venv> $ export DBFILE="your/db/file/path"
<.venv> $ export COOKIE_DOMAIN="localhost"
<.venv> $ flask --app booking --debug run
```

Run the frontend in dev mode:

```sh
$ cd pw-booking/frontend-vue
$ npm run dev --debug
```
