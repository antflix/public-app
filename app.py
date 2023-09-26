from flask import Flask, render_template, request
import math
from fractions import Fraction

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/offset', methods=['GET', 'POST'])
def offset():
    picture = 'offset-labeled.png'
    if request.method == 'POST':
        picture = 'offset-labeled-blank.png'
        # Define a dictionary of degree multipliers and shrinkage rates
        degree = {'10': 1.75, '22.5': 1.41, '30': 1.15, '45': 1.0, '60': 0.87, '90': 0.71}
        shrinkage = {'1/2': 0.6, '3/4': 0.8, '1': 1.0, '1 1/4': 1.3, '1 1/2': 1.6, '2': 2.0, '2 1/2': 2.5, '3': 3.0, '3 1/2': 3.5, '4': 4.0}
        offset_angle = float(request.form['offset_angle'])
        offset_depth = float(request.form['offset_depth'])  # User-provided offset depth
        offset_width = float(request.form['offset_width'])  # User-provided offset width
        degree_multiplier = degree[str(offset_angle)]
        shrinkage_rate = shrinkage[str(offset_width)]
        offset_depth_rounded = round(offset_depth * degree_multiplier, 2)
        distance_between_bends = round(offset_depth_rounded * shrinkage_rate, 2)
        conduit_shrinkage = round(offset_depth_rounded - distance_between_bends, 2)
        offset_width_rounded = round(offset_width * degree_multiplier, 2)
        math = {'degree_multiplier': degree_multiplier, 'shrinkage_rate': shrinkage_rate, 'offset_depth_rounded': offset_depth_rounded,
                'distance_between_bends': distance_between_bends, 'conduit_shrinkage': conduit_shrinkage, 'offset_width_rounded': offset_width_rounded}
        return render_template('offset.html', picture=picture, offset_angle=degree, Fraction=Fraction,
                               offset_depth=offset_depth_rounded, distance_between_bends=distance_between_bends, conduit_shrinkage=conduit_shrinkage,
                               offset_width=offset_width_rounded, math=math)
    offset_depth_mixed = None
    return render_template('offset.html', picture=picture, math=math, offset_depth_mixed=offset_depth_mixed)

@app.route('/4-point-saddle', methods=['GET', 'POST'])
def four_point_saddle():
    picture='4-point-labeled-white-object.png'
    if request.method == 'POST':
        picture='4-point-labeled-white.png'
        # Define a dictionary of degree multipliers
        degree_multipliers = {
            10: 6,
            22.5: 2.6,
            30: 2.0,
            45: 1.4,
            60: 1.2
        }
        shrinkage_rates = {
            10: 1 / 16,
            15: 1 / 8,
            22.5: 3 / 16,
            30: 1 / 4,
            45: 3 / 8,
            60: 1 / 2
        }

        offset_angle = float(request.form['offset_angle'])
        distance_to_object = float(request.form['object_distance'])
        object_width = float(request.form['object_width'])  # User-provided offset width
        rise = float(request.form['rise'])  # User-provided offset depth


        # Get the selected degree from the form
        if offset_angle != 22.5:
            offset_angle = int(['offset_angle'])
        else:
            offset_angle = offset_angle      

        shrinkage = rise * math.tan(offset_angle)
        
        if offset_angle in degree_multipliers:
            rise_multiplier = degree_multipliers[offset_angle]
            distance = rise_multiplier * rise
        else:
            # Handle cases where the offset angle is not in the dictionary
            rise = None  # You can define a default value or handle it differently

        if offset_angle in shrinkage_rates:
            shrinkage_rate = shrinkage_rates[offset_angle]
            shrinkage = rise * shrinkage_rate
        else:
            # Handle cases where the offset angle is not in the dictionary
            shrinkage = None  # You can define a default value or handle it differently

        # Round decimal values to 1/8th inch increments and convert to mixed fractions
        distance_to_first_mark = (distance_to_object - distance) + shrinkage
        distance_to_first_mark_rounded = decimal_to_mixed_fraction(round_to_eighth(distance_to_first_mark))
        rise_rounded= decimal_to_mixed_fraction(round_to_eighth(rise))
        distance_rounded = decimal_to_mixed_fraction(round_to_eighth(distance))
        shrinkage_rounded = decimal_to_mixed_fraction(round_to_eighth(shrinkage))
        offset_width_rounded = decimal_to_mixed_fraction(round_to_eighth(object_width))
        degree = f"{offset_angle}°"
        return render_template('4-point-saddle.html', picture=picture, offset_angle=degree,
                               rise=rise_rounded, distance_between_bends=distance_rounded, conduit_shrinkage=shrinkage_rounded,
                               offset_width=offset_width_rounded, math=math, first_mark=distance_to_first_mark_rounded)
   
    return render_template('4-point-saddle.html', picture=picture)

if __name__ == '__main__':
    app.run(debug=True)