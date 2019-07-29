from MiniMonkey import MiniMonkey
import click
import yaml
import time


def paus(mm):
    time.sleep(0.1)
    print(mm.recv())


@click.command()
@click.option('--host', default='localhost')
@click.option('--token', default='myToken')
@click.option('--config', default='provision.yaml')
def main(host, token, config):
    mm = MiniMonkey()
    mm.start()

    mm.auth(token)
    paus(mm)

    data = yaml.safe_load(open(config))

    tokens = {}
    for name, info in data['users'].items():
        tokens[name] = info['token']

    for name, info in data['devices'].items():
        tokens[name] = info['token']

    for token in tokens.values():
        print(token)
        mm.add_login(token)
        paus(mm)

    for name, info in data['rooms'].items():
        mm.enter(name)
        paus(mm)

        for publisher in info['publishers']:
            mm.add_publish(tokens[publisher])
            paus(mm)

        for subscriber in info['subscribers']:
            mm.add_subscribe(tokens[subscriber])
            paus(mm)

    time.sleep(2)

    mm.should_run = False


if __name__ == '__main__':
    main()
