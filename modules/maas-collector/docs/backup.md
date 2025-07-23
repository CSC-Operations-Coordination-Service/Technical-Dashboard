# Backup

WIP: There is some TODO here

There is currently the follwoing backup type:

## Usage

```json
{
    "other_collector_config": "...",
    "backup": {
        "Here_the_backup_conf": "..."
    },
}
```

## FileSystem

```json
{
    "...": "...",
    "backup": {
        "type": "BackupLocal",
        "directory": "/tmp/backup"
    },
    "..": "..",
}
```

## S3

```json
{
    "...": "...",
    "backup": {
        "type": "BackupS3",
        "TODO": "TODO"
    },
    "..": "..",
}
```

## SFTP

```json
{
    "...": "...",
    "backup": {
        "type": "BackupSFTP",
        "TODO": "TODO"
    },
    "..": "..",
}
```

## Improvments

- Support multiple backups strategy

```json
{
    "...": "...",
    "backup": [
        {
            "type": "BackupLocal",
            "directory": "/tmp/backup_on_system_a"
        }, 
        {
            "type": "BackupLocal",
            "directory": "/tmp/backup_on_system_b"
        }
    ],
    "..": "..",
}
```

- Support Mail backup

```json
{
    "...": "...",
    "backup": {
        "type": "BackupMail",
        "email_adress": ["maas@local", "backup@local"],
        "server_adress": "...",
        "...": "..."
    }
}
```

- Add notificiation on backup
