from datetime import datetime, timedelta, timezone
from typing import Any
import httpx
from app.collectors.base import BaseCollector

NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"

_SEVERITY_MAP = {
    (9.0, 10.0): "CRITICAL", (7.0, 8.9): "HIGH",
    (4.0, 6.9): "MEDIUM",    (0.1, 3.9): "LOW",
}


def _severity(score: float | None) -> str:
    if score is None:
        return "INFO"
    for (lo, hi), label in _SEVERITY_MAP.items():
        if lo <= score <= hi:
            return label
    return "INFO"


class CVECollector(BaseCollector):
    async def collect(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        now = datetime.now(timezone.utc)
        pub_start = (now - timedelta(hours=48)).strftime("%Y-%m-%dT%H:%M:%S.000")
        pub_end = now.strftime("%Y-%m-%dT%H:%M:%S.000")
        params = {
            "pubStartDate": pub_start, "pubEndDate": pub_end,
            "resultsPerPage": "100", "startIndex": "0",
        }
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(NVD_API, params=params)
                if resp.status_code != 200:
                    print(f"[CVE] NVD returned {resp.status_code}")
                    return results
                data = resp.json()
                for item in (data.get("vulnerabilities") or []):
                    cve = item.get("cve", {})
                    cve_id = cve.get("id", "")
                    if not cve_id:
                        continue
                    desc_list = cve.get("descriptions", [])
                    desc = next((d["value"] for d in desc_list if d.get("lang") == "en"), "")
                    # CVSS
                    metrics = cve.get("metrics", {})
                    score = None
                    vector = None
                    for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
                        if key in metrics and metrics[key]:
                            m = metrics[key][0].get("cvssData", {})
                            score = m.get("baseScore")
                            vector = m.get("vectorString")
                            break
                    # Affected products
                    products: list[str] = []
                    for cfg in (cve.get("configurations") or []):
                        for node in (cfg.get("nodes") or []):
                            for match in (node.get("cpeMatch") or []):
                                cpe = match.get("criteria", "")
                                if cpe:
                                    products.append(cpe[:256])
                    # CWE
                    cwes = [w.get("value","") for w in cve.get("weaknesses",[]) for w in w.get("description",[])]
                    pub_str = cve.get("published", "")
                    pub = None
                    try:
                        pub = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
                    except Exception:
                        pub = now
                    refs = [r.get("url","") for r in (cve.get("references") or []) if r.get("url")]
                    results.append({
                        "indicator_id": cve_id,
                        "title": f"{cve_id}: {desc[:120]}",
                        "description": desc,
                        "indicator_type": "CVE",
                        "severity": _severity(score),
                        "cvss_score": score,
                        "cvss_vector": vector,
                        "affected_products": products[:20],
                        "references": refs[:10],
                        "cwe_ids": [c for c in cwes if c][:10],
                        "source_name": "NVD",
                        "published_at": pub,
                        "modified_at": pub,
                    })
        except Exception as exc:
            print(f"[CVE] Collection error: {exc}")
        return results
