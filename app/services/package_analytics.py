import io
import re
from typing import Any

import matplotlib
import pandas as pd
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.packages import Packages

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


PACKAGE_RESOURCE_TYPE = "App\\Models\\Admin\\Travel\\Package\\Package"


def _is_filled(value: Any) -> bool:
    return value is not None and str(value).strip() != ""


def _to_percent(count: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((count / total) * 100, 2)


def _extract_numeric_price(value: Any) -> float:
    if value is None:
        return 0.0
    text_value = str(value).replace(",", "")
    matches = re.findall(r"-?\d+(?:\.\d+)?", text_value)
    if not matches:
        return 0.0
    # Keep the largest parsed number in noisy strings like "From $1200 per person".
    return max(float(token) for token in matches)


async def _load_packages_with_relations(db: AsyncSession) -> list[Packages]:
    query = (
        select(Packages)
        .options(
            selectinload(Packages.package_overviews),
            selectinload(Packages.package_highlights),
            selectinload(Packages.package_attributes),
            selectinload(Packages.package_images),
            selectinload(Packages.package_seos),
        )
    )
    result = await db.execute(query)
    return result.scalars().all()


async def _load_main_image_package_ids(db: AsyncSession) -> set[int]:
    query = text(
        """
        SELECT DISTINCT resource_id
        FROM media_usage
        WHERE resource_type = :resource_type
          AND type = :usage_type
        """
    )
    result = await db.execute(
        query,
        {"resource_type": PACKAGE_RESOURCE_TYPE, "usage_type": "main_image"},
    )
    return {int(row.resource_id) for row in result if row.resource_id is not None}


def _first_or_none(values: list[Any]) -> Any:
    return values[0] if values else None


def _build_dataframe(packages: list[Packages], main_image_ids: set[int]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for package in packages:
        overviews = list(getattr(package, "package_overviews", []) or [])
        highlights = list(getattr(package, "package_highlights", []) or [])
        attributes = list(getattr(package, "package_attributes", []) or [])
        images = list(getattr(package, "package_images", []) or [])
        seos = list(getattr(package, "package_seos", []) or [])

        overview_has_100 = any(
            len(str(getattr(item, "description", "") or "").strip()) > 100 for item in overviews
        )
        highlight_has_100 = any(
            len(str(getattr(item, "description", "") or "").strip()) > 100 for item in highlights
        )

        prices = [_extract_numeric_price(getattr(attr, "price", None)) for attr in attributes]
        price_has_positive = any(price > 0 for price in prices)

        seo_has_complete = any(
            _is_filled(getattr(seo, "meta_title", None))
            and _is_filled(getattr(seo, "meta_description", None))
            and _is_filled(getattr(seo, "meta_keywords", None))
            for seo in seos
        )

        rows.append(
            {
                "package_id": int(package.id),
                "is_published": bool(getattr(package, "is_active", False)),
                "overview_complete": overview_has_100,
                "highlight_complete": highlight_has_100,
                "price_positive": price_has_positive,
                "image_count": len(images),
                "has_gis_data": _is_filled(getattr(package, "trailgis_map_id", None))
                and _is_filled(getattr(package, "trailgis_summary_response", None)),
                "seo_complete": seo_has_complete,
                "has_main_image": int(package.id) in main_image_ids,
                "seo_count": len(seos),
                "attribute_count": len(attributes),
                "overview_count": len(overviews),
                "highlight_count": len(highlights),
                "sample_price": _extract_numeric_price(getattr(_first_or_none(attributes), "price", None)),
            }
        )
    return pd.DataFrame(rows)


def _image_bucket(image_count: int) -> str:
    if image_count >= 4:
        return "4+"
    return str(image_count)


def _calculate_metrics(df: pd.DataFrame) -> dict[str, Any]:
    if df.empty:
        return {
            "totals": {"total_packages": 0, "published_packages": 0, "published_percent": 0.0},
            "published_metrics": {
                "overview_complete": {"count": 0, "percent": 0.0},
                "highlight_complete": {"count": 0, "percent": 0.0},
                "price_positive": {"count": 0, "percent": 0.0},
                "gis_complete": {"count": 0, "percent": 0.0},
                "seo_complete": {"count": 0, "percent": 0.0},
                "has_main_image": {"count": 0, "percent": 0.0},
            },
            "image_distribution": {
                "0": {"count": 0, "percent": 0.0},
                "1": {"count": 0, "percent": 0.0},
                "2": {"count": 0, "percent": 0.0},
                "3": {"count": 0, "percent": 0.0},
                "4+": {"count": 0, "percent": 0.0},
            },
            "meta": {"note": "No package records found."},
        }

    total_packages = int(len(df))
    published_df = df[df["is_published"] == True]  # noqa: E712
    published_packages = int(len(published_df))

    def metric_row(column: str) -> dict[str, float | int]:
        count = int(published_df[column].sum()) if published_packages > 0 else 0
        return {"count": count, "percent": _to_percent(count, published_packages)}

    image_counts = published_df["image_count"].apply(_image_bucket) if published_packages > 0 else pd.Series(dtype=str)
    distribution_counts = image_counts.value_counts().to_dict()
    ordered_buckets = ["0", "1", "2", "3", "4+"]
    image_distribution = {
        bucket: {
            "count": int(distribution_counts.get(bucket, 0)),
            "percent": _to_percent(int(distribution_counts.get(bucket, 0)), published_packages),
        }
        for bucket in ordered_buckets
    }

    return {
        "totals": {
            "total_packages": total_packages,
            "published_packages": published_packages,
            "published_percent": _to_percent(published_packages, total_packages),
        },
        "published_metrics": {
            "overview_complete": metric_row("overview_complete"),
            "highlight_complete": metric_row("highlight_complete"),
            "price_positive": metric_row("price_positive"),
            "gis_complete": metric_row("has_gis_data"),
            "seo_complete": metric_row("seo_complete"),
            "has_main_image": metric_row("has_main_image"),
        },
        "image_distribution": image_distribution,
        "meta": {
            "denominator": "published_packages",
        },
    }


async def get_package_health_analytics(db: AsyncSession) -> dict[str, Any]:
    try:
        packages = await _load_packages_with_relations(db)
    except Exception:
        packages = []

    try:
        main_image_package_ids = await _load_main_image_package_ids(db)
    except Exception:
        main_image_package_ids = set()

    try:
        df = _build_dataframe(packages, main_image_package_ids)
        return _calculate_metrics(df)
    except Exception:
        return {
            "totals": {"total_packages": 0, "published_packages": 0, "published_percent": 0.0},
            "published_metrics": {
                "overview_complete": {"count": 0, "percent": 0.0},
                "highlight_complete": {"count": 0, "percent": 0.0},
                "price_positive": {"count": 0, "percent": 0.0},
                "gis_complete": {"count": 0, "percent": 0.0},
                "seo_complete": {"count": 0, "percent": 0.0},
                "has_main_image": {"count": 0, "percent": 0.0},
            },
            "image_distribution": {
                "0": {"count": 0, "percent": 0.0},
                "1": {"count": 0, "percent": 0.0},
                "2": {"count": 0, "percent": 0.0},
                "3": {"count": 0, "percent": 0.0},
                "4+": {"count": 0, "percent": 0.0},
            },
            "meta": {"error": "Unable to calculate package analytics."},
        }


def build_package_health_figure(analytics: dict[str, Any]) -> bytes:
    totals = analytics.get("totals", {})
    published_percent = float(totals.get("published_percent", 0.0))

    metric_map = analytics.get("published_metrics", {})
    bars = [
        ("Overview", metric_map.get("overview_complete", {}).get("percent", 0.0)),
        ("Highlights", metric_map.get("highlight_complete", {}).get("percent", 0.0)),
        ("Price", metric_map.get("price_positive", {}).get("percent", 0.0)),
        ("GIS", metric_map.get("gis_complete", {}).get("percent", 0.0)),
        ("SEO", metric_map.get("seo_complete", {}).get("percent", 0.0)),
        ("Main Img", metric_map.get("has_main_image", {}).get("percent", 0.0)),
    ]

    image_distribution = analytics.get("image_distribution", {})
    image_labels = ["0", "1", "2", "3", "4+"]
    image_values = [float(image_distribution.get(label, {}).get("count", 0)) for label in image_labels]

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Gauge-like donut for publishing ratio.
    axes[0].pie(
        [published_percent, max(100.0 - published_percent, 0.0)],
        labels=["Published", "Unpublished"],
        autopct="%1.1f%%",
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.35},
    )
    axes[0].set_title("Publishing Status")

    bar_labels = [item[0] for item in bars]
    bar_values = [float(item[1]) for item in bars]
    axes[1].bar(bar_labels, bar_values)
    axes[1].set_ylim(0, 100)
    axes[1].set_title("Published Package Completeness")
    axes[1].set_ylabel("Percent")
    axes[1].tick_params(axis="x", rotation=25)

    axes[2].bar(image_labels, image_values)
    axes[2].set_title("Image Count Distribution")
    axes[2].set_xlabel("Images per package")
    axes[2].set_ylabel("Published package count")

    fig.tight_layout()
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=150)
    plt.close(fig)
    buffer.seek(0)
    return buffer.getvalue()
