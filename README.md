# SpotiPlays - a WEB application for manage [spotifyd](https://github.com/Spotifyd/spotifyd) with multiaccounts.

[![Lint and Tests](https://github.com/Addovej/spotiplays/actions/workflows/lint_and_tests.yml/badge.svg)](https://github.com/Addovej/spotiplays/actions/workflows/lint_and_tests.yml)
[![Dockerhub build](https://github.com/Addovej/spotiplays/actions/workflows/dockerhub.yml/badge.svg)](https://github.com/Addovej/spotiplays/actions/workflows/dockerhub.yml)


### Install
```bash
# Clone the repo
git clone https://github.com/Addovej/spotiplays.git

# Copy .env and fill them
cp .env.example .env

# You must specify a SECRET_KEY. Here used 'cryptography' module.
# To generate a new secret just call:
make generate-secret

# Run it
make start
```

To get help for more commands type:
```bash
make help
```

### Usage
Go to http://0.0.0.0:8000 for list of accounts.

Go to http://0.0.0.0:8000/api/docs for view API documentation.

[Here](https://spotifyd.github.io/spotifyd/config/File.html) full list of spotifyd configuration.

Add your spotify account credentials and apply them. After this it should work. 


# Note
This project in a progress development.
The full documentation will be soon.
