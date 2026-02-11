# Power Sources for Billion-Year Autonomous Computing

Research into energy sources capable of powering a small autonomous computing device
for billions of years on Earth.

## 1. Radioisotope Power

### The Problem with Conventional RTGs

Standard RTGs use Pu-238 (half-life 87.7 years, specific power ~0.57 W/g). This is
far too short-lived. After 1,000 years, the power output is reduced to ~0.04% of
its initial value. Not viable for billion-year operation.

### Naturally Occurring Long-Lived Isotopes

| Isotope | Half-Life (years)   | Decay Energy (MeV) | Specific Thermal Power | Notes |
|---------|---------------------|---------------------|------------------------|-------|
| U-238   | 4.47 x 10^9        | 4.27 (alpha)        | ~8.5 uW/kg (alpha only), ~95 uW/kg (with full chain in secular equilibrium) | 99.3% of natural uranium |
| Th-232  | 1.40 x 10^10       | 4.08 (alpha)        | ~2.6 uW/kg (alpha only), ~26 uW/kg (full chain) | More abundant than uranium |
| K-40    | 1.25 x 10^9        | 1.31 (beta/gamma)   | ~3.4 nW/kg of natural potassium (~29 uW/kg of pure K-40) | Only 0.012% of natural K |
| Rb-87   | 4.92 x 10^10       | 0.28 (beta)         | ~0.6 uW/kg | Very low energy per decay |
| Sm-147  | 1.06 x 10^11       | 2.31 (alpha)        | ~0.13 uW/kg | Extremely long half-life |

### Key Calculations for U-238

The most promising long-lived isotope for power is U-238 (or natural uranium).

**Alpha-only power (U-238 decay alone):**
- Activity per kg = ln(2) / (t_half * m_atom) = 0.693 / (1.408e17 s * 3.95e-25 kg) = 1.246e7 decays/s/kg
- Power = 1.246e7 * 4.27 MeV * 1.602e-13 J/MeV = ~8.5 uW/kg

**With full decay chain (secular equilibrium):**
Natural uranium produces ~95-98 uW/kg when all daughter products are in secular
equilibrium (the entire U-238 decay chain through to Pb-206). This is because the
total decay energy of the full chain is ~47 MeV, roughly 11x the initial alpha decay.
The literature reports ~98.29 uW/kg for natural uranium in geochemical contexts.

**Practical implications:**
- 1 kg of natural uranium: ~95 uW (continuous, for billions of years)
- 10 kg: ~1 mW
- 100 kg: ~10 mW
- To get 1 mW, you need ~10 kg of uranium

This is a remarkably stable power source. After 4.47 billion years, you still have
50% of the original material. After 1 billion years, you retain ~86% power output.

### Th-232: Even Longer Lived

Thorium-232's half-life of 14 billion years means after 5 billion years, ~78% remains.
But its specific power is ~3-4x lower than U-238. You'd need ~30-40 kg for 1 mW.

Thorium is ~3-4x more abundant in Earth's crust than uranium, so sourcing it is easier.

### Conversion: Heat to Electricity

The challenge: these isotopes produce *heat*, not electricity. Conversion options:
- **Thermoelectric (Seebeck effect):** ~5-8% efficiency. So 10 mW thermal -> ~0.5-0.8 mW electrical.
- **Thermophotovoltaic:** Higher efficiency possible but requires higher temperatures.
- **Betavoltaic (direct):** Only works well with beta emitters. Ni-63 (100-year half-life)
  and tritium (12-year half-life) are used in existing devices but are too short-lived.

### Verdict on Radioisotope Power

**U-238 is the best candidate for billion-year radioisotope power.**
- ~10 kg of natural uranium -> ~1 mW thermal -> ~50-80 uW electrical (with thermoelectrics)
- Power declines only ~14% per billion years
- Uranium is available and stable as a metal or oxide
- No moving parts required

The power level is low but non-zero and extremely stable. A device running at the
Landauer limit could do an enormous number of operations per second with even 1 uW
(see Section 6 below).


## 2. Geothermal Energy

### Earth's Internal Heat Budget

