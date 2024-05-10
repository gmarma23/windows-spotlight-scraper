from wss import WindowsSpotlightScraper
import argparse


def parse_args():
    arg_parser = argparse.ArgumentParser(prog='Windows Spotlight Scraper')
    arg_parser.add_argument(
        '-c', '--count', 
        action = 'store', 
        type = int, 
        required = False, 
        help = 'Number of most recent images to scrape'
    )
    return arg_parser.parse_args()


def main():
    args = parse_args()
    wss = WindowsSpotlightScraper()

    print()
    wss.download_images(args.count)
    print()


if __name__ == '__main__':
    main()