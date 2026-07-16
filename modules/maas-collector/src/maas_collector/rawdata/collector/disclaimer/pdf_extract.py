"""PDF extraction for SAR-MPC Quality Disclaimer documents.

This module is the library form of the standalone ``pdf_extract.py`` tool
provided by the MPC team: the parsing logic is kept verbatim, only the CLI and
file-writing helpers were dropped. The collector calls :func:`extract_pdf`,
which returns the PDF metadata together with the structured Quality Disclaimer
fields for a single downloaded PDF.

The structured parser is tolerant: any field it cannot find is reported as
``None`` rather than raising, so it degrades gracefully on unexpected layouts.
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    import pdfplumber
except Exception:  # pragma: no cover - import guard
    pdfplumber = None

# Optional, only used as a text-extraction fallback if pdfplumber is missing.
try:
    from pypdf import PdfReader  # type: ignore
except Exception:  # pragma: no cover
    try:
        from PyPDF2 import PdfReader  # type: ignore
    except Exception:
        PdfReader = None


# --------------------------------------------------------------------------- #
# Extraction
# --------------------------------------------------------------------------- #
def extract_text(path: Path) -> list[str]:
    """Return a list of per-page text strings."""
    if pdfplumber is not None:
        texts: list[str] = []
        with pdfplumber.open(path) as pdf:
            for pg in pdf.pages:
                texts.append(pg.extract_text() or "")
        return texts

    if PdfReader is not None:
        reader = PdfReader(str(path))
        texts = []
        for p in reader.pages:
            try:
                texts.append(p.extract_text() or "")
            except Exception:
                texts.append("")
        return texts

    raise RuntimeError(
        "No PDF text extraction backend available. Install pdfplumber (or pypdf)."
    )


_PDF_DATE_RE = re.compile(
    r"D:(?P<Y>\d{4})(?P<m>\d{2})(?P<d>\d{2})"
    r"(?P<H>\d{2})?(?P<M>\d{2})?(?P<S>\d{2})?"
    r"(?P<tz>[Zz]|[+-]\d{2}'?\d{2}'?)?"
)


def _normalize_pdf_date(value: str) -> str:
    """Convert a PDF date string (``D:YYYYMMDDHHmmSS+hh'mm'``) to ISO 8601.

    Returns the original string unchanged if it does not match.
    """
    m = _PDF_DATE_RE.match(value.strip())
    if not m:
        return value
    g = m.groupdict()
    out = f"{g['Y']}-{g['m']}-{g['d']}"
    if g["H"]:
        out += f"T{g['H']}:{g['M'] or '00'}:{g['S'] or '00'}"
        tz = g["tz"]
        if tz in ("Z", "z"):
            out += "+00:00"
        elif tz:
            digits = tz.replace("'", "")
            out += f"{digits[:3]}:{digits[3:5]}"
    return out


def extract_metadata(path: Path) -> dict:
    """Return document metadata as a plain, JSON-serializable dict."""
    data: dict[str, str] = {}
    if pdfplumber is not None:
        with pdfplumber.open(path) as pdf:
            raw = pdf.metadata or {}
        for k, v in raw.items():
            key = str(k)
            val = str(v)
            if key in ("CreationDate", "ModDate"):
                val = _normalize_pdf_date(val)
            data[key] = val
        return data

    if PdfReader is not None:
        reader = PdfReader(str(path))
        md = reader.metadata
        if md:
            for k, v in md.items():
                data[str(k).lstrip("/")] = str(v)
    return data


# --------------------------------------------------------------------------- #
# Checkbox detection
# --------------------------------------------------------------------------- #
# In the Quality Disclaimer template the option checkboxes are NOT text: each
# box is a small square drawn as a rectangle, and a *checked* box has an "X"
# drawn over it with two diagonal line segments. So a box is "checked" when at
# least one line/curve segment has its midpoint inside the square.
#
# Each detected box is labelled with the first word to its right on the same
# row, then classified by that word into the disclaimer's option groups.

# value (first word) -> group name
_CHECKBOX_GROUPS: dict[str, str] = {}
for _v in (
    "DEGRADED_PRODUCT_RADIOMETRY", "DEGRADED_PRODUCT_GEOLOCATION",
    "DEGRADED_RADIOMETRIC_CALIBRATION", "DEGRADED_PLATFORM_POINTING",
    "DEGRADED_ORBIT_CONTROL", "DEGRADED_PERFORMANCE_INSTRUMENT_ANOMALY",
    "COMPLETE_PRODUCT_DEGRADATION", "SLICE_PRODUCT_NON_CONCATENABLE",
    "DEGRADED_PHASE", "OTHER",
):
    _CHECKBOX_GROUPS[_v] = "degradation_types"
for _v in ("S-1A", "S-1B", "S-1C", "S-1D"):
    _CHECKBOX_GROUPS[_v] = "platform"
for _v in ("EW", "IW", "SM", "WV", "RF"):
    _CHECKBOX_GROUPS[_v] = "acquisition_mode"
for _v in ("RAW", "SLC", "GRDM", "GRDH", "GRDF", "OCN"):
    _CHECKBOX_GROUPS[_v] = "product_type"
for _v in ("SH", "SV", "DH", "DV"):
    _CHECKBOX_GROUPS[_v] = "polarization"


def _detect_checkboxes(page) -> list[tuple[str, bool]]:
    """Return (label, checked) for every checkbox square on a pdfplumber page."""
    boxes = [
        r for r in page.rects
        if 6 <= r["width"] <= 12 and 6 <= r["height"] <= 12
        and abs(r["width"] - r["height"]) < 2
    ]
    segments = list(page.lines) + list(page.curves)
    words = page.extract_words()
    results: list[tuple[str, bool]] = []
    for b in boxes:
        cy = (b["top"] + b["bottom"]) / 2
        checked = any(
            b["x0"] - 1.5 <= (s["x0"] + s["x1"]) / 2 <= b["x1"] + 1.5
            and b["top"] - 1.5 <= (s["top"] + s["bottom"]) / 2 <= b["bottom"] + 1.5
            for s in segments
        )
        candidates = [
            w for w in words
            if w["x0"] >= b["x1"] - 2
            and abs((w["top"] + w["bottom"]) / 2 - cy) < 5
        ]
        candidates.sort(key=lambda w: w["x0"])
        if candidates:
            results.append((candidates[0]["text"], checked))
    return results


def extract_checkbox_selections(path: Path) -> dict | None:
    """Extract selected options from the disclaimer's checkbox groups.

    Returns a dict mapping group name -> list of selected values, or None if
    the geometry backend (pdfplumber) is unavailable.
    """
    if pdfplumber is None:
        return None
    groups: dict[str, list[str]] = {}
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            for label, checked in _detect_checkboxes(page):
                group = _CHECKBOX_GROUPS.get(label)
                if group is None:
                    continue
                groups.setdefault(group, [])
                if checked and label not in groups[group]:
                    groups[group].append(label)
    return groups or None


# --------------------------------------------------------------------------- #
# Sentinel-1 product naming convention
# --------------------------------------------------------------------------- #
# e.g. S1C_IW_GRDH_1SDV_20260625T152305_20260625T152336_008264_01056B_F534_COG.SAFE
_S1_PRODUCT_RE = re.compile(
    r"^(?P<mission>S1[ABCD])_"
    r"(?P<mode>[A-Z0-9]{2})_"
    r"(?P<ptype>[A-Z_]{3})(?P<resolution>[FHM_])_"
    r"(?P<level>[0-9])(?P<class>[SA])(?P<polarization>[SD][HV])_"
    r"(?P<start>\d{8}T\d{6})_"
    r"(?P<stop>\d{8}T\d{6})_"
    r"(?P<orbit>\d{6})_"
    r"(?P<datatake>[0-9A-Fa-f]{6})_"
    r"(?P<crc>[0-9A-Fa-f]{4})"
    r"(?:_(?P<cog>COG))?"
    r"\.SAFE$"
)

_POL_LABELS = {"SH": "Single pol. H", "SV": "Single pol. V",
               "DH": "Double pol. H", "DV": "Double pol. V"}

# Auxiliary / ADF products, e.g.
# S1C_AUX_INS_V20241204T000000_G20241204T092730.SAFE
_S1_AUX_RE = re.compile(
    r"^(?P<mission>S1[ABCD])_AUX_(?P<aux_type>[A-Z0-9]{3})_"
    r"V(?P<validity_start>\d{8}T\d{6})"
    r"(?:_(?P<validity_stop>\d{8}T\d{6}))?"
    r"_G(?P<generation>\d{8}T\d{6})"
    r"\.SAFE$"
)


def parse_sentinel1_product(name: str) -> dict | None:
    """Parse a Sentinel-1 SAFE product name into its components.

    Handles both SAR imagery products and auxiliary (AUX/ADF) products.
    Returns None if the name does not match a known Sentinel-1 convention.
    """
    name = name.strip()

    aux = _S1_AUX_RE.match(name)
    if aux:
        g = aux.groupdict()
        return {
            "name": name,
            "category": "AUX",
            "mission": g["mission"].replace("S1", "S-1"),
            "product_type": f"AUX_{g['aux_type']}",
            "validity_start": g["validity_start"],
            "validity_stop": g["validity_stop"],
            "generation": g["generation"],
        }

    m = _S1_PRODUCT_RE.match(name)
    if not m:
        return None
    g = m.groupdict()
    ptype = g["ptype"].rstrip("_")
    if ptype == "GRD" and g["resolution"] != "_":
        ptype = f"GRD{g['resolution']}"  # GRDH / GRDM / GRDF
    return {
        "name": name,
        "category": "SAR",
        "mission": g["mission"].replace("S1", "S-1"),
        "mode": g["mode"],
        "product_type": ptype,
        "processing_level": int(g["level"]),
        "polarization": g["polarization"],
        "polarization_label": _POL_LABELS.get(g["polarization"]),
        "sensing_start": g["start"],
        "sensing_stop": g["stop"],
        "absolute_orbit": int(g["orbit"]),
        "datatake_id_hex": g["datatake"].upper(),
        "crc": g["crc"].upper(),
        "cog": bool(g["cog"]),
    }


# --------------------------------------------------------------------------- #
# Quality Disclaimer parsing
# --------------------------------------------------------------------------- #
# Footer that repeats on every page; strip it out of captured sections.
_FOOTER_RE = re.compile(
    r"All dates in the document are provided in UTC\s*\d*\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def _clean(text: str | None) -> str | None:
    if text is None:
        return None
    text = _FOOTER_RE.sub("", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()
    return text or None


def _section(text: str, start_label: str, *end_labels: str) -> str | None:
    """Return the text between ``start_label`` and the first end label found."""
    sm = re.search(rf"^{re.escape(start_label)}[ \t]*\n?", text, re.MULTILINE)
    if not sm:
        return None
    rest = text[sm.end():]
    end = len(rest)
    for label in end_labels:
        em = re.search(rf"^{re.escape(label)}", rest, re.MULTILINE)
        if em:
            end = min(end, em.start())
    return _clean(rest[:end])


def _first(text: str, pattern: str) -> str | None:
    m = re.search(pattern, text, re.MULTILINE)
    return m.group(1).strip() if m else None


def parse_quality_disclaimer(
    full_text: str, checkboxes: dict | None = None
) -> dict | None:
    """Parse a SAR-MPC Quality Disclaimer document into structured fields.

    ``checkboxes`` is the optional output of :func:`extract_checkbox_selections`
    (which requires the PDF geometry, not just its text). When provided, the
    selected degradation types and product-selection criteria are included.

    Returns None if the document does not look like a Quality Disclaimer.
    """
    header = re.search(
        r"S\s*ENTINEL-(?P<mission>\d[A-Z]?).*?Quality Disclaimer\s*No\.?\s*(?P<num>\d+)",
        full_text,
        re.IGNORECASE | re.DOTALL,
    )
    if not header:
        return None

    out: dict = {
        "document_type": "Quality Disclaimer",
        "mission": f"Sentinel-{header.group('mission')}",
        "disclaimer_number": int(header.group("num")),
        "title": _section(full_text, "Title:", "Description:"),
        "description": _section(full_text, "Description:", "Degradation types:"),
        "degradation_percentage": _first(
            full_text, r"Degradation percentage\d*:\s*\n?\s*([0-9.,]+\s*%)"
        ),
        "degradation_types_selected": (checkboxes or {}).get("degradation_types"),
        "criteria": {
            "platform": (checkboxes or {}).get("platform"),
            "acquisition_mode": (checkboxes or {}).get("acquisition_mode"),
            "product_type": (checkboxes or {}).get("product_type"),
            "polarization": (checkboxes or {}).get("polarization"),
            "processing_facility": _first(full_text, r"Processing facility:\s*(.+)"),
            "ipf_version": _first(full_text, r"IPF version:\s*(.+)"),
            "instrument_configuration_id": _first(
                full_text, r"Instrument Configuration ID \(RDB\):\s*(.+)"
            ),
        },
        "period_of_issue": _parse_period(full_text),
        "cause": _section(full_text, "Cause:", "Status:"),
        "status": _section(full_text, "Status:", "References:"),
        "references": {
            "mpc_ref": _first(full_text, r"MPC ref:\s*(.+)"),
            "cams_ref": _first(full_text, r"CAMS ref:\s*(.+)"),
        },
    }

    # ADF files block: lines like "AUX_INS N/A"
    adf_block = _section(full_text, "ADF files:", "1 Percentage", "Period of the issue:")
    if adf_block:
        adf: dict[str, str] = {}
        for line in adf_block.splitlines():
            mm = re.match(r"(AUX_[A-Z0-9]+)\s+(.+)", line.strip())
            if mm:
                adf[mm.group(1)] = mm.group(2).strip()
        out["criteria"]["adf_files"] = adf or None

    # Impacted products
    products = []
    for line in full_text.splitlines():
        parsed = parse_sentinel1_product(line)
        if parsed:
            products.append(parsed)
    out["impacted_product_names"] = [p["name"] for p in products]
    out["impacted_products_count"] = len(products)
    if products:
        sar = [p for p in products if p.get("category") == "SAR"]
        summary = {
            "categories": sorted({p["category"] for p in products}),
            "missions": sorted({p["mission"] for p in products}),
            "product_types": sorted({p["product_type"] for p in products}),
        }
        if sar:
            summary.update(
                {
                    "modes": sorted({p["mode"] for p in sar}),
                    "polarizations": sorted({p["polarization"] for p in sar}),
                    "orbits": sorted({p["absolute_orbit"] for p in sar}),
                    "datatakes": sorted({p["datatake_id_hex"] for p in sar}),
                }
            )
        out["impacted_products_summary"] = summary
    return out


def _parse_period(full_text: str) -> dict | None:
    """Parse the 'Period of the issue' Start/Stop table."""
    block = _section(full_text, "Period of the issue:", "Cause:")
    if not block:
        return None
    period: dict[str, dict[str, str]] = {}
    row_keys = {
        "Acquisition date": "acquisition_date",
        "Generation date": "generation_date",
        "Orbit": "orbit",
        "Datatake (hex)": "datatake_hex",
    }
    for label, key in row_keys.items():
        m = re.search(rf"{re.escape(label)}\s+(\S+)\s+(\S+)", block)
        if m:
            period[key] = {"start": m.group(1), "stop": m.group(2)}
    return period or None


# --------------------------------------------------------------------------- #
# Collector entry point
# --------------------------------------------------------------------------- #
def extract_pdf(path: str | Path) -> dict:
    """Extract everything the collector needs from a single disclaimer PDF.

    Returns a dict with:
      - ``metadata``:   the PDF's own document metadata (incl. ISO ``ModDate``)
      - ``structured``: the parsed Quality Disclaimer fields, or a minimal
                        summary when the PDF is not a recognised disclaimer.

    Never raises on parsing problems: text extraction failure is the only hard
    error (missing backend / unreadable file); checkbox geometry is best-effort.
    """
    path = Path(path)

    texts = extract_text(path)
    full_text = "\n".join(texts)
    metadata = extract_metadata(path)

    try:
        checkboxes = extract_checkbox_selections(path)
    except Exception:  # geometry parsing is best-effort
        checkboxes = None

    structured = parse_quality_disclaimer(full_text, checkboxes)
    if structured is None:
        structured = {
            "document_type": "unknown",
            "page_count": len(texts),
            "character_count": len(full_text),
            "note": "Not recognized as a Quality Disclaimer; only text and "
            "metadata were extracted.",
        }

    return {"metadata": metadata, "structured": structured}