- Total heat flow from interior to surface: ~44-47 TW
- Radiogenic heat production: ~30 TW (U, Th, K decay)
- Primordial heat: ~14-17 TW (leftover from formation)
- Average surface heat flux: ~91.6 mW/m^2 (~65 mW/m^2 for continental crust)

### How Long Will It Last?

Earth's core is cooling at ~100-200 K per billion years. The core temperature is
currently ~5,000-6,000 K. Even at 200 K/billion years, the core won't solidify for
tens of billions of years.

The radiogenic component (30 TW) will decline as isotopes decay:
- K-40 (1.25 Gy half-life) will be mostly gone in 5 billion years (~6% remaining)
- U-238 (4.47 Gy half-life) will be at ~46% in 5 billion years
- Th-232 (14 Gy half-life) will be at ~78% in 5 billion years

Net effect: total radiogenic heat production drops from ~30 TW today to roughly
~12-15 TW in 5 billion years. Combined with primordial heat, geothermal energy
will persist for the entire remaining main-sequence lifetime of the Sun.

### Power Available to a Small Device

**Surface geothermal gradient:** ~25-30 C/km in normal continental crust.
A device at 10m depth experiences a temperature difference of only ~0.25-0.3 C
relative to the surface.

**Using a thermoelectric generator on the geothermal gradient:**
- Temperature difference of 0.3 C at ~300 K
- Carnot efficiency: dT/T = 0.3/300 = 0.1%
- Real thermoelectric efficiency at this dT: extremely low, maybe 0.01-0.05%
- Heat flux available to a 1 m^2 collector: ~65 mW
- Electrical output: ~0.006 - 0.03 mW = 6-30 uW per m^2

**At geothermal hotspots or greater depth:**
- At 100m depth: dT ~ 3 C, Carnot efficiency ~1%, electrical output ~0.6 mW/m^2
- At 1 km depth: dT ~ 25-30 C, much more practical, milliwatts to watts possible
- Near volcanic/hydrothermal areas: temperature gradients much steeper

**Hot spring or geothermal vent:**
- dT of 50-80 C readily available
- A small thermoelectric module could produce 10-100 mW easily
- But specific vent locations are geologically transient (thousands to millions of years)

### Verdict on Geothermal

**Geothermal energy will be available for billions of years**, but:
- Surface gradients are tiny, yielding microwatts per m^2
- Deeper installations or geothermal hotspots give more power but are harder to maintain
- The geothermal gradient itself is one of the most stable energy sources on Earth
- A buried device with a long thermal conductor (heat pipe) reaching 10-100m depth
  could plausibly harvest 10s of uW to mW continuously
- No moving parts needed (thermoelectric conversion)

Main risk: geological change. Over billions of years, plate tectonics will move the
device, potentially burying it deeper or exposing it. The geothermal gradient itself
persists, but the local conditions change.


## 3. Solar Energy

### Sun's Main Sequence Lifetime

