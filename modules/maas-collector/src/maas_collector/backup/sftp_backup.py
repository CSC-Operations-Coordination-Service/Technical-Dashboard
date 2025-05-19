from maas_collector.backup.backup import CollectorBackupConfiguration, CollectorBackup
import paramiko


class CollectorBackupSFTP(CollectorBackup):
    """store ingested files to an stfp server"""

    CONFIGURATION_CLASS = CollectorBackupConfiguration

    def __init__(self, args: CollectorBackupConfiguration):
        raise NotImplementedError()
        super().__init__(args)

        self.__transport: paramiko.Transport = None

        # a cache list of created directories to minimize sftp stat usage
        self._created_directories = []

    @property
    def transport(self):
        """property holding a lazy-created paramiko Transport"""

        if self.__transport is None or not self.__transport.is_active():

            self.logger.debug("Connecting to backup host %s", self.args.host)

            transport = paramiko.Transport((self.args.host, self.args.port))

            transport.connect(username=self.args.username, password=self.args.password)

            # send keep alive packet every 30 seconds
            transport.set_keepalive(30)

            self.__transport = transport

        return self.__transport

    def validate_backup_arguments(self):
        """Function used to make sure that all needed variables
        needed by the backup implementation have been provided

        Raises:
            ValueError: Raise if mandatory arguments needed for SFTP backup are missing
        """
        if (
            not self.args.host
            or not self.args.port
            or not self.args.username
            or not self.args.password
        ):
            raise ValueError(
                "The following arguments are mandatory for a SFTP Backup"
                " logic => (backup-hostname, backup-port, backup-username, backup-password)"
            )

    def makedirs(self, client: paramiko.SFTPClient, path: str):
        """create directory tree recursively

        Args:
            client (paramiko.SFTPClient): sftp client
            path (str): directory path
        """
        subdir = self.args.directory

        for subpath in path[len(self.args.directory) + 1 :].split("/"):

            subdir = "/".join([subdir, subpath])

            try:
                if subdir not in self._created_directories:
                    self.logger.debug("Checking if %s exists", subdir)
                    client.stat(subdir)

            except FileNotFoundError:
                self.logger.debug("Creating %s", subdir)
                client.mkdir(subdir)

            self._created_directories.append(subdir)

    def backup_file_implementation(self, config, path):
        """Copy file to backup space

        Args:
            config (CollectorConfiguration): ingestion config
            path (str): local file path on the pod working directory
        """

        try:
            # TODO may be retry n times
            with paramiko.SFTPClient.from_transport(self.transport) as client:

                target_dir, target_path = self.get_backup_path(config, path)

                self.logger.debug("Backuping %s to %s", path, target_path)

                if target_dir not in self._created_directories:

                    self.makedirs(client, target_dir)

                target = "/".join([target_dir, target_path])

                tmp_target = "/".join([target_dir, f".{target_path}"])

                self.logger.debug("Uploading %s to %s", path, tmp_target)

                client.put(path, tmp_target)

                self.logger.debug("Renaming %s to %s", tmp_target, target)

                client.posix_rename(tmp_target, target)

        except (paramiko.SSHException, IOError, OSError) as error:
            self.logger.critical("Cannot backup file %s to %s", path, self.args.host)
            self.logger.exception(error)
            # do not raise as logging critical is the only thing to do to not break
            # the ingestion loop

    def close(self):
        """close transport and clear directory creation cache"""
        if self.__transport:
            self.logger.debug("Closing backup sftp connection to %s", self.args.host)
            self.__transport.close()
            self.__transport = None

        self._created_directories.clear()
