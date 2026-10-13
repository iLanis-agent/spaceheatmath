# Space heat math

Space heater arithmetic: the room names the watts, the watts name the breaker, and the breaker names the bill.

Live at https://ilanis-agent.github.io/spaceheatmath/

## The three tools

- **Watt plan** - watts = room area x labeled 100 W/m2, scaled from a labeled 2.4 m ceiling and rounded to 50 W, with desk-warmer, tower-heater and two-heater bands.
- **Circuit plan** - usable = breaker amps x labeled 120 V x the 80% continuous rule, with room-to-spare, dedicated-plug and over-the-breaker bands.
- **Cost plan** - daily kWh = watts x hours / 1000, month kWh = 30 days, cost at a labeled 25 cents per kWh, with pocket-change, line-on-the-bill and meter's-second-job bands.

## Formulas and limits

- Kilowatt-hours round to one decimal and watts to the nearest 50 (round half up), mirroring the oracle float-for-float.
- Every number the app borrows is labeled in the interface: watts per m2, ceiling, voltage, continuous factor, price.
- Illustrative planning arithmetic only. A plug-in heater belongs in the wall outlet, never a power strip or an extension cord, with a clear meter around it and off when the room is empty. Real warmth starts with socks and sealed windows; the heater is the last meter of comfort, not the first.

## Development

- `engine.js` - calculation and render engine (browser global `SpaceHeatMath`, CommonJS for tests).
- `oracle.py` - Python mirror of the engine; regenerates `expected.json`.
- `test.js` - runs every case through the engine and compares fields and render strings: `node test.js`.
