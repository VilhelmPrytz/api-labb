# pubg-api-experiment

Experimenting with the [PUBG](https://developer.pubg.com/) API.

## Requirements

- Python 3.8.x
- A PUBG developer API key (see instructions below)
- [pipenv](https://github.com/pypa/pipenv)

## Use the script

Retrieve a development API key from [developer.pubg.com](https://developer.pubg.com/) (you need to sign-up with your PUBG account).

Create a file named `secret.json` and put your newly generated API key in the following format.

```json
{
    "api_key": "API key here!"
}
```

Make sure you have [pipenv](https://github.com/pypa/pipenv) installed.

Install all dependencies.

```bash
pipenv install
```

Enter the shell of the pipenv environment.

```bash
pipenv shell
```

Run the Python script.

```bash
python app.py
```

## Author

Script written by [Vilhelm Prytz](https://github.com/VilhelmPrytz).
