from traceback import print_tb

import click


@click.command()
@click.option("--moves", help="all moves happened")
def main(moves):
    print(moves)


if __name__ == "__main__":
    main()
