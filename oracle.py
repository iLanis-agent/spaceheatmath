import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def fmt(x): return str(jsnum(x))
def round1(x): return jsnum(math.floor(x * 10 + 0.5) / 10)
def round50(x): return jsnum(math.floor(x / 50 + 0.5) * 50)
def round0(x): return jsnum(math.floor(x + 0.5))

W_PER_M2 = 100
BASE_CEIL = 2.4
VOLTS = 120
CONT_FACTOR = 0.8
CENTS_PER_KWH = 25

def watt_plan(areaM2, ceilingM):
    if not (areaM2 > 0) or not (ceilingM > 0):
        return {"error": "the room and the ceiling must be positive"}
    watts = round50(areaM2 * W_PER_M2 * ceilingM / BASE_CEIL)
    if watts <= 750: verdict = "a desk-warmer job"
    elif watts <= 1500: verdict = "a tower-heater room"
    else: verdict = "a two-heater space"
    return {"watts": watts, "verdict": verdict}

def circuit_plan(watts, amps):
    if not (watts > 0) or not (amps > 0):
        return {"error": "the watts and the breaker must be positive"}
    usable = round0(amps * VOLTS * CONT_FACTOR)
    margin = usable - watts
    if margin >= 240: verdict = "room to spare"
    elif margin >= 0: verdict = "a dedicated-plug job"
    else: verdict = "over the breaker"
    return {"usable": usable, "margin": margin, "verdict": verdict}

def cost_plan(watts, hours):
    if not (watts > 0) or not (hours > 0):
        return {"error": "the watts and the hours must be positive"}
    day_kwh = round1(watts * hours / 1000)
    month_kwh = round0(day_kwh * 30)
    cost = jsnum(math.floor(month_kwh * CENTS_PER_KWH + 0.5) / 100)
    if cost <= 15: verdict = "pocket change"
    elif cost <= 60: verdict = "a line on the bill"
    else: verdict = "the meter's second job"
    return {"dayKwh": day_kwh, "monthKwh": month_kwh, "cost": cost, "verdict": verdict}

def render_watt(r, areaM2, ceilingM):
    return ("Your " + fmt(areaM2) + " m2 room with a " + fmt(ceilingM) + " m ceiling needs about " + fmt(r["watts"])
            + " W of heat - " + r["verdict"] + ".")

def render_circuit(r, watts, amps):
    if r["margin"] >= 0:
        return ("A " + fmt(amps) + " A breaker at a labeled " + fmt(VOLTS) + " V holds " + fmt(r["usable"]) + " W continuous; your "
                + fmt(watts) + " W heater leaves " + fmt(r["margin"]) + " W to spare - " + r["verdict"] + ".")
    return ("A " + fmt(amps) + " A breaker at a labeled " + fmt(VOLTS) + " V holds " + fmt(r["usable"]) + " W continuous; your "
            + fmt(watts) + " W heater comes up " + fmt(-r["margin"]) + " W short - " + r["verdict"] + ".")

def render_cost(r, watts, hours):
    return ("Running " + fmt(watts) + " W for " + fmt(hours) + " h a day is " + fmt(r["dayKwh"]) + " kWh daily, "
            + fmt(r["monthKwh"]) + " kWh a month - about $" + fmt(r["cost"]) + " at a labeled " + fmt(CENTS_PER_KWH)
            + " cents a kWh - " + r["verdict"] + ".")

cases = []
def add(fn, f, rf, args):
    r = f(*args)
    c = {"fn": fn, "args": args, "result": r}
    if "error" not in r: c["render"] = rf(r, *args)
    cases.append(c)

for a in [[12,2.4],[20,3],[6,2.4],[15,2.7],[10,2.4],[25,2.4],[8,2.5],[18,3],[0,2.4],[12,0]]:
    add("wattPlan", watt_plan, render_watt, a)
for a in [[1500,15],[1200,15],[1500,20],[900,15],[2000,20],[1440,15],[1600,15],[750,15],[0,15],[1500,0]]:
    add("circuitPlan", circuit_plan, render_circuit, a)
for a in [[1200,4],[1500,8],[600,2],[2000,6],[900,3],[1500,24],[1200,1],[1800,5],[0,4],[1200,0]]:
    add("costPlan", cost_plan, render_cost, a)
json.dump(cases, open("expected.json", "w"), separators=(",", ":"))
print(len(cases), "cases")
