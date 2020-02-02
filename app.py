import requests
import click

from json import loads


with open("secret.json") as f:
    try:
        API_KEY = loads(f.read())["api_key"]
    except Exception as e:
        click.echo(
            f"could not read secret.json, error {click.style(str(e), bold=True)}"
        )
        exit(1)

HEADERS = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/vnd.api+json"}


def _handle_exception(r):
    click.echo(f"error {click.style(str(r.status_code), bold=True, fg='red')}")

    try:
        for error in r.json()["errors"]:
            click.echo(f"{error['title']} - {error['detail']}")
    except Exception:
        pass

    exit(1)


def player_info():
    click.echo("Query for PUBG player information")

    click.secho("Available Platforms", bold=True)
    platforms = ["kakao", "steam", "tournament", "psn", "xbox", "console"]
    for i in platforms:
        click.echo(f"{i}")

    platform = click.prompt(
        "Which platform would you like to query for?", default="steam"
    ).lower()

    if platform not in platforms:
        click.echo(f"{platform} is not a valid platform")
        exit(1)

    username = click.prompt(
        "Enter username you would like to query information from (comma separate to query for multiple users):",
        default="MrKaKisen",
    )

    url = (
        f"https://api.pubg.com/shards/{platform}/players?filter[playerNames]={username}"
    )

    click.echo(f"{click.style('Retrieving', bold=True)} {url}")
    r = requests.get(url, headers=HEADERS)

    if r.status_code != requests.codes.ok:
        _handle_exception(r)

    player_ids = []

    for player in r.json()["data"]:
        player_ids.append(player["id"])

    return platform, player_ids


def lifetime_stats(platform, player_ids):
    base_url = "https://api.pubg.com/shards/{}/players/{}/seasons/lifetime"

    for player_id in player_ids:
        url = base_url.format(platform, player_info)

        r = requests.get(url, headers=HEADERS)

        if r.status_code != requests.codes.ok:
            _handle_exception(r)

        click.echo(r.json())


def main():
    platform, player_ids = player_info()
    lifetime_stats(platform, player_ids)


if __name__ == "__main__":
    main()
