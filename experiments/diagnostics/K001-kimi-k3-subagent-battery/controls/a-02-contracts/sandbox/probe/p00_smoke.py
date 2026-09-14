"""Does the package import here, and are the re-exports the same objects?"""
from __future__ import annotations

import _boot  # noqa: F401

from minireason.loop import contracts, standard, types

print("contracts imported:", contracts.CONTRACTS_VERSION)
print("SCHEMAS is standard.SCHEMAS:", contracts.SCHEMAS is standard.SCHEMAS)
print("FORBIDDEN_KEYS is standard.FORBIDDEN_KEYS:",
      contracts.FORBIDDEN_KEYS is standard.FORBIDDEN_KEYS)
print("DIFFERENCE_KINDS is standard.DIFFERENCE_KINDS:",
      contracts.DIFFERENCE_KINDS is standard.DIFFERENCE_KINDS)
print("READING_VOCABULARY:", contracts.READING_VOCABULARY)
print("CRITIC_RELATIONS:", contracts.CRITIC_RELATIONS)
print("ALL_DIFFERENCE_KINDS:", contracts.ALL_DIFFERENCE_KINDS,
      len(contracts.ALL_DIFFERENCE_KINDS))
print("SCHEMA_REASONS count:", len(contracts.SCHEMA_REASONS))
print("roles:", sorted(contracts.SCHEMAS))
print("LoopError is base of ContractError:",
      issubclass(contracts.ContractError, types.LoopError))
