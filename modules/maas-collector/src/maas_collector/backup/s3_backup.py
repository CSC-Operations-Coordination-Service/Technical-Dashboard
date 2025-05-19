import dataclasses
from typing import List
import boto3
import botocore
from maas_collector.backup.backup import CollectorBackupConfiguration, CollectorBackup
from botocore.client import Config


@dataclasses.dataclass
class CollectorBackupS3Configuration(CollectorBackupConfiguration):

    s3_endpoint_url: str = None

    s3_secret_key: str = None

    s3_access_key: str = None

    s3_signature_version: str = None

    s3_region: str = None

    buckets: List[str] = dataclasses.field(default_factory=lambda: [])


class CollectorBackupS3(CollectorBackup):
    """S3 implementation of the Collector Backup

    Args:
        CollectorBackup (CollectorBackup): Main Backup Collector Class
    """

    CONFIGURATION_CLASS = CollectorBackupS3Configuration

    def __init__(self, args: CollectorBackupS3Configuration):

        super().__init__(args)

        self.buckets = args.buckets

        self.s3_client = boto3.client(
            service_name="s3",
            endpoint_url=self.args.s3_endpoint_url,
            aws_access_key_id=self.args.s3_access_key,
            aws_secret_access_key=self.args.s3_secret_key,
            config=Config(signature_version=self.args.s3_signature_version),
            region_name=self.args.s3_region,
        )

    def __enter__(self):

        return self.s3_client

    def __exit__(self, exc_type, exc_value, traceback):
        if self.s3_client:
            self.s3_client.close()

    def validate_backup_arguments(self):
        return super().validate_backup_arguments()

    def close(self):
        # No action needed with S3 when transfert is over
        pass

    def backup_file_implementation(self, config, path):

        for bucket in self.buckets:

            try:
                remote_file_path = "/".join(self.get_backup_path(config, path))

                self.logger.debug(
                    "A backup of %s will be created on %s, its remote path will be %s",
                    path,
                    bucket,
                    remote_file_path,
                )

                self.s3_client.upload_file(path, bucket, remote_file_path)
            except (
                botocore.exceptions.BotoCoreError,
                botocore.exceptions.ClientError,
                boto3.exceptions.Boto3Error,
            ) as error:

                self.logger.critical(
                    "Cannot backup file %s to %s on bucket %s due to the following error: %s",
                    path,
                    self.args.interface_name,
                    bucket,
                    error,
                )
