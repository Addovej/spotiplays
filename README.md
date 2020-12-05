# Spotifyd playlists handler

## Currently this python app based on fastAPI which handle spotifyd daemon with home assistant


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
Go to http://0.0.0.0:8000

Add your spotify account credentials and apply them. After this it should work. 


# Note
This project in progress development.
The documentation will be soon.
