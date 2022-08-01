import json
import logging
from datetime import datetime

from lxml.etree import HTML, XML

from .download import Downloader


logger = logging.getLogger("logger")


try:
    local_timezone = datetime.utcnow().astimezone().tzinfo
except Exception as e:
    logger.error(f"parser.local_timezone error: {e}")
    local_timezone = None


def parse_url(url: str) -> str:
    # If the url is a youtube channel, then convert it to its rss url
    if "youtube.com/channel/" in url:
        channel_id = url.split("youtube.com/channel/")[1].split("/")[0]
        return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    elif "youtube.com/user/" in url:
        username = url.split("youtube.com/user/")[1].split("/")[0]
        return f"https://www.youtube.com/feeds/videos.xml?user={username}"
    elif "youtube.com/c/" in url:
        # extract the channel id from the web page
        downloader = Downloader()
        response = downloader.get_accept_cookies(url)
        html = HTML(response.content)
        try:
            feed_url = html.xpath("//link[@type='application/rss+xml']")[0].get("href")
        except IndexError:
            feed_url = ""
            logger.error(f"parse_url: RSS feed url could not be extracted from '{url}' ({response.url})")
        return feed_url
    elif "soundcloud.com/" in url and not "soundcloud:users" in url:
        # extract the user id from the web page
        downloader = Downloader()
        response = downloader.get(url)
        html = HTML(response.content)
        try:
            j = json.loads(html.xpath("//script[contains(text(),'window.__sc_hydration')]")[0].text.lstrip("window.__sc_hydration = ").rstrip(";"))
            for l in j:
                if l["hydratable"] == "user":
                    user_id = l["data"]["id"]
                    feed_url = f"https://feeds.soundcloud.com/users/soundcloud:users:{user_id}/sounds.rss"
                    return feed_url
            return url
        except IndexError:
            feed_url = ""
            logger.error(f"parse_url: RSS feed url could not be extracted from '{url}' ({response.url})")
        return url
    else:
        return url.rstrip("/")


def parse_feed(feed_bytes: bytes, feed_type: str = "", author: str = "") -> dict:
    try:
        root = XML(feed_bytes)
    except Exception as e:
        logger.debug(f"parse_feed: parsing {feed_type} failed: {e}")
        return {}

    if feed_type == "youtube":
        prefixes = {prefix: "{" + root.nsmap[prefix] + "}" for prefix in root.nsmap.keys()}
        prefix = prefixes[None]
        entries = root.findall(prefix + "entry")
        author = root.find(prefix + "author").find(prefix + "name").text if author == "" else author
    else:
        entries = root.xpath("//item")
        author = root.xpath("//*[local-name()='name']")[0].text if author == "" else author

    feed = {
        "author": author,
        "type": feed_type,
        "entries": {}
    }

    for i, entry in enumerate(entries):
        try:
            if feed_type == "youtube":
                date_published = datetime.strptime(entry.find(prefix + "published").text, "%Y-%m-%dT%H:%M:%S%z").astimezone(local_timezone)
                date_updated = datetime.strptime(entry.find(prefix + "updated").text, "%Y-%m-%dT%H:%M:%S%z").astimezone(local_timezone)

                group = entry.find(prefixes["media"] + "group")
                community = group.find(prefixes["media"] + "community")

                feed["entries"].update({
                    i: {
                        "title": entry.find(prefix + "title").text,
                        "link": entry.find(prefix + "link", {}).get("href"),
                        "link_raw": entry.find(prefix + "link", {}).get("href"),
                        "published": date_published.strftime("%Y-%m-%dT%H:%M:%S"),
                        "updated": date_updated.strftime("%Y-%m-%dT%H:%M:%S"),
                        "entry_id": entry.find(prefix + "id").text,
                        "author": entry.find(prefix + "author").find(prefix + "name").text if author == "" else author,
                        "thumbnail": group.find(prefixes["media"] + "thumbnail").get("url"),
                        "description": group.find(prefixes["media"] + "description").text,
                        "views": int(community.find(prefixes["media"] + "statistics").get("views")),
                        "duration": "",
                        "rating_average": float(community.find(prefixes["media"] + "starRating").get("average")),
                        "rating_count": int(community.find(prefixes["media"] + "starRating").get("count"))
                    }
                })

            elif feed_type == "soundcloud":
                date_published = datetime.strptime(entry.xpath("*[local-name()='pubDate']")[0].text, "%a, %d %b %Y %H:%M:%S %z").astimezone(local_timezone)

                feed["entries"].update({
                    i: {
                        "title": entry.find("title").text,
                        "link": entry.find("link").text,
                        "link_raw": entry.find("enclosure", {}).get("url"),
                        "published": date_published.strftime("%Y-%m-%dT%H:%M:%S"),
                        "updated": date_published.strftime("%Y-%m-%dT%H:%M:%S"),
                        "entry_id": entry.find("guid").text,
                        "author": entry.xpath("*[local-name()='author']")[0].text if author == "" else author,
                        "thumbnail": entry.xpath("*[local-name()='image']")[0].get("href"),
                        "description": entry.find("description").text,
                        "views": 0,
                        "duration": entry.xpath("*[local-name()='duration']")[0].text,
                        "rating_average": 0,
                        "rating_count": 0
                    }
                })
                
        except Exception as e:
            logger.error(f"parse_feed: parsing entry {i} failed: {e}")

    return feed
