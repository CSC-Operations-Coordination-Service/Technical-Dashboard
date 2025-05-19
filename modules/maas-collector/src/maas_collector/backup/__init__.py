from .s3_backup import CollectorBackupS3
from .sftp_backup import CollectorBackupSFTP
from .local_backup import CollectorBackupLocal


factory_type_dict = {
    "BackupS3": CollectorBackupS3,
    "BackupLocal": CollectorBackupLocal,
    "BackupSFTP": CollectorBackupSFTP,
}


def instanciate_collector_backup(args: CollectorBackupLocal):

    if args["type"] not in factory_type_dict:
        raise ValueError("Unknow type of backup %s", args["type"])

    backup_class = factory_type_dict.get(args["type"])

    backup_configuration_class = backup_class.CONFIGURATION_CLASS

    return backup_class(backup_configuration_class(**args))
