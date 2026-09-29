# Dominyk SynKairos adapter

This directory is the first integration boundary between the upstream MiroFish engine and the Dominyk platform.

## What is adapted

- Dominyk's `SynKairosStudio` sends a normalized scenario brief, lens, population size and round count.
- `synkairos_adapter.py` validates those fields and maps them to engine-neutral simulation concepts.
- The adapter is **draft-first** and explicitly sets `external_actions: false`.
- It does not connect to brokers, wallets, trading venues or transaction endpoints.

## Engine mapping

| Dominyk concept | MiroFish concept |
|---|---|
| Scenario brief | Seed context / project input |
| SynKairos lens | Scenario metadata |
| Population | Agent/profile generation |
| Rounds | Simulation run configuration |
| Report | Downstream report and decision room |

The existing MiroFish API families remain the source of truth for graph building, simulation, profiles, timeline, agent stats and reports. The next implementation phase can add an authenticated Dominyk server route that calls those APIs; this adapter intentionally makes no network call until the deployment contract and secrets are configured.

## License and attribution

The upstream project is [MiroFish](https://github.com/666ghj/MiroFish), licensed under **AGPL-3.0**. This fork keeps the upstream license and attribution. Dominyk-specific integration code in this directory is released under the same repository license unless a file states otherwise.
