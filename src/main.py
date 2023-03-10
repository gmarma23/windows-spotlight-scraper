from windows_spotlight_scraper import WindowsSpotlightScraper
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
    ws_scraper = WindowsSpotlightScraper()

    print('')
    if args.count:
        ws_scraper.download_images(args.count)
    else:
        ws_scraper.download_images()
    print('')


if __name__ == '__main__':
    main()
