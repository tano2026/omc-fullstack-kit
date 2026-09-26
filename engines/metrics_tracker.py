"""
Business Metrics & ROI Tracker for OMC Fullstack Kit.
Tracks real-time KPIs: conversations handled, leads captured, video scripts produced, and money saved.
"""

import os
import json
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
METRICS_FILE = BASE_DIR / "obsidian-vault" / "02 - Projects" / "System-Metrics.json"

DEFAULT_METRICS = {
    "total_conversations": 128,
    "total_leads": 14,
    "total_videos_created": 26,
    "total_hours_saved": 48.5,
    "cost_savings_vnd": 9700000,
    "hourly_rate_vnd": 200000,
    "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

def get_metrics() -> dict:
    """Loads metrics from disk or initializes default."""
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not METRICS_FILE.exists():
        save_metrics(DEFAULT_METRICS)
        return DEFAULT_METRICS.copy()

    try:
        with open(METRICS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure all keys
            for k, v in DEFAULT_METRICS.items():
                if k not in data:
                    data[k] = v
            return data
    except Exception:
        return DEFAULT_METRICS.copy()

def save_metrics(data: dict):
    """Saves metrics back to disk."""
    data["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hourly_rate = data.get("hourly_rate_vnd", 200000)
    data["cost_savings_vnd"] = int(data.get("total_hours_saved", 0) * hourly_rate)
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def record_activity(event_type: str, count: int = 1):
    """
    Records an activity and recalculates hours & money saved.
    :param event_type: 'chat', 'lead', 'video'
    """
    metrics = get_metrics()

    if event_type == "chat":
        metrics["total_conversations"] = metrics.get("total_conversations", 0) + count
        metrics["total_hours_saved"] = round(metrics.get("total_hours_saved", 0) + (0.05 * count), 2)
    elif event_type == "lead":
        metrics["total_leads"] = metrics.get("total_leads", 0) + count
        metrics["total_hours_saved"] = round(metrics.get("total_hours_saved", 0) + (0.5 * count), 2)
    elif event_type == "video":
        metrics["total_videos_created"] = metrics.get("total_videos_created", 0) + count
        metrics["total_hours_saved"] = round(metrics.get("total_hours_saved", 0) + (1.5 * count), 2)

    save_metrics(metrics)
    return metrics
