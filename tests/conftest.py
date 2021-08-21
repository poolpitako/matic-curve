import pytest
from brownie import config, Wei, Contract, chain


@pytest.fixture
def gov(accounts):
    yield accounts[0]


@pytest.fixture
def rewards(accounts):
    yield accounts[1]


@pytest.fixture
def guardian(accounts):
    yield accounts[2]


@pytest.fixture
def management(accounts):
    yield accounts[3]


@pytest.fixture
def strategist(accounts):
    yield accounts[4]


@pytest.fixture
def keeper(accounts):
    yield accounts[5]


@pytest.fixture
def token():
    token_address = "0xE7a24EF0C5e95Ffb0f6684b813A78F2a3AD7D171"  # this should be the address of the ERC-20 used by the strategy/vault
    yield Contract(token_address)


@pytest.fixture
def amount(token):
    amount = 100 * 10 ** token.decimals()
    # In order to get some funds for the token you are about to use,
    # it impersonate an exchange address to use it's funds.
    yield amount


@pytest.fixture
def vault(pm, gov, rewards, guardian, management, token):
    Vault = pm(config["dependencies"][0]).Vault
    vault = guardian.deploy(Vault)
    vault.initialize(token, gov, rewards, "", "", guardian)
    vault.setDepositLimit(2 ** 256 - 1, {"from": gov})
    vault.setManagement(management, {"from": gov})
    yield vault


@pytest.fixture
def yswapper_safe():
    yield Contract("0x31ABE8B1A645ac2d81201869d6eC77CF192e7d7F")


@pytest.fixture
def trade_factory(yswapper_safe, zrx_swapper, one_inch_swapper, sushi_swapper):
    yield Contract("0x3853fa6a2110CEF32aA49437F22319F888784B87")


@pytest.fixture
def one_inch_swapper():
    yield Contract("0x0902388b5e695aC9581b49B7E36DC38f921f4141")


@pytest.fixture
def sushi_swapper():
    yield Contract("0x128729f2Ce6cB31F6e85e21FD686D1F5b3c30226")


@pytest.fixture
def zrx_swapper():
    yield Contract("0xcce31974C651BFd6565262382776828d2Faaf998")


@pytest.fixture
def ymechanic(accounts):
    yield accounts.at("0xB82193725471dC7bfaAB1a3AB93c7b42963F3265", True)


@pytest.fixture
def strategy(
    accounts,
    strategist,
    keeper,
    vault,
    Strategy,
    gov,
    token,
    trade_factory,
    yswapper_safe,
    zrx_swapper
):
    strategy = Strategy.deploy(vault, trade_factory, {"from": strategist})

    # yswap first setup
    #trade_factory.grantRole(trade_factory.STRATEGY(), strategy, {"from": yswapper_safe})
    #trade_factory.setStrategyAsyncSwapper(strategy, zrx_swapper, {"from": yswapper_safe})

    strategy.setKeeper(keeper)
    vault.addStrategy(strategy, 10_000, 0, 2 ** 256 - 1, 1_000, {"from": gov})

    yield strategy


@pytest.fixture
def guard(
    strategist,
    YearnGuard,
    yswapper_safe
):
    yield YearnGuard.deploy(yswapper_safe, {"from": strategist})


@pytest.fixture
def whale(accounts):
    yield accounts.at("0xA1C4Aac752043258c1971463390013e6082C106f", force=True)
