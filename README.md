# SpotiPlays - a WEB application for manage [spotifyd](https://github.com/Spotifyd/spotifyd) with multiaccounts.

![Python application](https://github.com/Addovej/spotiplays/workflows/Python%20application/badge.svg?branch=master)
![Dockerhub build](https://github.com/Addovej/spotiplays/workflows/Dockerhub%20build/badge.svg)


### Install
```bash
# Clone the repo
>> git clone https://github.com/Addovej/spotiplays.git

# Copy .env and fill them
>> cp .env.example .env
# You must specify a SECRET_KEY. Here used 'cryptography' module.
# To generate a new secret just call:
>> docker-compose run web python -c 'from cryptography.fernet import Fernet;print(Fernet.generate_key())'

# Fill spotifyd.conf file if it needs.
# More in an official documentation of spotifyd.
>> cp spotifyd.conf.example spotifyd.conf

# Run it
>> docker-compose up -d
```

### Usage
Go to http://0.0.0.0:8000 for list of accounts.

Go to http://0.0.0.0:8000/api/docs for view API documentation.

[Here](https://github.com/Spotifyd/spotifyd#configuration-file) full list of spotifyd configuration.

Add your spotify account credentials and apply them. After this it should work. 


# Note
This project in a progress development.
The full documentation will be soon.
