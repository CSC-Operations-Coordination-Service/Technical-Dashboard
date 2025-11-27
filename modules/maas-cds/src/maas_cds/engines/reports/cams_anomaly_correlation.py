"""AN consolidation"""

import datetime
import re
from maas_engine.engine.replicate import ReplicatorEngine
from maas_cds.model import CdsAnomalyCorrelation, CamsCloudAnomalyCorrelation
from typing import Union
from maas_cds.lib.parsing_name.utils import (
    normalize_product_name_list,
    generate_publication_names,
)


class AnomalyCorrelationConsolidatorEngine(ReplicatorEngine):
    """Consolidate Anomaly Correlation"""

    ENGINE_ID = "CONSOLIDATE_ANOMALY_CORRELATION"

    CONSOLIDATED_MODEL = CdsAnomalyCorrelation

    def __init__(
        self,
        args=None,
        send_reports=False,
        min_doi=None,
        target_model="CdsAnomalyCorrelation",
        exclude_fields=None,
        include_fields=None,
    ):
        # Add some default configuration for this replciator engine
        # if include_fields is None:
        #     include_fields = []
        if exclude_fields is None:
            exclude_fields = [
                "reportName",
                "interface_name",
                "reportFolder",
                "impacted_passes",
                "impacted_observations",
            ]
        super().__init__(
            args,
            target_model=target_model,
            include_fields=include_fields,
            exclude_fields=exclude_fields,
            send_reports=send_reports,
            min_doi=min_doi,
        )

    def get_consolidated_id(self, raw_document: CamsCloudAnomalyCorrelation):
        return raw_document.meta.id

    def consolidate(
        self, raw_document: CamsCloudAnomalyCorrelation, document: CdsAnomalyCorrelation
    ) -> Union[CdsAnomalyCorrelation]:
        """consolidate metrics data

        Args:
            raw_document (CamsCloudAnomalyCorrelation): raw CamsCloudAnomalyCorrelation extracted from metrics api
            document (CdsAnomalyCorrelation): consolidated data

        Returns:
            CdsAnomalyCorrelation: consolided data
        """
        document = super().consolidate(raw_document, document)

        document.errors = []

        document.products = normalize_product_name_list(raw_document.products)

        document.publications = [
            publication_name
            for product_name in document.products
            for publication_name in generate_publication_names(product_name)
        ]

        document.datatake_ids = (
            list(
                set(
                    [
                        re.sub(r"\s+", "", impacted_observation)
                        for impacted_observation in raw_document.impacted_observations
                        if impacted_observation
                        and re.sub(r"\s+", "", impacted_observation)
                    ]
                )
            )
            if raw_document.impacted_observations
            else []
        )

        if raw_document.impacted_passes:
            acquisition_pass_keys = []

            if not raw_document.station or not raw_document.station_type:
                # In the future: raise a MaasError to have a common way to identify issues

                missing_fields = []
                if not raw_document.station:
                    missing_fields.append("station")
                if not raw_document.station_type:
                    missing_fields.append("station_type")

                missing_fields_str = ", ".join(missing_fields)

                self.logger.warning(
                    "Missing required field(s) [%s] in anomaly raw_document %s",
                    missing_fields_str,
                    raw_document.key,
                )

                document.errors.append(
                    f"Acquisition Passes Missing required field(s): {missing_fields_str}"
                )

            else:
                # Whitelist station
                edrs_station = ["HDGS", "RDGS", "BFLGS", "FLGS"]
                gs_station = ["SGS", "MTI", "INS", "NSG", "MPS", "KSE", "PAR"]
                allowed_station = edrs_station + gs_station

                impacted_stations = [
                    st for st in allowed_station if st in raw_document.station
                ]

                # Impacted pass must contains satellite like S1A-orbit
                for impacted_passe in raw_document.impacted_passes:
                    if not impacted_passe:
                        continue
                    # 🍭 Sugar stuff to help mission specialist

                    # Handle cases where impacted_passe contains multiple passes concatenated (e.g., SXX-XXXXYSXX-XXXX)
                    # Also match patterns like S1C-L20250714102850293000224 or SXX-LXXXXX
                    multi_pass_matches = re.findall(
                        r"(S\d{1}[a-zA-Z]{1}-L\d+|S\d{1}[a-zA-Z]{1}-\d+|SXX-L\w+)",
                        impacted_passe,
                    )

                    if multi_pass_matches and len(multi_pass_matches) >= 1:
                        for single_pass in multi_pass_matches:

                            try:
                                satellite, orbit = single_pass.split("-")
                            except ValueError:
                                self.logger.warning(
                                    "[%s] - Wrong format of single passes type provided in anomaly raw_document : %s | expected SXX-orbit",
                                    raw_document.key,
                                    single_pass,
                                )
                                document.errors.append(
                                    f"Impacted Passes Wrong format data from: {single_pass} expected SXY-orbit"
                                )
                                continue

                            for station in impacted_stations:

                                acquisition_pass_keys.append(
                                    "_".join(
                                        [
                                            satellite,
                                            raw_document.station_type,
                                            orbit,
                                            station,
                                        ]
                                    )
                                )
                    else:
                        self.logger.warning(
                            "[%s] - Wrong format of passes type provided in anomaly raw_document : %s | expected SXX-orbit",
                            raw_document.key,
                            impacted_passe,
                        )
                        document.errors.append(
                            f"Impacted Passes Wrong format data from: {impacted_passe} expected SXY-orbit"
                        )
                        continue
                # Since the 21/06/2024 we supporte only orbit that are prefix by satellite unit to avoid collision in the futur
                # Keep it to be retroactive
                if raw_document.created < datetime.datetime(
                    2024, 7, 1, tzinfo=datetime.UTC
                ):
                    satellite_list = raw_document.sattelite_unit
                    if isinstance(raw_document.sattelite_unit, str):
                        satellite_list = [raw_document.sattelite_unit]
                    for satellite in satellite_list:
                        for impacted_passe in raw_document.impacted_passes:
                            if impacted_passe.startswith("S"):
                                continue
                            acquisition_pass_keys.append(
                                "_".join(
                                    [
                                        satellite,
                                        raw_document.station_type,
                                        impacted_passe,
                                        raw_document.station,
                                    ]
                                )
                            )

            # remove duplicated
            document.acquisition_pass = list(
                dict.fromkeys(acquisition_pass_keys).keys()
            )

        else:
            document.acquisition_pass = []

        # Next is the way to extract the issue from the AN ticket
        issue_id = None

        # Try to extract the GSANOM id from the title
        match = re.search(r"(GSANOM-\d+)", raw_document.title)
        if match:
            issue_id = match.group(1)
            self.logger.debug(
                "[%s] - GSANOM id found in title: %s", document.key, issue_id
            )
        else:
            # Try to find the first issue starting with GSANOM
            gsanom_issue = next(
                (i for i in raw_document.issue if i.startswith("GSANOM")), None
            )
            if gsanom_issue:
                issue_id = gsanom_issue
                self.logger.debug(
                    "[%s] - GSANOM id found in issue linked: %s", document.key, issue_id
                )
            else:
                document.errors.append(f"Not able to find the associated GSANOM")
                self.logger.warning(
                    "[%s] - No GSANOM id found in title or issues", document.key
                )

        document.ticket_id = issue_id

        return document
