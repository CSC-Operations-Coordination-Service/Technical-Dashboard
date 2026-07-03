import datetime

from collections import namedtuple
from typing import List

Period = namedtuple("Period", ("start", "end"))

# A product candidate for duplicated items detection. Unlike ``Period`` it keeps
# the product identity (``name``) and its deletion trace so a duplicated pair can
# be traced back to the actual products (e.g. to know which one is targeted for
# deletion). Only ``start`` / ``end`` are used by the completeness computations,
# so a ``DuplicationCandidate`` can be used wherever a ``Period`` is expected.
DuplicationCandidate = namedtuple(
    "DuplicationCandidate",
    (
        "name",
        "start",
        "end",
        "to_be_deleted",
        "deletion_issue",
        # Per-interface deletion trace (see CdsProduct.deletion_trace_by_interface),
        # used to split the duplicated items reporting by DD / LTA.
        "dd_deleted",
        "dd_issue",
        "lta_deleted",
        "lta_issue",
    ),
    defaults=(False, None, False, None, False, None),
)


def compute_total_sensing_product(periods: list[Period]) -> int:
    """Compute total sensing period

    Note: periods must be sort

    """

    sensing = 0
    last_period = None

    for period in periods:

        if last_period is None or period.start >= last_period.end:
            sensing += (period.end - period.start).total_seconds() * 1000000
        elif period.start < last_period.end and last_period.end < period.end:
            sensing += (period.end - last_period.end).total_seconds() * 1000000

        last_period = period

    return sensing


def compute_total_sensing_period(periods: list[Period]) -> Period:
    """Compute sensing period covered by products"""

    total_period = None

    for period in periods:
        if total_period is None:
            total_period = Period(period.start, period.end)
        else:
            minstart = min(total_period.start, period.start)
            maxend = max(total_period.end, period.end)
            total_period = Period(minstart, maxend)

    return total_period


def reduce_periods(
    periods: List[Period],
    tolerance_value=datetime.timedelta(seconds=15),
) -> List[Period]:
    """Reduce a list of period"""

    # periods.sort(key=lambda p: (p.start, p.end))  # sort by start date
    periods.sort(key=lambda p: p.start)  # sort by start date

    reduced = []

    for period in periods:

        adjusted_period = Period(
            period.start - tolerance_value, period.end + tolerance_value
        )

        if not reduced:
            reduced.append(adjusted_period)

        elif adjusted_period.start <= reduced[-1].end:
            reduced[-1] = Period(
                reduced[-1].start, max(reduced[-1].end, adjusted_period.end)
            )
        else:
            reduced.append(adjusted_period)

    return reduced


def compute_missing_sensing_periods(
    range_to_evaluate: Period,
    periods: List[Period],
    maximal_offset,
    tolerance_value=0,
) -> List[Period]:
    """Identify missing products within sensing period"""

    period_start = range_to_evaluate.start
    period_stop = range_to_evaluate.end

    if not periods:
        # No coverage at all, return the whole period
        return [Period(period_start, period_stop)]

    period_stop += datetime.timedelta(microseconds=tolerance_value)

    previous = None
    missing_periods = []

    start_offset = (periods[0].start - period_start).total_seconds() * 1000000

    # Missing period at start
    if start_offset > maximal_offset:
        # Fake product ending at the begin of the datatake
        previous = Period(period_start, period_start)

    else:
        # move end date cursor
        period_stop += datetime.timedelta(microseconds=start_offset)

    for brother in periods:
        if previous and brother.start > previous.end:
            # Missing period between products
            missing_periods.append(Period(previous.end, brother.start))
        previous = brother

    end_offset = (period_stop - periods[-1].end).total_seconds()

    if end_offset > 0:
        # Missing period at stop
        missing_periods.append(
            Period(
                periods[-1].end,
                period_stop,
            )
        )

    return missing_periods


def compute_missing_sensing_periods(
    range_to_evaluate: Period,
    periods: List[Period],
    maximal_offset,
    tolerance_value=0,
) -> List[Period]:
    """Identify missing products within sensing period"""

    period_start = range_to_evaluate.start
    period_stop = range_to_evaluate.end

    if not periods:
        # No coverage at all, return the whole period
        return [Period(period_start, period_stop)]

    period_stop += datetime.timedelta(microseconds=tolerance_value)

    previous = None
    missing_periods = []

    start_offset = (periods[0].start - period_start).total_seconds() * 1000000

    # Missing period at start
    if start_offset > maximal_offset:
        # Fake product ending at the begin of the datatake
        previous = Period(period_start, period_start)

    else:
        # move end date cursor
        period_stop += datetime.timedelta(microseconds=start_offset)

    for brother in periods:
        if previous and brother.start > previous.end:
            # Missing period between products
            missing_periods.append(Period(previous.end, brother.start))
        previous = brother

    end_offset = (period_stop - periods[-1].end).total_seconds()

    if end_offset > 0:
        # Missing period at stop
        missing_periods.append(
            Period(
                periods[-1].end,
                period_stop,
            )
        )

    return missing_periods


