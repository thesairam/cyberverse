from datetime import datetime, timezone
from typing import Any
import httpx
from app.collectors.base import BaseCollector
from app.config import get_settings

YT_SEARCH_API = "https://www.googleapis.com/youtube/v3/search"
QUERIES = [
    "cybersecurity live stream",
    "hacking conference live",
    "AI artificial intelligence live",
    "ransomware cybersecurity news",
    "AI policy technology live",
    "DEF CON Black Hat live",
]


class YouTubeCollector(BaseCollector):
    async def collect(self) -> list[dict[str, Any]]:
        api_key = get_settings().YOUTUBE_API_KEY
        if not api_key:
            return []
        results: list[dict[str, Any]] = []
        async with httpx.AsyncClient(timeout=20.0) as client:
            for q in QUERIES:
                try:
                    resp = await client.get(YT_SEARCH_API, params={
                        "key": api_key, "q": q, "part": "snippet",
                        "type": "video", "eventType": "live",
                        "maxResults": "10", "order": "viewCount",
                    })
                    if resp.status_code != 200:
                        continue
                    for item in (resp.json().get("items") or []):
                        vid_id = item.get("id", {}).get("videoId", "")
                        snip = item.get("snippet", {})
                        title = snip.get("title", "")
                        if not vid_id or not title:
                            continue
                        results.append({
                            "video_id": vid_id,
                            "title": title[:512],
                            "channel_name": snip.get("channelTitle", ""),
                            "channel_id": snip.get("channelId", ""),
                            "stream_url": f"https://www.youtube.com/watch?v={vid_id}",
                            "thumbnail_url": snip.get("thumbnails", {}).get("high", {}).get("url"),
                            "is_live": True,
                            "category_tags": q.split()[:4],
                            "started_at": datetime.now(timezone.utc),
                        })
                except Exception as exc:
                    print(f"[YouTube] query={q!r} error: {exc}")
        seen, unique = set(), []
        for r in results:
            if r["video_id"] not in seen:
                seen.add(r["video_id"])
                unique.append(r)
        return unique
