"""Dominyk -> MiroFish adapter boundary.

This module deliberately contains no network calls and no broker/trading integration.
It normalizes the SynKairos UI payload into the simulation concepts already exposed
by MiroFish: seed context, population size, rounds and lens metadata.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


ALLOWED_LENSES = {"market", "narrative", "strategy"}
MAX_AGENTS = 1000


@dataclass(frozen=True)
class SynKairosRequest:
    brief: str
    lens: str = "market"
    population: int = 250
    rounds: int = 12
    thesis: str | None = None

    def normalized(self) -> "SynKairosRequest":
        brief = self.brief.strip()
        if not brief:
            raise ValueError("brief is required")
        lens = self.lens if self.lens in ALLOWED_LENSES else "market"
        population = min(MAX_AGENTS, max(12, int(self.population)))
        rounds = min(48, max(1, int(self.rounds)))
        thesis = self.thesis.strip() if isinstance(self.thesis, str) and self.thesis.strip() else None
        return SynKairosRequest(brief=brief, lens=lens, population=population, rounds=rounds, thesis=thesis)


def to_mirofish_payload(request: SynKairosRequest) -> dict[str, Any]:
    """Return an engine-neutral payload for the existing MiroFish API layer."""
    item = request.normalized()
    return {
        "source": "dominyk-synkairos",
        "mode": "draft-first",
        "external_actions": False,
        "scenario": {
            "brief": item.brief,
            "lens": item.lens,
            "thesis": item.thesis,
        },
        "simulation": {
            "agent_count": item.population,
            "rounds": item.rounds,
        },
    }


def from_mapping(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a JSON-like SynKairos request without executing a simulation."""
    request = SynKairosRequest(
        brief=str(payload.get("brief", "")),
        lens=str(payload.get("lens", "market")),
        population=int(payload.get("population", 250)),
        rounds=int(payload.get("rounds", 12)),
        thesis=payload.get("thesis"),
    )
    return to_mirofish_payload(request)


__all__ = ["ALLOWED_LENSES", "MAX_AGENTS", "SynKairosRequest", "from_mapping", "to_mirofish_payload"]
