"""The completeness engines must load the dataflow configuration.

``CdsDatatake._dataflow_expected_interfaces`` reads ``MaasConfigDataflow`` from the
``MaasConfigManager`` cache to know which interfaces distribute each product type.
When it is not loaded the duplicated deletion reporting silently degrades: every
duplicated pair is then counted as expected on every interface.
"""

from unittest.mock import patch

from maas_cds.engines.compute.compute_completeness import ComputeCompletenessEngine
from maas_cds.engines.compute.compute_completeness_v2 import ComputeCompletenessEngineV2
from maas_cds.model.configuration import MaasConfigDataflow


def _loaded_config_names(mock_manager):
    """Configuration class names passed to the MaasConfigManager constructor."""
    names = []
    for call in mock_manager.call_args_list:
        configs = call.kwargs.get("config_model_class", [])
        if not isinstance(configs, list):
            configs = [configs]
        names.extend(type(config).__name__ for config in configs)
    return names


@patch("maas_cds.engines.compute.compute_completeness.MaasConfigManager")
def test_compute_completeness_engine_loads_dataflow(mock_manager):
    """The base engine loads the dataflow: without it the per-interface filtering
    of the duplicated pairs to be deleted is skipped."""

    ComputeCompletenessEngine()

    assert MaasConfigDataflow.__name__ in _loaded_config_names(mock_manager)


@patch("maas_cds.engines.compute.compute_completeness_v2.MaasConfigManager")
@patch("maas_cds.engines.compute.compute_completeness.MaasConfigManager")
def test_compute_completeness_engine_v2_loads_dataflow(mock_manager, mock_manager_v2):
    """V2 inherits the base load and adds its own configurations."""

    ComputeCompletenessEngineV2()

    loaded = _loaded_config_names(mock_manager) + _loaded_config_names(mock_manager_v2)
    assert MaasConfigDataflow.__name__ in loaded
