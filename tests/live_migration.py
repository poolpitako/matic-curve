from brownie import accounts, config, reverts, Wei, Contract
from useful_methods import state_of_vault, state_of_strategy
import brownie


def test_live_migration(web3, chain, vault, strategy, token, whale, gov, strategist, rewards, amount):

    live_strat = Contract("0xE73817de3418bB44A4FeCeBa53Aa835333C550e7", owner=gov)
    new_strat = Contract("0x106838c85Ab33F41567F7AbCfF787d7269E824AF", owner=gov)
    vault = Contract(new_strat.vault(), owner=gov)
    proxy = Contract(new_strat.proxy(), owner=gov)

    print(f"before migration")
    print(f"old balanceOfPool: {live_strat.balanceOfPool()/1e18}")
    print(f"old balanceOfWant: {live_strat.balanceOfWant()/1e18}")
    print(f"new balanceOfPool: {new_strat.balanceOfPool()/1e18}")
    print(f"new balanceOfWant: {new_strat.balanceOfWant()/1e18}")
    print()
    vault.migrateStrategy(live_strat, new_strat)
    print()
    print(f"after migration")
    print(f"old balanceOfPool: {live_strat.balanceOfPool()/1e18}")
    print(f"old balanceOfWant: {live_strat.balanceOfWant()/1e18}")
    print(f"new balanceOfPool: {new_strat.balanceOfPool()/1e18}")
    print(f"new balanceOfWant: {new_strat.balanceOfWant()/1e18}")
    proxy.approveStrategy(new_strat.gauge(), new_strat)
    new_strat.harvest()

    print(f"\n >>> after migration")
    state_of_strategy(live_strat, token, vault)
    state_of_strategy(new_strat, token, vault)
    state_of_vault(vault, token)

    stkaave = Contract("0x4da27a545c0c5B758a6BA100e3a049001de870f5")
    ykeeper = accounts.at("0x1ea056C13F8ccC981E51c5f1CDF87476666D0A74", force=True)
    print(f"stkaave on keeper: {stkaave.balanceOf(ykeeper)/1e18}")

    # balanceOfPool is the same b/c they see the same gauge with same voter
    print(f"old balanceOfPool: {live_strat.balanceOfPool()/1e18}")
    print(f"old balanceOfWant: {live_strat.balanceOfWant()/1e18}")
    print(f"new balanceOfPool: {new_strat.balanceOfPool()/1e18}")
    print(f"new balanceOfWant: {new_strat.balanceOfWant()/1e18}")

    print(f"\n >>> wait 1 day to get the share price back")
    chain.sleep(86400)
    chain.mine(1)
    state_of_strategy(live_strat, token, vault)
    state_of_strategy(new_strat, token, vault)
    state_of_vault(vault, token)
