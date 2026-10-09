# GCC-Wireless

A learner's project to make a GameCube controller wireless, documented so a newcomer (and their AI assistant) can answer "why does X do Y" from this repo alone.

**Goal:** a PhobGCC controller (open-source GameCube controller board) in a stock GameCube shell, sending inputs over a Nordic nRF52 radio to (a) a real GameCube/Wii and (b) a PC over USB.

**Status:** research and setup only. No hardware owned yet. See [docs/STATUS.md](docs/STATUS.md).

## Where things live
| You want | Read |
|---|---|
| What works / what is blocked now | [docs/STATUS.md](docs/STATUS.md) |
| What happened, in order, including failures | [docs/BUILD_LOG.md](docs/BUILD_LOG.md) |
| Verified facts about the tech | [docs/facts/](docs/facts/) (joybus, nRF52 radio, RP2040 PIO/SPI, PhobGCC, power) |
| Why we chose this platform | [docs/DECISIONS.md](docs/DECISIONS.md) |
| Questions asked and answers | [docs/FAQ.md](docs/FAQ.md) |
| Upstream code, versions, licenses | [docs/PROVENANCE.md](docs/PROVENANCE.md) |

## Getting the code
```
git clone --recurse-submodules <this repo>
```
`upstream/` holds other people's projects pinned at exact commits (git submodules). All are GPL-3.0; so is this repo.

## Rules for the docs
Write verified facts with a source (file + commit, or URL). Mark anything not checked as **Unverified**. Define every acronym once.

## How this repo is built
The planner, worker and evaluator AI agents that work on this repo run from the configuration in https://github.com/Gidntsquia/claude-config/releases/tag/v1.0.0 (release v1.0.0, published 2026-10-09 UTC; the release exists, checked with `gh release view`).
