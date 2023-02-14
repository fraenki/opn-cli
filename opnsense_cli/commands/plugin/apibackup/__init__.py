import click

from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import formatter_from_formatter_name, available_formats
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.apibackup import Apibackup

pass_api_client = click.make_pass_decorator(ApiClient)
pass_apibackup_svc = click.make_pass_decorator(Apibackup)


@click.group()
def apibackup(**kwargs):
    """
    Manage api-backup
    """

@pass_apibackup_svc
def download(apibackup_svc: Apibackup, **kwargs):
    """
    Download config.xml from OPNsense.
    """
    result = apibackup_svc.download()
    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
