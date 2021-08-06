import logging
from datetime import datetime

from lxml.etree import XML

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
    else:
        return url.rstrip("/")


def parse_feed(feed_bytes: bytes, feed_type: str = "", author: str = "") -> dict:
    try:
        root = XML(feed_bytes)
    except Exception as e:
        logger.debug(f"parse_feed: parsing {feed_type} failed: {e}")
        return {}

    prefixes = {prefix: "{" + root.nsmap[prefix] + "}" for prefix in root.nsmap.keys()}
    prefix = prefixes[None]

    feed = {
        "author": root.find(prefix + "author").find(prefix + "name").text if author == "" else author,
        "type": feed_type,
        "entries": {}
    }

    entries = root.findall(prefix + "entry")
    for i, entry in enumerate(entries):
        # links = entry.findall(prefix + "link", {}) # can be multiple: e.g. "text/html", "image/jpg", ... for other feeds

        date_published = datetime.strptime(entry.find(prefix + "published").text, "%Y-%m-%dT%H:%M:%S%z").astimezone(local_timezone)
        date_updated = datetime.strptime(entry.find(prefix + "updated").text, "%Y-%m-%dT%H:%M:%S%z").astimezone(local_timezone)
        try:
            feed["entries"].update({
                i: {
                    "title": entry.find(prefix + "title").text,
                    "link": entry.find(prefix + "link", {}).get("href"),
                    "entry_id": entry.find(prefix + "id").text,
                    "published": date_published.strftime("%Y-%m-%dT%H:%M:%S"),
                    "updated": date_updated.strftime("%Y-%m-%dT%H:%M:%S"),
                }
            })

            if feed_type == "youtube":
                group = entry.find(prefixes["media"] + "group")
                community = group.find(prefixes["media"] + "community")
                feed["entries"][i].update({
                    "author": entry.find(prefix + "author").find(prefix + "name").text if author == "" else author,
                    "thumbnail": group.find(prefixes["media"] + "thumbnail").get("url"),
                    "description": group.find(prefixes["media"] + "description").text,
                    "views": int(community.find(prefixes["media"] + "statistics").get("views")),
                    "rating_average": float(community.find(prefixes["media"] + "starRating").get("average")),
                    "rating_count": int(community.find(prefixes["media"] + "starRating").get("count"))
                })
        except Exception as e:
            logger.error(f"parse_feed: parsing entry {i} failed: {e}")

    return feed
