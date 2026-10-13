(function (root) {
  "use strict";
  var W_PER_M2 = 100;   // labeled watts per m2 at a labeled 2.4 m ceiling
  var BASE_CEIL = 2.4;  // labeled ceiling, meters
  var VOLTS = 120;      // labeled mains voltage
  var CONT_FACTOR = 0.8; // labeled continuous-load factor
  var CENTS_PER_KWH = 25; // labeled electricity price, cents per kWh

  function round1(x) { return Math.round(x * 10) / 10; }
  function round50(x) { return Math.round(x / 50) * 50; }

  function wattPlan(areaM2, ceilingM) {
    if (!(areaM2 > 0) || !(ceilingM > 0)) return { error: "the room and the ceiling must be positive" };
    var watts = round50(areaM2 * W_PER_M2 * ceilingM / BASE_CEIL);
    var verdict;
    if (watts <= 750) verdict = "a desk-warmer job";
    else if (watts <= 1500) verdict = "a tower-heater room";
    else verdict = "a two-heater space";
    return { watts: watts, verdict: verdict };
  }

  function circuitPlan(watts, amps) {
    if (!(watts > 0) || !(amps > 0)) return { error: "the watts and the breaker must be positive" };
    var usable = Math.round(amps * VOLTS * CONT_FACTOR);
    var margin = usable - watts;
    var verdict;
    if (margin >= 240) verdict = "room to spare";
    else if (margin >= 0) verdict = "a dedicated-plug job";
    else verdict = "over the breaker";
    return { usable: usable, margin: margin, verdict: verdict };
  }

  function costPlan(watts, hours) {
    if (!(watts > 0) || !(hours > 0)) return { error: "the watts and the hours must be positive" };
    var dayKwh = round1(watts * hours / 1000);
    var monthKwh = Math.round(dayKwh * 30);
    var cost = Math.round(monthKwh * CENTS_PER_KWH) / 100;
    var verdict;
    if (cost <= 15) verdict = "pocket change";
    else if (cost <= 60) verdict = "a line on the bill";
    else verdict = "the meter's second job";
    return { dayKwh: dayKwh, monthKwh: monthKwh, cost: cost, verdict: verdict };
  }

  function renderWatt(r, areaM2, ceilingM) {
    return "Your " + areaM2 + " m2 room with a " + ceilingM + " m ceiling needs about " + r.watts
      + " W of heat - " + r.verdict + ".";
  }

  function renderCircuit(r, watts, amps) {
    if (r.margin >= 0) {
      return "A " + amps + " A breaker at a labeled " + VOLTS + " V holds " + r.usable + " W continuous; your "
        + watts + " W heater leaves " + r.margin + " W to spare - " + r.verdict + ".";
    }
    return "A " + amps + " A breaker at a labeled " + VOLTS + " V holds " + r.usable + " W continuous; your "
      + watts + " W heater comes up " + (-r.margin) + " W short - " + r.verdict + ".";
  }

  function renderCost(r, watts, hours) {
    return "Running " + watts + " W for " + hours + " h a day is " + r.dayKwh + " kWh daily, "
      + r.monthKwh + " kWh a month - about $" + r.cost + " at a labeled " + CENTS_PER_KWH
      + " cents a kWh - " + r.verdict + ".";
  }

  var api = { wattPlan: wattPlan, circuitPlan: circuitPlan, costPlan: costPlan, renderWatt: renderWatt, renderCircuit: renderCircuit, renderCost: renderCost };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.SpaceHeatMath = api;
})(this);
