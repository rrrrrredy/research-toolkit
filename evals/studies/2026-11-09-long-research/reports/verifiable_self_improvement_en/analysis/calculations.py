"""Reported-value arithmetic and explicitly hypothetical illustrations, not model trials."""
from pathlib import Path
import json

result = {
    'reported_value_arithmetic': {
        'harnesspro_tb_gain_percentage_points': round(80.8 - 76.3, 4),
        'harnesspro_tb_mean_execution_cost_reduction_percent': round((1.09 - 0.72) / 1.09 * 100, 4),
        'score_math_base_second_minus_first_pp': round(41.4 - 52.6, 4),
        'score_math_trained_second_minus_first_pp': round(64.4 - 60.0, 4),
        'score_math_change_in_correction_delta_pp': round((64.4 - 60.0) - (41.4 - 52.6), 4),
        'dgm_full_polyglot_gain_pp': round(30.7 - 14.2, 4),
        'rethinking_heldout_mean_gain_pp': round(((64.5 - 63.3) + (72.1 - 72.1)) / 2, 4),
    },
    'hypothetical_amdahl_examples': [
        {'original_runtime_fraction': f, 'component_speed_multiplier': 1.23,
         'new_normalized_runtime': round((1-f) + f/1.23, 6),
         'total_runtime_reduction_percent': round((1-((1-f) + f/1.23))*100, 4)}
        for f in (0.05, 0.2, 0.8)
    ],
    'scope': 'Arithmetic on published values; fractions 0.05/0.2/0.8 are invented illustrations, not inferred Google profiles.'
}
Path(__file__).with_name('calculation-results.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, indent=2))