The Sun has ~5-5.5 billion years of main-sequence life remaining. During this time:
- Luminosity increases ~1% per 100 million years (~10% per billion years)
- Current solar constant: ~1361 W/m^2
- In 1 billion years: ~1497 W/m^2
- In 5 billion years: ~1905 W/m^2 (but Earth's surface conditions may be uninhabitable)

Solar power is the most energy-dense option by far. Even a 1 cm^2 solar cell receives
~136 mW in direct sunlight.

### Solar Cell Degradation

**Terrestrial silicon cells:** ~0.3-0.5% per year degradation
- After 25 years: ~88-92% of original output (standard warranty spec)
- After 100 years: ~60-77% of original output
- After 1,000 years: practically zero

**Space-grade GaAs cells:** ~0.44-1.03% per year (radiation-dominated in space)
**Terrestrial GaAs cells:** lower degradation than silicon, but still on the order
of decades to centuries at most.

**No known solar cell material can last billions of years without replacement.**

### Degradation Mechanisms
- UV-induced polymer degradation (encapsulant, backsheet)
- Corrosion of metal contacts
- Potential-induced degradation (PID)
- Light-induced degradation (LID)
- Moisture ingress
- Mechanical stress (thermal cycling)

### Could a Self-Maintaining Solar System Work?

The concept requires either:

1. **Biological photosynthesis:** Plants and photosynthetic organisms are self-repairing
   and self-replicating. Photosynthetic efficiency is low (~1-2% for most plants, up to
   ~6% theoretical max for C4 plants). A biological system coupled to a bioelectric
   converter could theoretically run indefinitely as long as conditions support life.
   - Cyanobacteria have existed for ~2.5 billion years already
   - But converting biological energy to electricity for computation is non-trivial

2. **Self-replicating machines:** A machine that can fabricate replacement solar cells
   from raw materials. This is essentially a von Neumann machine -- far beyond current
   technology and arguably requires a full industrial civilization.

3. **Extremely durable photoelectric materials:** Some research into perovskite self-healing
   properties, but current best lifetimes are ~30 years. Nowhere near billion-year scale.

### Verdict on Solar

**Solar provides the highest power density by far** (~100 mW/cm^2 in direct sunlight),
but **no known material can survive billions of years** without replacement or repair.

A biological photosynthetic system (e.g., cyanobacteria or algae coupled to a
bioelectrochemical cell) is the most plausible "self-maintaining solar" approach,
since biology has demonstrated multi-billion-year persistence. But the coupling
to a computing device is a major unsolved problem.

Solar power is available for ~5 billion more years (increasing in intensity), but
Earth's surface becomes uninhabitable to complex life in ~1 billion years due to
the runaway greenhouse effect from increasing solar luminosity.


## 4. Tidal / Gravitational Energy

### Current State of Earth-Moon System

- Moon recedes at 3.83 cm/year (measured by lunar laser ranging)
- Tidal energy dissipation: ~3.75 TW total
- Most of this (>97%) is converted to heat by ocean friction
- Only ~0.12 TW is transferred as orbital energy to the Moon
- Earth's day lengthens by ~2.3 milliseconds per century

### How Long Will Tides Last?

**Ocean tides as we know them: ~1-1.5 billion more years.**

After that, increasing solar luminosity will evaporate Earth's oceans, removing the
primary mechanism for tidal dissipation. Without oceans, the solid-body tides are
much weaker (the Moon still raises tides in the solid Earth, but the energy dissipation
is orders of magnitude less).

The theoretical endpoint of mutual tidal locking (Earth's day = Moon's orbital period
= ~47 current days) would take ~50 billion years, but the Sun destroys the Earth-Moon
system in ~5-7.5 billion years during its red giant phase.

### Power Available

A small tidal energy harvester could extract energy from:
- Ocean currents driven by tides
- Water level changes in coastal areas

Power levels from a small device: potentially milliwatts to watts, depending on
design. But this requires moving parts and is subject to:
- Biofouling
- Corrosion
- Mechanical wear
- Silting/sedimentation

### Verdict on Tidal

**Tidal energy is available for ~1-1.5 billion years** (as long as oceans exist),
potentially longer if solid-body tides are harnessed. But:
- Requires moving parts or deformable elements (corrosion, wear)
- Requires proximity to ocean/coast (geological instability on billion-year scales)
- Lower longevity than geothermal or radioisotope sources
- More mechanically complex than solid-state alternatives

Not the best choice for a billion-year device.


## 5. Other Notable Sources

### Atmospheric Temperature Cycling (Day/Night)

Temperature differences between day and night could drive a thermoelectric or
thermomechanical energy harvester. Typical dT: 5-20 C depending on location.
This would provide milliwatts and works as long as the atmosphere exists and the
planet rotates (~5 billion years). But it requires surviving surface conditions.

### Chemical Energy (Corrosion-Based)

Some bacteria harvest energy from redox reactions in rock. A device could potentially
tap into chemical gradients in the crust. But chemical reservoirs are finite and
local -- not billion-year sources unless continually replenished by geological processes.

### Ambient Electromagnetic Radiation

A rectenna harvesting thermal radiation or other EM energy. At room temperature,
the available energy density from blackbody radiation is real but thermodynamically
tricky to convert (you need a colder reservoir). Not a practical primary source.


## 6. Thermodynamic Minimum: Landauer's Principle

### The Fundamental Limit

The minimum energy to erase one bit of information (an irreversible logical operation):

    E_min = k_B * T * ln(2)

At room temperature (T = 300 K):

    E_min = 1.381e-23 J/K * 300 K * 0.693
    E_min = 2.87 x 10^-21 J per bit erasure
    E_min ~ 3 x 10^-21 J (as stated in the problem)

### What Does This Mean for Computation?

A single arithmetic operation (like adding two 64-bit numbers) involves on the order
of ~100-1000 irreversible bit operations (depending on the algorithm and architecture).
Let's use 1000 as a conservative upper bound.

**Minimum energy per arithmetic operation:**
    E_arith ~ 1000 * 3e-21 J = 3e-18 J = 3 aJ (attojoules)

### Operations Per Second at Various Power Levels

| Available Power | Operations/Second (at Landauer limit) | Operations/Second (1000x Landauer) |
|-----------------|---------------------------------------|-------------------------------------|
| 1 nW            | 3.3 x 10^11                           | 3.3 x 10^8                         |
| 1 uW            | 3.3 x 10^14                           | 3.3 x 10^11                        |
| 1 mW            | 3.3 x 10^17                           | 3.3 x 10^14                        |
| 1 W             | 3.3 x 10^20                           | 3.3 x 10^17                        |

Note: "1000x Landauer" represents a device that is 1000x less efficient than the
theoretical minimum -- which would still be ~1,000,000x more efficient than current
computers (which operate at ~10^9 x Landauer).

### Reversible Computing

With reversible computation (no bit erasure), the Landauer limit does not apply in
principle. Energy can be recycled, and computation can approach zero dissipation --
but at the cost of:
- Slower operation (approaching zero dissipation requires infinite time per operation)
- Greater circuit complexity (all operations must be logically reversible)
- Quantum effects still impose a minimum energy related to desired accuracy

A practical reversible computer might operate at, say, 10-100x the Landauer limit.

### Comparison: Available Power vs. Computation

**Scenario: 10 kg of U-238 (radioactive decay power)**
- Thermal power: ~1 mW
- Electrical power (after thermoelectric conversion, ~7%): ~70 uW
- At Landauer limit: 70 uW / 3e-21 J = ~2.3 x 10^16 bit operations/second
- At 1000x Landauer: ~2.3 x 10^13 bit operations/second
- Arithmetic operations (1000 bits each): ~2.3 x 10^10 ops/sec (at 1000x Landauer)

**That is ~23 GHz equivalent in arithmetic operations** -- comparable to a modern
CPU, from 10 kg of uranium, for 4.5 billion years. This is the power of operating
near the thermodynamic limit.

For comparison, a modern CPU at 5 GHz clock rate uses ~50-150 W. The same computation
rate, at Landauer limit, would need only ~15 nW. The ratio is ~10^10.

**Scenario: Geothermal (1 m^2 surface collector, 10m depth)**
- Electrical power: ~10-30 uW
- At 1000x Landauer: ~3-10 x 10^9 arithmetic ops/sec (~3-10 GHz equivalent)

**Scenario: Solar (1 cm^2 cell, 20% efficiency, 50% capacity factor)**
- Electrical power: ~14 mW
- At 1000x Landauer: ~4.7 x 10^12 arithmetic ops/sec (~4.7 THz equivalent)
- But solar cell won't last billions of years without replacement

### Key Insight

The enormous gap between current computing efficiency and the Landauer limit (factor
of ~10^9) means that a device designed to operate near the thermodynamic minimum could
perform a surprising amount of computation with very little power. The limiting factor
for a billion-year computer is NOT the amount of energy available -- it is the
engineering of devices that can survive and operate at ultra-low power near the
fundamental limits, for geological timescales.


## 7. Summary Comparison

| Source        | Power (small device) | Duration          | Moving Parts? | Reliability |
|---------------|----------------------|-------------------|---------------|-------------|
| U-238 (10 kg) | ~70 uW electrical   | 4.5+ billion yr   | No            | Excellent   |
| Th-232 (10 kg)| ~20 uW electrical   | 14+ billion yr    | No            | Excellent   |
| Geothermal    | ~10-30 uW/m^2       | 5+ billion yr     | No            | Good        |
| Solar (1 cm^2)| ~14 mW              | 5 billion yr (Sun)| No            | Poor (degradation) |
| Tidal         | mW-W range          | ~1 billion yr     | Yes           | Poor        |
| Day/night dT  | uW-mW range         | 5 billion yr      | No            | Moderate    |

### Recommendation

For a truly autonomous billion-year device, the most promising approaches are:

1. **Radioisotope (U-238 or Th-232):** Most reliable, no external dependencies, no
   moving parts, extremely predictable power output. Low power but sufficient when
   combined with near-Landauer-limit computation.

2. **Geothermal (passive thermoelectric):** Good backup/complement. Uses the same
   radioactive decay that heats the Earth, but harvests it via temperature gradient
   instead of direct decay. No fuel to carry -- but requires careful placement.

3. **Hybrid approach:** Radioisotope primary + geothermal secondary. Both are
   fundamentally powered by the same physics (radioactive decay), both are solid-state,
   and both will last for billions of years.

Solar provides orders of magnitude more power but cannot be sustained without
self-repair mechanisms that don't currently exist.


## Sources

- [Naturally-Occurring Radioactive Materials (NORM) - World Nuclear Association](https://world-nuclear.org/information-library/safety-and-security/radiation-and-health/naturally-occurring-radioactive-materials-norm)
- [Uranium-238 - Wikipedia](https://en.wikipedia.org/wiki/Uranium-238)
- [Radioisotopes Power Production (Ragheb)](https://mragheb.com/NPRE%20402%20ME%20405%20Nuclear%20Power%20Engineering/Radioisotopes%20Power%20Production.pdf)
- [K, Th, U, and Radiogenic Heat Production](https://tohoku.elsevierpure.com/en/publications/k-th-u-and-radiogenic-heat-production)
- [Radiogenic Power and Geoneutrino Luminosity of the Earth (McDonough 2020)](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2019GC008865)
- [Earth's Internal Heat Budget - Wikipedia](https://en.wikipedia.org/wiki/Earth's_internal_heat_budget)
- [Earth's Internal Heat - UC Berkeley](https://ugc.berkeley.edu/background-content/earths-internal-heat/)
- [Geothermal Energy from Nuclear Decay (Stanford)](http://large.stanford.edu/courses/2024/ph241/slye1/)
- [Radioisotope Thermoelectric Generator - Wikipedia](https://en.wikipedia.org/wiki/Radioisotope_thermoelectric_generator)
- [Radioisotope Power Systems FAQ - NASA](https://science.nasa.gov/planetary-science/programs/radioisotope-power-systems/faq/)
- [Beyond Plutonium-238: Alternate Fuel (Stanford)](http://large.stanford.edu/courses/2022/ph241/spaugh1/)
- [Sun - Wikipedia](https://en.wikipedia.org/wiki/Sun)
- [Tidal Acceleration - Wikipedia](https://en.wikipedia.org/wiki/Tidal_acceleration)
- [Earth-Moon Evolution: Orbit & Ocean Tide Models](https://pmc.ncbi.nlm.nih.gov/articles/PMC9285098/)
- [Tides - NASA Science](https://science.nasa.gov/moon/tides/)
- [Landauer's Principle - Wikipedia](https://en.wikipedia.org/wiki/Landauer's_principle)
- [The Landauer Limit: Why Erasing A Bit Generates Heat](https://quantumzeitgeist.com/landauer-limit-why-erasing-a-bit-generates-heat/)
- [Fundamental Energy Limits and Reversible Computing (DOE)](https://www.osti.gov/servlets/purl/1458032)
- [Betavoltaic Device - Wikipedia](https://en.wikipedia.org/wiki/Betavoltaic_device)
- [Nuclear Battery Revival - IEEE Spectrum](https://spectrum.ieee.org/nuclear-battery-revival)
- [Low-Temperature Thermoelectric Energy Harvesting](https://www.mdpi.com/2076-3417/13/4/2603)
- [Solar Cell Degradation GaAs vs Si (Inderscience)](https://www.inderscience.com/info/inarticle.php?artid=90549)
- [GaAs Solar Cells Overview (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8200097/)
- [First Long-Lived Perovskite Solar Cells (BNL)](https://www.bnl.gov/newsroom/news.php?a=221018)
