from opnsense_cli.exceptions.command import CommandException
from opnsense_cli.facades.commands.base import CommandFacade

class ApibackupFacade(CommandFacade):
    def __init__(self):
        super().__init__()
