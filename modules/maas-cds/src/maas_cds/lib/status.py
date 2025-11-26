from maas_cds.model.enumeration import CompletenessStatus


def evaluate_completeness_status(value):
    """Compute completeness status"""
    value_completeness_status = None
    if value == 0:
        value_completeness_status = CompletenessStatus.MISSING.value
    elif value >= 100:
        value_completeness_status = CompletenessStatus.COMPLETE.value
    else:
        value_completeness_status = CompletenessStatus.PARTIAL.value
    return value_completeness_status
