from server.ice_servers.coturn import CoturnHMAC
from tests.conftest import coturn_hosts,coturn_credentials
from unittest import mock
import pytest

@pytest.fixture
def coturn_hmac(coturn_hosts, coturn_keys):
    return CoturnHMAC(coturn_hosts=coturn_hosts, coturn_keys=coturn_keys)


@mock.patch('time.time', mock.MagicMock(return_value=1000))
def test_coturn_tokens(coturn_hmac, coturn_hosts, coturn_credentials):
    servers = coturn_hmac.server_tokens(username='faf-test', ttl=123456)
    comparison_list = []
    for coturn_host,coturn_cred in zip(coturn_hosts, coturn_credentials):
        comparison_list.append(
            dict(host=coturn_host, cred=coturn_cred)
        )

    for i in range(0, len(servers)):
        server = servers[i]
        host = comparison_list[i]['host']
        credential = comparison_list[i]['cred']
        assert(server['credentialType'] == 'token')
        assert(server['urls'] ==
                [
                    f"turn:{host}?transport=tcp",
                    f"turn:{host}?transport=udp",
                    f"stun:{host}"
                ]
        )
        assert(server['credential'] == credential)
        assert(server['username'] == '124456:faf-test')

