import argparse
from app import main

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-host', required=False, default='0.0.0.0', help='host')
    parser.add_argument('-port', required=False, default=5000, help='port')
    args = parser.parse_args()

    print(f'----> USE: localhost:{args.port}')
    main.app.run(host=args.host, port=args.port, debug=False)
    