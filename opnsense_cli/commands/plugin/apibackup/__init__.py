import click

from opnsense_cli.formatters.cli_output import CliOutputFormatter
from opnsense_cli.callbacks.click import formatter_from_formatter_name, available_formats
from opnsense_cli.api.client import ApiClient
from opnsense_cli.api.plugin.apibackup import Apibackup

pass_api_client = click.make_pass_decorator(ApiClient)
pass_apibackup_svc = click.make_pass_decorator(Apibackup)


@click.group()
@pass_api_client
@click.pass_context
def apibackup(ctx, api_client: ApiClient, **kwargs):
    """
    Manage api-backup
    """
    ctx.obj = Apibackup(api_client)


@apibackup.command()
@click.option(
    '--output', '-o',
    help=' Output format.',
    default="table",
    type=click.Choice(available_formats()),
    callback=formatter_from_formatter_name,
    show_default=True,
)
@click.option(
    '--cols', '-c',
    help='Which columns should be printed? Pass empty string (-c '') to show all columns',
    default="<ID>,name,supportedOptions",
    show_default=True,
)
@pass_apibackup_svc
def download(apibackup_svc: Apibackup, **kwargs):
    """
    Download config.xml from OPNsense.
    """
    print("DEBUG: hello world 1")
    result = apibackup_svc.download()
    print("DEBUG: hello world 2")
    CliOutputFormatter(result, kwargs['output'], kwargs['cols'].split(",")).echo()
