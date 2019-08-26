import db
import time

from scraper import ImmoScraper


def get_ad_ids(scraper, db_conn):
    for batch in scraper.get_all_urls():
        db.insert_data(db_conn, batch)


"""
1. get all IDs from DB -> for each ID
    a. scrape page for ID into object
    b. store object into DB and commit
"""


def load_ads(scraper, db_conn):
    ads = list()
    GROUP_SIZE = 10
    for adid in db.get_data(db_conn):
        a = scraper.get_ad(adid[0])
        if not(a):
            continue
        ads.append(a.to_tuple())
        if len(ads) == GROUP_SIZE:
            db.insert_data(conn=db_conn, data=ads)
            db.delete_data(conn=db_conn, ids=[(ad[0],) for ad in ads])
            ads = list()
        time.sleep(1)
    db.insert_data(conn=db_conn, data=ads)
    db.delete_data(conn=db_conn, ids=[(ad[0],) for ad in ads])


def main():
    scraper = ImmoScraper()
    conn = db.create_or_open_db()
    #get_ad_ids(scraper=scraper, conn=conn)
    #print_ad(scraper, '30843586')
    #scraper.get_ad('51804493')
    load_ads(scraper, conn)


if __name__ == '__main__':
    main()
