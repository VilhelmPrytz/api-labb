import requests
import click

from json import loads, dumps


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
    click.echo(
        f"Response HTTP code: {click.style(str(r.status_code), bold=True, fg='red')}"
    )

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

    click.echo(
        f"Response HTTP code: {click.style(str(r.status_code), fg='green', bold=True)}"
    )

    players = []

    for player in r.json()["data"]:
        players.append(player)

    return platform, players


def lifetime_stats(platform, players):
    base_url = "https://api.pubg.com/shards/{}/players/{}/seasons/lifetime"

    for player in players:
        url = base_url.format(platform, player["id"])

        click.echo(f"{click.style('Retrieving', bold=True)} {url}")
        r = requests.get(url, headers=HEADERS)

        if r.status_code != requests.codes.ok:
            _handle_exception(r)

        click.echo(
            f"Response HTTP code: {click.style(str(r.status_code), fg='green', bold=True)}"
        )

        click.secho(
            f"Statistics for {player['attributes']['name']} (curated list of variables shown, more are available within the API)",
            bold=True,
        )

        # print the amount of wins and kills this user has for each gamemode
        for k, v in r.json()["data"]["attributes"]["gameModeStats"].items():
            click.echo(f"{click.style(str(k), fg='green')} wins - {v['wins']}")
            click.echo(f"{click.style(str(k), fg='green')} kills - {v['kills']}")
            click.echo(
                f"{click.style(str(k), fg='green')} rounds played - {v['roundsPlayed']}"
            )
            click.echo(
                f"{click.style(str(k), fg='green')} distance walked - {v['walkDistance']}"
            )
            click.echo(f"{click.style(str(k), fg='green')} suicides - {v['suicides']}")
            click.echo(
                f"{click.style(str(k), fg='green')} damage dealt - {v['damageDealt']}"
            )


def main():
    platform, players = player_info()
    lifetime_stats(platform, players)


if __name__ == "__main__":
    main()
