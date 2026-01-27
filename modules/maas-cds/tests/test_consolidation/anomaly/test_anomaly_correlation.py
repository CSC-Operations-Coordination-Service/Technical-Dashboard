from maas_cds.engines.reports.cams_anomaly_correlation import (
    AnomalyCorrelationConsolidatorEngine,
)


def test_kindly_input_corrector():
    impacted_observations = [
        "S1A-516379",
        "S1A-516379",
        "S1A-516380S1A-516381",
        "S1A-516382.S1A-516383",
        "S1A-516384;S1A-516385",
        "\r\nS1A-516441",
        "S1A--516386",
        "\tS1A-516576",
        " S1A-516757",
    ]

    corrected_dt_ids = set()
    for impacted_observation in impacted_observations:
        patched_dt = AnomalyCorrelationConsolidatorEngine.kindly_input_corrector(
            impacted_observation
        )
        for corrected_dt in patched_dt:
            corrected_dt_ids.add(corrected_dt)

    assert sorted(list(corrected_dt_ids)) == sorted(
        [
            "S1A-516441",
            "S1A-516379",
            "S1A-516380",
            "S1A-516381",
            "S1A-516382",
            "S1A-516383",
            "S1A-516384",
            "S1A-516385",
            "S1A-516386",
            "S1A-516576",
            "S1A-516757",
        ]
    )
