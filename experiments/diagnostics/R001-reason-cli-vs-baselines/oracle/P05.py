import json
from decimal import Decimal, ROUND_HALF_UP, getcontext

getcontext().prec = 50
p0 = Decimal("101325")
rho = Decimal("997.0")
g = Decimal("9.80665")
depth = Decimal("7.800")
length = Decimal("2.600")
r = rho * g
b = p0 + r * (depth - length)
discriminant = b * b + Decimal(4) * r * p0 * length
root = discriminant.sqrt()
air_length = (Decimal(2) * p0 * length) / (b + root)
negative_air_length = (-b - root) / (Decimal(2) * r)
rise = length - air_length
pressure_pa = p0 + r * (depth - rise)
pressure_kpa = pressure_pa / Decimal(1000)
rounded_rise = rise.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
rounded_pressure = pressure_kpa.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
assert Decimal(0) < rise < length
assert negative_air_length < 0
assert abs(pressure_pa * air_length - p0 * length) < Decimal("1e-35")
assert rounded_rise == Decimal("1.028")
assert rounded_pressure == Decimal("167.5")

payload = {
    "problem_id": "P05",
    "answer": {
        "rise_m": float(rounded_rise),
        "pressure_kpa_absolute": float(rounded_pressure),
    },
    "diagnostics": {
        "unrounded_rise_m": str(rise),
        "unrounded_pressure_pa": str(pressure_pa),
        "air_length_m": str(air_length),
        "rejected_air_length_m": str(negative_air_length),
        "tolerance_rise_m": "0.0005",
        "tolerance_pressure_kpa": "0.05",
    },
}
print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
