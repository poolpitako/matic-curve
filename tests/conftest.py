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
def amount(accounts, token, whale):
    amount = 100 * 10 ** token.decimals()
    # In order to get some funds for the token you are about to use,
    # it impersonate an exchange address to use it's funds.
    reserve = whale
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
def trade_factory():
    yield Contract("0xc9EB13d39bd7fF767bE985f5640a43b07104b40d")


@pytest.fixture
def sushi_swapper():
    yield Contract("0x67B4fEDD812656Ea44CE977f2c818532E5D91571")


@pytest.fixture
def swapper_registry():
    yield Contract("0xcb12Ac8649eA06Cbb15e29032163938D5F86D8ad")


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
    sushi_swapper,
    swapper_registry,
    ymechanic,
):
    strategy = Strategy.deploy(vault, trade_factory, {"from": strategist})
    trade_factory.grantRole(trade_factory.STRATEGY(), strategy, {"from": ymechanic})
    strategy.setSwapper(swapper_registry.nameByAddress(sushi_swapper), False)
    strategy.setSwapperCheckpoint(chain.time(), {"from": vault.governance()})
    strategy.setKeeper(keeper)
    vault.addStrategy(strategy, 10_000, 0, 2 ** 256 - 1, 1_000, {"from": gov})

    yield strategy


@pytest.fixture
def whale(accounts):
    # binance7 wallet
    # acc = accounts.at('0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8', force=True)

    # binance8 wallet
    # acc = accounts.at('0xf977814e90da44bfa03b6295a0616a897441acec', force=True)

    # whale
    acc = accounts.at("0x0172e05392aba65366c4dbbb70d958bbf43304e4", force=True)
    yield acc
