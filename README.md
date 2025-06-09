# Ekonn

> A general-purpose Discord bot with a focus on economy features


## Setup

### Self host

Create a .env file with the following structure
```
BOT_TOKEN="<your token here>"
MONGODB_URI="<mongodb cluster link>"
```

Run the commands below to start up the bot in the background
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
nohup python bot.py &
```


## License

[GNU AGPL-3.0](https://choosealicense.com/licenses/agpl-3.0/)

