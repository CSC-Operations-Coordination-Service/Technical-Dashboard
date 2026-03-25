from maas_cds.lib.parsing_name.utils import (
    normalize_product_name_list,
    remove_extension_from_product_name,
)


def test_iterator():

    product_name = (
        "S1C_IW_RAW__0NDV_20251016T203726_20251016T204002_004592_009148_E271.SAFE.zip"
    )

    product_names = normalize_product_name_list([product_name])

    assert product_names == [product_name]

    product_name_without_ext = remove_extension_from_product_name(product_name)

    assert (
        product_name_without_ext
        == "S1C_IW_RAW__0NDV_20251016T203726_20251016T204002_004592_009148_E271"
    )
