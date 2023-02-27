from opnsense_cli.api.plugin.apibackup import Backup
from opnsense_cli.facades.commands.plugin.apibackup.base import ApibackupFacade

class ApibackupBackupFacade(ApibackupFacade):
    def __init__(self, backup_api: Backup):
        self._backup_api = backup_api

    def download_backup(self, path):
        config = self._backup_api.download('json')
        self._write_base64_string_to_zipfile(path, config['content'])
        return {
            "status": f"sucessfully saved to: {path}"
        }
