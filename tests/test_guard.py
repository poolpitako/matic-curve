from brownie import accounts, config, reverts, Wei, Contract, interface

def test_guard(
    strategist,
    guard,
    yswapper_safe
):

    original = Contract("0x3E5c63644E683549055b9Be8653de26E0B4CD36E")
    yswapper_safe = Contract.from_abi("yswappers", yswapper_safe.address, original.abi)
    yswapper_safe.setGuard(guard, {"from": yswapper_safe})

    assert False
