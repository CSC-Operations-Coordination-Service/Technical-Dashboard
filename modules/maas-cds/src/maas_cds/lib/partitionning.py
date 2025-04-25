from datetime import timedelta


def get_partionning(
    start_date,
    stop_date,
    day_precision: int = 0,
) -> list[str]:
    """Get the partitionning of the datatake

    Args:
        start_date (str): start time of the period
        stop_date (str): stop time of the period
        day_precision (int): number of days to consider for partitionning

    Returns:
        list[str]: list of months in YYYY-MM format
    """

    # TODO (Improvement) use dynamic format - currently in month

    date_set = set()

    current_date = start_date - timedelta(days=day_precision)
    target_end_date = stop_date + timedelta(days=day_precision)

    while current_date < target_end_date:
        date_set.add(current_date.strftime("%Y-%m"))
        # Increment by one month
        if current_date.month == 12:
            current_date = current_date.replace(
                year=current_date.year + 1, month=1, day=1
            )
        else:
            new_month = current_date.month + 1
            current_date = current_date.replace(month=new_month, day=1)
    date_set.add(target_end_date.strftime("%Y-%m"))

    return sorted(date_set)
