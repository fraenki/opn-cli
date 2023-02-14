from opnsense_cli.api.base import ApiBase


class Apibackup(ApiBase):
    MODULE = "apibackup"
    CONTROLLER = "backup"
    """
    api-backup BackupController
    """

    @ApiBase._api_call
    def download(self, *args, json=None):
        self.method = "get"
        self.command = "download"
