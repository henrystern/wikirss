"""Clean and output data."""

from datetime import datetime
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from loguru import logger
import requests

from wikirss.config import (
    LOGS_DIR,
    MAIN_PAGE_HISTORY_URL,  # noqa: F401
    MAIN_PAGE_URL,
    PROCESSED_DATA_DIR,
)


def scrape_main_page(url, headers):
    """Scrape Wikipedia's main page and return clean HTML for each section."""
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    main_page_sections = {
        "From today's featured article": "mp-tfa",
        "In the news": "mp-itn",
        "Did you know": "mp-dyk",
        "On this day": "mp-otd",
        "Today's featured picture": "mp-tfp",
    }
    to_exclude = ["noprint"]
    content = []
    for section, html_id in main_page_sections.items():
        section_content = soup.find(id=html_id)
        if section_content is None:
            logger.warning(f"Section {section} with id {html_id} not found.")
            continue
        for tag in section_content.find_all(class_=to_exclude):
            tag.decompose()
        content.append(f"<h2>{section}</h2>")
        content.append(str(section_content))
    content = "\n".join(content)
    logger.success("Scraped main page content.")
    return content


def get_last_change(url, headers, tz=ZoneInfo("America/Toronto")):
    """Get the last change date and permalink from the main page history."""
    hist_response = requests.get(url, headers=headers, timeout=10)
    hist_response.raise_for_status()

    hist_soup = BeautifulSoup(hist_response.text, "html.parser")
    last_change = hist_soup.find("a", class_="mw-changeslist-date")
    if last_change is None:
        logger.warning("Could not find last change in page history.")
        date = datetime.now(tz=tz).isoformat()
        permalink = MAIN_PAGE_URL
    else:
        date = (
            datetime.strptime(last_change.get_text(), "%H:%M, %d %B %Y")
            .replace(tzinfo=tz)
            .isoformat()
        )
        permalink = last_change.get("href")
        logger.success("Retrieved last change date and permalink.")
    return date, permalink


def update_feed(date, permalink, content):
    """Update the RSS and Atom feeds with the latest main page content."""
    fg = FeedGenerator()
    fg.id("http://hstern.ca/wikirss")
    fg.title("Wikipedia Main Page")
    fg.link(href=MAIN_PAGE_URL, rel="alternate")
    fg.description("RSS feed generated daily from Wikipedia's main page.")
    fg.language("en")

    fe = fg.add_entry()
    fe.id(permalink)
    fe.title(f"Wikipedia Main Page—{date[:10]}")
    fe.link(href=permalink)
    fe.published(date)
    fe.content(content, type="html")

    fg.atom_file(PROCESSED_DATA_DIR / "atom.xml")
    fg.rss_file(PROCESSED_DATA_DIR / "rss.xml")
    logger.success("Updated RSS and Atom feeds.")


if __name__ == "__main__":
    logger.add(LOGS_DIR / "dataset.log")

    user_agent = ""
    headers = {"User-Agent": user_agent, "Accept-encoding": "gzip"}

    content = scrape_main_page(MAIN_PAGE_URL, headers)
    # BUG: history doesn't record content changes so just return date and regular link
    # date, permalink = get_last_change(MAIN_PAGE_HISTORY_URL, headers)
    date = datetime.now(tz=ZoneInfo("America/Toronto")).isoformat()
    permalink = MAIN_PAGE_URL

    update_feed(date, permalink, content)
