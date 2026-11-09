"""One new hypothetical pack-envelope scenario; existing calculations are not run."""
from pathlib import Path
import json

inputs = {
    "usable_energy_kwh": 75,
    "usable_fraction_of_nominal": 0.90,
    "vehicle_envelope_l": 300,
    "outside_pack_installation_reserve_l": 20,
    "pack_density_wh_per_l": {"A_candidate_LFP": 240, "B_candidate_NCM": 320},
    "lower_usable_energy_sensitivity_kwh": 60,
    "scope": "Explicit assumptions, not measured Blade/Qilin specifications or chemistry-wide ranges. Pack density includes enclosure, internal cooling/protection/BMS; the separate 20 L is external connections and installation clearance. Same reference temperature, new-pack state and usable window; no winter or aging derating.",
}
space = inputs["vehicle_envelope_l"] - inputs["outside_pack_installation_reserve_l"]
nominal = inputs["usable_energy_kwh"] / inputs["usable_fraction_of_nominal"]
results = {}
for name, density in inputs["pack_density_wh_per_l"].items():
    pack_l = nominal * 1000 / density
    installed_l = pack_l + inputs["outside_pack_installation_reserve_l"]
    results[name] = {
        "nominal_energy_required_kwh": nominal,
        "required_pack_volume_l": pack_l,
        "required_installed_volume_l": installed_l,
        "envelope_margin_l": inputs["vehicle_envelope_l"] - installed_l,
        "max_usable_energy_in_envelope_kwh": space * density / 1000 * inputs["usable_fraction_of_nominal"],
        "fits_volume_necessary_condition": installed_l <= inputs["vehicle_envelope_l"],
    }
output = {
    "kind": "author_hypothetical_scenario",
    "author": "/root/remaining_research_inputs",
    "inputs": inputs,
    "formulas": {
        "nominal_energy_kwh": "usable_energy_kwh / usable_fraction",
        "installed_volume_l": "usable_energy_kwh * 1000 / (usable_fraction * pack_density_wh_per_l) + external_reserve_l",
        "minimum_pack_density_wh_per_l": "usable_energy_kwh * 1000 / (usable_fraction * (envelope_l - external_reserve_l))",
    },
    "results": results,
    "minimum_pack_density_wh_per_l": nominal * 1000 / space,
    "A_at_60_usable_kwh_installed_volume_l": inputs["lower_usable_energy_sensitivity_kwh"] * 1000 / (inputs["usable_fraction_of_nominal"] * 240) + inputs["outside_pack_installation_reserve_l"],
    "lower_energy_target_reduction_fraction": 1 - inputs["lower_usable_energy_sensitivity_kwh"] / inputs["usable_energy_kwh"],
    "limits": "Volume is a necessary condition only. Shape, height, crash structure, mass, power, thermal management and lifetime remain separate constraints. No vehicle/model experiment, cost estimate or earlier calculation was rerun.",
}
destination = Path(__file__).with_name("volume-scenario-full-03.json")
if destination.exists():
    raise FileExistsError(destination)
destination.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf8", newline="\n")
print(json.dumps(output, ensure_ascii=False, indent=2))
