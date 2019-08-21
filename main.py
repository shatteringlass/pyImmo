import db
from scraper import ImmoScraper

def main():
    conn = db.create_or_open_db()
    for batch in ImmoScraper().scrape():
        db.insert_data(conn, batch)

if __name__ == '__main__':
    main()