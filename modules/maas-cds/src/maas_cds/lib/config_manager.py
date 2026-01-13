import logging


class MaasConfigManager:
    """Util class to have a commun solution to handle configuration

    Oppportunity handle some time to live of the config to allow hot refresh of this one

    Some specific method can be add on MaasConfig for default usage
    """

    _instance = None

    CACHE = {}

    def __new__(cls, config_model_class=None):

        if cls._instance is None:
            cls._instance = super(MaasConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_model_class=None):

        self.logger = logging.getLogger(self.__class__.__name__)

        from maas_cds.model.configuration import MaasConfig

        # Just to have a local reference of the class
        if config_model_class is None:
            return None

        self.logger.info("Init with %s", config_model_class)
        if isinstance(config_model_class, MaasConfig):
            self.logger.info("This is a MaasConfig")
            configs_to_load = [config_model_class]

        elif isinstance(config_model_class, list):
            if not all(isinstance(config, MaasConfig) for config in config_model_class):
                raise TypeError("List contains non-MaasConfig sub class")
            configs_to_load = config_model_class
        else:
            raise TypeError(
                f"Unexpected type for consolidated_doc: {type(config_model_class)}"
            )

        self.logger.info(
            "Attempts to load %s configuration : %s",
            len(configs_to_load),
            configs_to_load,
        )
        for config_to_load in configs_to_load:
            self.load_config(config_to_load)

    def load_config(self, model_class):
        # ! Over 1000 elements need to think about a different way

        # ? It would be good here to handle also some commun pattern ie :
        # - use latest
        # - use the current one
        # - set a expiration date

        if model_class.__class__.__name__ in self.CACHE:
            self.logger.info(
                "Configuration %s already loaded", model_class.__class__.__name__
            )

        else:
            self.logger.info("Loading %s configuration", model_class.__class__.__name__)

            # Here the loaded function should be handle by the class themself
            document_config = model_class.load()

            # Name is like MaasConfigCompleteness
            self.CACHE[model_class.__class__.__name__] = document_config

    def get_config(self, model_class_name):
        # Can be improve and load if missing, but we still need to take care of a proper usage
        if model_class_name not in self.CACHE:
            self.logger.info(
                "Attempts to get an unload %s configuration",
                model_class_name,
            )
            return None

        return self.CACHE[model_class_name]
