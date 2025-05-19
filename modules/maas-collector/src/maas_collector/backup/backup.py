"""Ingested files backup"""

import dataclasses
import datetime
import gzip
import logging
import os
import shutil

from maas_collector.rawdata.collector.credentialmixin import CredentialMixin


@dataclasses.dataclass
class CollectorBackupConfiguration:
    """store backup parameters"""

    type: str = None

    directory: str = None

    calendar_tree: bool = False

    enable_gzip: bool = False

    interface_name: str = None

    interface_credentials: str = None


class CollectorBackup:
    """Main Collector Backup class which contains all
    methods common to all backup implementations.
    This class shall not be instanciated but inherited"""

    CONFIGURATION_CLASS = CollectorBackupConfiguration

    DO_NOT_COMPRESS_EXTENSION = (".xlsx", ".gzip", ".zip")

    def __init__(self, args: CollectorBackupConfiguration):
        self.args = args
        self.logger = logging.getLogger(self.__class__.__name__)
        self.validate_backup_arguments()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def close(self):
        """close transport and clear directory creation cache"""
        # Abstract Class
        raise NotImplementedError()

    def get_backup_path(
        self, config, path, dirdatetime: datetime.datetime = None
    ) -> tuple:
        """generate remote path"""

        path_elements = [self.args.directory]

        if self.args.calendar_tree:
            # DOI instead of ingestion time ?
            if dirdatetime is None:
                dirdatetime = datetime.datetime.utcnow()

            path_elements.extend(
                [
                    f"{dirdatetime.year:04d}",
                    f"{dirdatetime.month:02d}",
                    f"{dirdatetime.day:02d}",
                ]
            )

        if config.interface_name:
            path_elements.append(config.interface_name)
        elif config.model_name:
            # default: model class name. may be rabbit queue mmm ?
            path_elements.append(config.model_name)
        else:
            path_elements.append("Antoine")

        return "/".join(path_elements), os.path.basename(path)

    def backup_file(self, config, path):
        """Copy file to backup space

        Args:
            config (CollectorConfiguration): ingestion config
            path (str): local file path on the pod working directory
        """
        compression_enabled = self.args.enable_gzip
        for filetype in CollectorBackup.DO_NOT_COMPRESS_EXTENSION:
            if path.endswith(filetype):
                self.logger.debug(
                    "The following file %s will not be compressed before"
                    " being backed-up as its type '%s' in not suitable for compression",
                    path,
                    filetype,
                )
                compression_enabled = False
                break

        # handle compression.
        if compression_enabled:

            gzip_path = f"{path}.gz"

            self.logger.debug("Compressing %s to %s", path, gzip_path)

            with open(path, "rb") as f_in:

                with gzip.open(gzip_path, "wb") as f_out:

                    shutil.copyfileobj(f_in, f_out)

            path = gzip_path

        self.backup_file_implementation(config, path)

        # clean up compressed file
        if compression_enabled:
            os.remove(path)

    def backup_file_implementation(self, config, path):
        """This function which shall be redefined by the child class is responsible
           to perform the file backup operation to the remote server

        Args:
            config (CollectorConfiguration): ingestion config
            path (str): local file path on the pod working directory

        Raises:
            NotImplementedError: Raise in case the backup implementation
            function has not been defined in the instanciated child class
        """
        # Abstract Class
        raise NotImplementedError()

    def validate_backup_arguments(self):
        """Function used to make sure that all needed variables
        needed by the backup implementation have been provided
        """
        if not self.args.directory:
            raise ValueError(
                "The following arguments are mandatory for a Local Backup : directory"
            )
