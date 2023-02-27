from opnsense_cli.api.base import ApiBase


#class Apibackup(ApiBase):
class Backup(ApiBase):
    MODULE = "backup"
    CONTROLLER = "backup"
    """
    api-backup BackupController
    """

    @ApiBase._api_call
    #def download(self, *args, json=None):
    def download(self, *args):
        self.method = "get"
        self.command = "download"
