from statistics import median


def summarize(rows: list[dict]) -> dict:
    samples = [x for x in rows if x.get("type") == "sample"]
    if not samples:
        return {"samples": 0}
    rss = [int(x["rss_kb"]) for x in samples]
    children = [int(x.get("child_rss_kb", 0)) for x in samples]
    total = [a + b for a,b in zip(rss, children)]
    duration = max(float(x["t_seconds"]) for x in samples)
    warm_cut = duration * .25
    steady = [
        int(x["rss_kb"]) + int(x.get("child_rss_kb", 0))
        for x in samples
        if float(x["t_seconds"]) >= warm_cut
    ]
    return {
        "samples": len(samples),
        "duration_seconds": duration,
        "peak_process_rss_mb": max(rss) / 1024,
        "peak_tree_rss_mb": max(total) / 1024,
        "median_tree_rss_mb": median(total) / 1024,
        "median_steady_tree_rss_mb": median(steady or total) / 1024,
        "first_tree_rss_mb": total[0] / 1024,
        "last_tree_rss_mb": total[-1] / 1024,
        "growth_mb": (total[-1] - total[0]) / 1024,
    }


def compare(left: list[dict], right: list[dict]) -> dict:
    a = summarize(left)
    b = summarize(right)
    keys = ["peak_tree_rss_mb", "median_steady_tree_rss_mb", "growth_mb"]
    return {
        key: b.get(key, 0) - a.get(key, 0)
        for key in keys
    }
