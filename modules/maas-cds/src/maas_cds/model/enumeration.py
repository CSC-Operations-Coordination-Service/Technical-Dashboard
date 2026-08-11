"""Enumerations CDS model definition"""

import enum

__all__ = ["CompletenessStatus", "CompletenessScope", "DuplicatedDeletionStatus"]


class CompletenessStatus(enum.Enum):
    """

    Enumeration to describe completeness status of CdsDatatake
    """

    MISSING = "Missing"

    COMPLETE = "Complete"

    PARTIAL = "Partial"

    UNKNOWN = "Unknown"


class DuplicatedDeletionStatus(enum.Enum):
    """

    Enumeration to describe the removal of the duplicated products of a
    CdsDatatake on an interface (DD / LTA)

    It sits on the duplicated deletion funnel, each step being a subset of the
    previous one:

    - **identified**: the pair is identified by us as duplicated
    - **mentioned**: one of its products is present in a deletion (ticket and
      attachment consolidated on the product)
    - **deleted**: the interface probe reports that product as missing, so it is
      really gone
    """

    # the interface distributes no duplicated product type: nothing to delete
    NO_DUPLICATED = "No duplicated"

    # pairs are identified but none of them is mentioned in a deletion
    MISSING = "Missing"

    # deletions exist but the funnel is not complete: pairs still to be mentioned,
    # or mentioned pairs whose product is not (probed as) deleted yet
    CREATED = "Created"

    # every identified pair has its duplicate really deleted from the interface
    COMPLETE = "Complete"


class CompletenessScope(enum.Enum):
    """

    Enumeration to describe the scope for completeness
    """

    SLICE = "slice"

    LOCAL = "local"

    GLOBAL = "global"

    FINAL = "final"
