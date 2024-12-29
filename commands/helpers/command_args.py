import argparse

def parse_args(argument_name):
    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument(f'--{argument_name}', type=str)
    args = parser.parse_args()
    return args
