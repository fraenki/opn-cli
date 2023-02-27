#from opnsense_cli.api.plugin.apibackup import Apibackup
from opnsense_cli.api.plugin.apibackup import Backup
from opnsense_cli.facades.commands.plugin.apibackup.base import ApibackupFacade

class ApibackupBackupFacade(ApibackupFacade):
    #def __init__(self, backup_api: Apibackup):
    def __init__(self, backup_api: Backup):
        self._backup_api = backup_api

    # XXX function name?
    def download_backup(self, path):
        config = self._backup_api.download('json')
        # XXX maybe rename the function to "_file", because there is really
        # no "zip" magic anywhere...
        self._write_base64_string_to_zipfile(path, config['content'])
        return {
            "status": f"sucessfully saved to: {path}"
        }
