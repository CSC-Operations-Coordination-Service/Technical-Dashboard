"""Custom CDS model definition for product deletion"""

from maas_model import ZuluDate

from maas_cds.model import generated


__all__ = ["ProductDeletion", "CdsInterfaceProductDeletion"]


class CdsInterfaceProductDeletion(generated.CdsInterfaceProductDeletion):
    """
    CdsInterfaceProductDeletion override because ingestionTime is excluded from
    generation
    """

    ingestionTime = ZuluDate()


class ProductDeletion(generated.ProductDeletion):
    """ProductDeletion custom"""

    @property
    def jira_issue(self) -> str:
        """Get the issue name contained in the report name

        Returns:
            str: The issue name
        """
        return self.reportName.split("_")[0]
