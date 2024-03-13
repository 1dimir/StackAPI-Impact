import argparse
from stackapi_impact import StackExchangeImpact


def main():
    parser = argparse.ArgumentParser(
        prog="get-so-impact",
        description="Sample calculation of user's impact on StackOverflow")

    parser.add_argument("user_id", type=int, help="Id of a user")
    parser.add_argument("-k", "--api-key", type=str, help="Use an API key", dest='api_key')

    args = parser.parse_args()

    impact = StackExchangeImpact(api_key=args.api_key)
    result = impact.calculate(args.user_id)

    print(result)


if __name__ == '__main__':
    main()
