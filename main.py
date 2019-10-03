import argparse

def main(args):
    print(args.query)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Fetch data on musical artists and bands.')
    parser.add_argument('query',  type=str, nargs='+',
                        help='The band or artist to search for.')
    args = parser.parse_args()
    main(args)