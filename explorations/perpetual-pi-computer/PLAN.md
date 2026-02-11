# Perpetual Pi Computer: Analysis Plan

## The Problem

Build a computing system that continuously computes digits of pi from now until the Sun becomes a red giant and renders Earth uninhabitable (~5 billion years from now).

"Computer" is interpreted in the broadest sense: electronic, mechanical, biological, quantum, or anything else that performs computation.

## Design Parameters (from discussion)

- **Fully autonomous**: must survive with zero intervention
- **Always be computing**: the machine must be actively computing pi at every moment
- **Anything goes**: no technology constraints

## Key Constraints

- **Duration**: ~5 x 10^9 years (but see ENVIRONMENTAL-THREATS.md -- Earth's surface melts at ~3.5 Gyr)
- **Environment**: Earth's subsurface, subject to geological and eventually solar changes
- **Goal**: Always be computing pi; storage is secondary

## Research Documents

| Document | Contents |
|---|---|
| [POWER-SOURCES.md](POWER-SOURCES.md) | U-238, geothermal, solar, tidal, Landauer analysis |
| [RESEARCH-SUBSTRATES.md](RESEARCH-SUBSTRATES.md) | Material longevity, biological computing, mechanical computing, self-replication, redundancy |
| [RESEARCH.md](RESEARCH.md) | Pi algorithms (BBP, Machin, Chudnovsky, spigot) and physical limits (Landauer, Bremermann, Margolus-Levitin) |
| [ENVIRONMENTAL-THREATS.md](ENVIRONMENTAL-THREATS.md) | Ice ages, volcanoes, asteroids, plate tectonics, solar evolution, erosion, placement strategy |
| [SYNTHESIS.md](SYNTHESIS.md) | Candidate architecture ("The Deep Mycelia"), the 5-Gyr problem, conclusions |

## Challenge Dimensions

### 1. Power Source
- [x] Solar -- see POWER-SOURCES.md (high power but cells degrade; not viable without self-repair)
- [x] Geothermal -- see POWER-SOURCES.md (~10-30 uW/m^2, lasts 5+ Gyr)
- [x] Radioisotope (U-238) -- see POWER-SOURCES.md (winner: ~70 uW from 10 kg, lasts 4.5 Gyr)
- [x] Tidal -- see POWER-SOURCES.md (not viable: moving parts, oceans evaporate at ~1 Gyr)
- [x] Landauer analysis -- see POWER-SOURCES.md (even 70 uW provides ~23 GHz equivalent at Landauer limit)

### 2. Hardware Longevity
- [x] Self-repairing systems -- see RESEARCH-SUBSTRATES.md (biological is the only viable approach)
- [x] Redundancy (TMR with repair) -- see RESEARCH-SUBSTRATES.md (TMR + 1-day repair = 44 Gyr MTBF)
- [x] Mechanical computation -- see RESEARCH-SUBSTRATES.md (sapphire, ~10^6 yr lifespan)
- [x] Stable substrates -- see RESEARCH-SUBSTRATES.md (zircon 4.375 Gyr, 5D quartz 13.8 Gyr)
- [x] Biological computing -- see RESEARCH-SUBSTRATES.md (slow but self-repairing)

### 3. Error Correction & Reliability
- [x] Redundancy approaches -- see RESEARCH-SUBSTRATES.md and SYNTHESIS.md
- [x] Verification via BBP -- see RESEARCH.md (verify any hex digit independently)
- [x] Diverse algorithms prevent common-mode failure -- see SYNTHESIS.md

### 4. Storage
- [x] Expected digits: 10^10 to 10^14 depending on power and algorithm -- see RESEARCH.md
- [x] Storage medium: 5D quartz crystal (13.8 Gyr, 360 TB/disc) -- see RESEARCH-SUBSTRATES.md
- [x] Goal is "always computing" not "maximize stored digits" -- but archive anyway

### 5. Algorithm Choice
- [x] All major algorithms analyzed -- see RESEARCH.md
- [x] Recommendation: Machin-like primary, BBP for verification -- see SYNTHESIS.md

### 6. Environmental Threats
- [x] Ice ages, volcanoes, asteroids, tectonics -- see ENVIRONMENTAL-THREATS.md (all survivable underground)
- [x] Solar evolution -- see ENVIRONMENTAL-THREATS.md (**the hard limit: ~3-3.5 Gyr on Earth**)
- [x] Best placement: Canadian Shield, 500-1000m depth -- see ENVIRONMENTAL-THREATS.md

### 7. Physical/Thermodynamic Limits
- [x] Landauer's principle -- see RESEARCH.md
- [x] Bremermann, Margolus-Levitin -- see RESEARCH.md
- [ ] Bekenstein bound (trivially not binding: 10^43 bits for 1 kg, we need ~10^14)

## Key Findings

1. **The device cannot survive 5 Gyr on Earth.** Solar evolution melts the surface at ~3.5 Gyr. Hard limit for Earth-bound computation: ~2.5-3 Gyr.
2. **U-238 is the optimal power source.** 50 kg provides ~5 mW thermal for 4.5 Gyr. Solid-state, no dependencies.
3. **Biology is the only viable self-repair mechanism.** No other substrate can maintain itself indefinitely.
4. **TMR with diverse algorithms solves reliability.** Machin-like + spigot + BBP, cross-verified.
5. **5D quartz crystal solves storage.** 13.8 Gyr lifetime, 360 TB per disc.
6. **Canadian Shield at 800m depth is the optimal location.**
7. **For true 5 Gyr operation, the device must leave Earth.**

## Proposed Architecture

See [SYNTHESIS.md](SYNTHESIS.md) for the "Deep Mycelia" architecture: a hybrid biological-mechanical-electronic system buried in the Canadian Shield.

## Status

- [x] Problem definition and constraints
- [x] Power source research
- [x] Hardware/substrate research
- [x] Algorithm research
- [x] Physical limits research
- [x] Environmental threats research
- [x] Synthesis and candidate architecture
- [ ] Detailed design of biological maintenance layer
- [ ] Thermal modeling of underground temperature over time
- [ ] Prototype design (1000-year version)
- [ ] Space probe option analysis
