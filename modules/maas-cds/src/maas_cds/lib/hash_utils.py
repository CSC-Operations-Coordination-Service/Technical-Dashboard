import hashlib
from typing import Any, List


def get_hash(fields: List[str], input_document: Any):
    """Calculate an hash using the value of different field in an input document

    Args:
        fields (List[str]): field name to use for hash calculation
        input_document (Any): input document containing the fields
    Raises:
        ValueError: triggered when field used to calculate
        hash are missing from document

    Returns:
        str: calculated hash
    """
    md5 = hashlib.md5()
    for name in fields:
        try:
            md5.update(str(input_document[name]).encode())
        except KeyError as error:
            raise ValueError(
                f"Field {name} is missing from {input_document}"
            ) from error
    return md5.hexdigest()
