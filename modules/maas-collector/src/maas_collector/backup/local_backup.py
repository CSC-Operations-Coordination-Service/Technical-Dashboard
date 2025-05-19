import os
import shutil

from maas_collector.backup.backup import CollectorBackup


class CollectorBackupLocal(CollectorBackup):
    """Local implementation of the Collector Backup

    Args:
        CollectorBackup (CollectorBackup): Main Backup Collector Class
    """

    def close(self):
        "Nothing to close"
        pass

    def backup_file_implementation(self, config, path):

        try:
            local_file_path = "/".join(self.get_backup_path(config, path))
            parent_folder = os.path.dirname(local_file_path)

            # Create the parent folder if it doesn't exist
            os.makedirs(parent_folder, exist_ok=True)

            self.logger.debug(
                "A backup of %s will be created on %s, its remote path will be %s",
                path,
                self.args.directory,
                local_file_path,
            )
            shutil.copy2(path, local_file_path)

        except IOError as error:

            self.logger.critical(
                "Cannot backup file %s to %s on localfilesystem %s due to the following error: %s",
                path,
                self.args.interface_name,
                self.args.directory,
                error,
            )
