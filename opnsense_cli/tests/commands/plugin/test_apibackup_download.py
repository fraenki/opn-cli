from unittest.mock import patch
from opnsense_cli.commands.core.openvpn import openvpn
from opnsense_cli.tests.commands.base import CommandTestCase

class TestApibackupCommands(CommandTestCase):
    def setUp(self):
        self._api_data_fixtures_download = {
            "result": "ok",
            "changed": "false",
            "filename": "OpenVPN_Server_vpnuser1.ovpn",
            "filetype": "text/plain",
            "content": "T3BlblZQTiBjZXJ0aWZpY2F0ZQo="
        }
        self._api_client_args_fixtures = [
            'api_key',
            'api_secret',
            'https://127.0.0.1/api',
            True,
            '~/.opn-cli/ca.pem',
            60
        ]

    @patch('opnsense_cli.commands.core.apibackup.ApiClient.execute')
    def test_download(self, api_response_mock):
        result = self._opn_cli_command_result(
            api_response_mock,
            [
                self._api_data_fixtures_download,
            ],
            apibackup,
            ['download', '2', '57194c007be18', '-o', 'plain']
        )

        self.assertIn(
            "OpenVPN_Server_vpnuser1.ovpn T3BlblZQTiBjZXJ0aWZpY2F0ZQo=\n",
            result.output
        )
