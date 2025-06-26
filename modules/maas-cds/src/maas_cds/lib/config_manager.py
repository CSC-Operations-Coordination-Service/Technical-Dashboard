from maas_cds.model import MaasConfig


class MaasConfigManager:
    """Util class to have a commun solution to handle configuration

    Oppportunity handle some time to live of the config to allow hot refresh of this one

    Some specific method can be add on MaasConfig for default usage
    """

    CACHE = {}

    def __init__(self, config_model_class):

        if (config_model_class, MaasConfig):
            configs_to_load = [config_model_class]
        elif isinstance(config_model_class, list):
            if not all(issubclass(doc, MaasConfig) for doc in config_model_class):
                raise TypeError("List contains non-MAASDocument elements")
            configs_to_load = config_model_class
        else:
            raise TypeError(
                f"Unexpected type for consolidated_doc: {type(config_model_class)}"
            )

        for config_to_load in configs_to_load:
            self.load_config(config_to_load)

    def load_config(self, model_class):
        # Over 1000 need to think about a different way
        document_config = (
            model_class.search()
            .params(
                size=1000,
            )
            .execute()
        )

        self.CACHE[model_class.__class__.__name__] = document_config

    def get_config(self, model_class_name):

        return self.CACHE[model_class_name]
