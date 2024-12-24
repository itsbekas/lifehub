import sys

from dotenv import load_dotenv

from lifehub.config.checks import pre_run_checks


def run() -> None:
    pre_run_checks()

    if len(sys.argv) < 2:
        raise ValueError("Please provide a fetch script to run")

    fetch_script = sys.argv[1]

    load_dotenv()

    match fetch_script:
        case "trading212":
            from lifehub.providers.trading212.fetcher import Trading212Fetcher

            Trading212Fetcher().fetch()
        case "ynab":
            from lifehub.providers.ynab.fetcher import YNABFetcher

            YNABFetcher().fetch()
        case "all":
            from lifehub.providers.trading212.fetcher import Trading212Fetcher
            from lifehub.providers.ynab.fetcher import YNABFetcher

            Trading212Fetcher().fetch()
            YNABFetcher().fetch()
        case _:
            raise ValueError(f"Fetch script {fetch_script} not found")


if __name__ == "__main__":
    run()
