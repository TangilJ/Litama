# Litama
Litama is a WebSocket server for the Onitama board game written in Python. A live version of this is available at `wss://litama.herokuapp.com`. To make a client that communicates with this server, see the [wiki page](https://github.com/TheBlocks/Litama/wiki) on this repository. If you'd like to be able to run this server, follow the instructions below to get started.

## Getting started

### Prerequisites

#### Python

You'll need Python 3.6 or higher to run Litama: https://www.python.org/downloads/

You'll also need to install Litama's dependencies. The requirements.txt file has all the dependencies listed. Install them with:

```
pip install -r requirements.txt
```

#### MongoDB

If you want to run the database locally, you will need to install MongoDB. The free community version can be found here: https://www.mongodb.com/try/download/community

Alternatively, you can run the database on the cloud. You may wish to look into MongoDB Atlas for free hosting of small projects: https://www.mongodb.com/cloud/atlas


You will also need to set up `MONGODB_HOST` as an environment variable. This should be a URI to the `mongod` instance.
When running locally, it should look something like this: `mongodb://localhost:27017/`.
If you are using MongoDB Atlas, it will look similar to this: `mongodb+srv://username:password@clustername.abcde.mongodb.net/dbname`. If you are using MongoDB Atlas, visit the cluster page on the Atlas website to find the connection URI you should use.

You shouldn't need to set up the database manually. If you find issues with not being able to access or store data, make sure you have a database called `litama` with a collection called `matches`. Create this database if it was not created automatically and you are running into issues.


### Running Litama

You need to run the `mongod` daemon before running Litama:
```
mongod.exe (on Windows)
mongod (on Linux/macOS)
```
If the executable can't be found, add it to your PATH or run it from the installation directory (usually `C:\Program Files\MongoDB\Server\4.x\bin\mongod.exe` on Windows).

Now you should be ready to run Litama:
```
cd litama
python server.py
```

By default, the webpage can be found at `http://127.0.0.1:5000` and you can connect to the server with WebSocket at `ws://127.0.0.1:5000`.


## Built with

- [Python](http://python.org)
- [Flask](https://github.com/pallets/flask)
- [Flask-Sockets](https://github.com/heroku-python/flask-sockets)
- [MongoDB](https://www.mongodb.com/)


## License

This project is licensed under the Mozilla Public License Version 2.0. See the [LICENSE](https://github.com/TheBlocks/Litama/blob/master/LICENSE) file for details.
