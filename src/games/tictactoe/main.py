import click
import game


@click.command()
@click.option("--path_bot1", type=click.Path(exists=True), help="path to bot1 script")
@click.option("--path_bot2", type=click.Path(exists=True), help="path to bot2 script")
@click.option("--timeout", default=500, help="timeout per move, default 500ms")
def main(path_bot1, path_bot2, timeout):
    game.main(path_bot1=path_bot1, path_bot2=path_bot2, timeout=timeout)


if __name__ == "__main__":
    main()