def compute_duplicated_indicator(
    periods: List[Period],
) -> List[Period]:
    """Identify missing products within sensing period"""

    duplicated_indicator = {
        "min_percentage": 0.0,
        "avg_percentage": 0.0,
        "max_percentage": 0.0,
        "min_duration": 0,
        "avg_duration": 0,
        "max_duration": 0,
    }

    duplicated_percentage = []
    duplicated_duration = []

    if len(periods) < 2:
        # No coverage at all, return the whole period
        return duplicated_indicator

    for previous, brother in zip(periods[:-1], periods[1:]):

        if brother.start < previous.end:
            common_time = (
                min(previous.end, brother.end) - brother.start
            ).total_seconds() * 1000
            duplicated_duration.append(common_time)

            total_period = (previous.end - previous.start).total_seconds() * 1000

            common_percentage = common_time / total_period * 100
            duplicated_percentage.append(common_percentage)
        else:
            duplicated_duration.append(0)
            duplicated_percentage.append(0)

    duplicated_indicator = {
        "min_percentage": float(min(duplicated_percentage)),
        "avg_percentage": float(
            sum(duplicated_percentage) / len(duplicated_percentage)
        ),
        "max_percentage": float(max(duplicated_percentage)),
        "min_duration": int(min(duplicated_duration)),
        "avg_duration": int(sum(duplicated_duration) / len(duplicated_duration)),
        "max_duration": int(max(duplicated_duration)),
    }

    return duplicated_indicator


def compute_overlap_percentage(previous: Period, brother: Period) -> float:
    """Compute the overlap percentage of two periods.

    The percentage is expressed relative to the duration of ``previous``
    (same convention as :func:`compute_duplicated_indicator`).

    Returns 0.0 when the periods do not overlap or when ``previous`` has a null
    duration.
    """

    if brother.start >= previous.end:
        return 0.0

    common_time = (min(previous.end, brother.end) - brother.start).total_seconds()
    total_period = (previous.end - previous.start).total_seconds()

    if total_period <= 0:
        return 0.0

    return common_time / total_period * 100


def compute_duplicated_items(
    candidates: List[DuplicationCandidate],
    threshold: float = 30.0,
) -> List[dict]:
    """Identify duplicated products among a list of candidates.

    Two *consecutive* products (sorted by sensing start date) whose overlap
    percentage is greater than or equal to ``threshold`` are considered as
    duplicated of each other. Every such consecutive pair is returned (each
    element is compared only with the next one).

    Args:
        candidates (List[DuplicationCandidate]): the products to evaluate, each
            carrying its ``name`` and sensing period. Must be sorted by start.
        threshold (float): minimal overlap percentage to flag a pair.

    Returns:
        List[dict]: one entry per duplicated *pair* (not per member), with keys
            ``name`` and ``paired_with`` (the two products), ``sensing_start_date``,
            ``sensing_end_date``, ``duplicated_percentage`` and ``deleted_product``
            (``{"DD": name|None, "LTA": name|None}`` naming the pair member deleted
            from each interface). A product involved in several consecutive overlaps
            yields one pair entry per overlap.
    """

    duplicated_items = []

    if len(candidates) < 2:
        return duplicated_items

    def _deleted_product(first, second):
        """Name the member of the pair deleted from each interface (or None)."""
        deleted_product = {"DD": None, "LTA": None}
        for candidate in (first, second):
            if candidate.dd_deleted:
                deleted_product["DD"] = candidate.name
            if candidate.lta_deleted:
                deleted_product["LTA"] = candidate.name
        return deleted_product

    def _item(candidate, paired_with, percentage, deleted_product):
        return {
            "name": candidate.name,
            "sensing_start_date": candidate.start,
            "sensing_end_date": candidate.end,
            "duplicated_percentage": float(percentage),
            "paired_with": paired_with.name,
            "deleted_product": dict(deleted_product),
        }

    for previous, brother in zip(candidates[:-1], candidates[1:]):

        percentage = compute_overlap_percentage(
            Period(previous.start, previous.end),
            Period(brother.start, brother.end),
        )

        if percentage >= threshold:
            deleted_product = _deleted_product(previous, brother)
            duplicated_items.append(
                _item(previous, brother, percentage, deleted_product)
            )

    return duplicated_items
