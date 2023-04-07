import os
import base64
import io

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.cache import cache

import uuid
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

def plot_wall(**kwargs):

    #Unwrapped kwargs from **wall_properties
    height = kwargs.get("height")
    top_breadth = kwargs.get("top_breadth")
    base_breadth = kwargs.get("base_breadth")
    passive_soil_height = kwargs.get("passive_soil_height")
    water_table = kwargs.get("water_table")


    #Unwrapped kwargs from **stability_results
    weight = kwargs.get("weight")
    active_soil_pressure = kwargs.get("active_soil_pressure")
    passive_soil_pressure = kwargs.get("passive_soil_pressure")
    lateral_surcharge = kwargs.get("lateral_surcharge")
    lateral_water = kwargs.get("lateral_water")
    base_friction_force = kwargs.get("base_friction_force")

    fig, ax = plt.subplots(dpi=80)
    wall_polygon = plt.Polygon([[0, 0], [base_breadth, 0], [top_breadth, height], [0, height]], closed=True)
    ax.add_patch(wall_polygon)

    # Arrow scaling factors
    arrow_scale = 0.05
    head_width_scale = 0.1
    head_length_scale = 0.1

    gamma_soil = 18

     # Add active earth pressure triangle
    active_x_loc = base_breadth + 0.5
    active_pressure_triangle = plt.Polygon([[active_x_loc, 0], [active_x_loc, height], [active_x_loc + active_soil_pressure / gamma_soil, 0]], closed=True, alpha=0.3, color='blue', linestyle='--', fill=False)
    ax.add_patch(active_pressure_triangle)

    # Add passive earth pressure triangle
    passive_triangle_height = passive_soil_height - 0.3
    passive_pressure_triangle = plt.Polygon([[0, 0], [-passive_soil_pressure / gamma_soil, 0], [0, passive_triangle_height]], closed=True, alpha=0.3, color='red', linestyle='--', fill=False)
    ax.add_patch(passive_pressure_triangle)

    # Add surcharge pressure
    surcharge_x_loc = active_x_loc + active_soil_pressure / gamma_soil + 1
    surcharge_pressure = plt.Polygon([[surcharge_x_loc, 0], [surcharge_x_loc, height], [surcharge_x_loc + lateral_surcharge / gamma_soil, height], [surcharge_x_loc + lateral_surcharge / gamma_soil, 0]], closed=True, alpha=0.3, color='blue', linestyle='--', fill=False)
    ax.add_patch(surcharge_pressure)

     # Add water pressure triangle
    water_x_loc = surcharge_x_loc + lateral_surcharge/gamma_soil + 1
    water_pressure_triangle = plt.Polygon([[water_x_loc, 0], [water_x_loc, water_table], [water_x_loc + lateral_water / gamma_soil, 0]], closed=True, alpha=0.3, color='blue', linestyle='--', fill=False)
    ax.add_patch(water_pressure_triangle)

    # Add force arrows
    ax.arrow(base_breadth/2, height/2, 0, -weight * arrow_scale/4, head_width=head_width_scale, head_length=head_length_scale, fc='red', ec='red')
    ax.arrow(active_x_loc + active_soil_pressure * arrow_scale + head_length_scale, height / 3, -active_soil_pressure * arrow_scale, 0, head_width=head_width_scale, head_length=head_length_scale, fc='blue', ec='blue')
    if passive_soil_pressure:
        ax.arrow(0 - passive_soil_pressure * arrow_scale - head_length_scale, passive_triangle_height / 3, passive_soil_pressure * arrow_scale, 0, head_width=head_width_scale, head_length=head_length_scale, fc='red', ec='red')
    if lateral_surcharge:
        ax.arrow(surcharge_x_loc + lateral_surcharge*arrow_scale + head_length_scale, height / 2, -lateral_surcharge * arrow_scale, 0, head_width=head_width_scale, head_length=head_length_scale, fc='blue', ec='blue')
    if lateral_water:
        ax.arrow(water_x_loc + lateral_water * arrow_scale + head_length_scale, water_table / 3, -lateral_water * arrow_scale, 0, head_width=head_width_scale, head_length=head_length_scale, fc='blue', ec='blue')

    ax.arrow(base_breadth/2, 0.05, base_friction_force * arrow_scale/4, 0, head_width=head_width_scale/2, head_length=head_length_scale, fc='red', ec='red')

    # Add force labels
    ax.text(base_breadth/2, height/2 - weight * arrow_scale/4 - head_length_scale, f"{weight:.2f} kN/m", color='red', fontsize=8, ha='center', va='center')
    ax.text(active_x_loc + active_soil_pressure * arrow_scale + head_length_scale, height / 3 + 0.1, f"{active_soil_pressure:.2f} kN/m", color='blue', fontsize=8, ha='center', va='center')
    if passive_soil_pressure:
        ax.text(-passive_soil_pressure * arrow_scale - head_length_scale, passive_triangle_height/3 + 0.1, f"{passive_soil_pressure:.2f} kN/m", color='red', fontsize=8, ha='center', va='center')
    if lateral_surcharge:
        ax.text(surcharge_x_loc + lateral_surcharge * arrow_scale + head_length_scale, height/2 + 0.1, f"{lateral_surcharge:.2f} kN/m", color='blue', fontsize=8, ha='center', va='center')
    if lateral_water:
        ax.text(water_x_loc + lateral_water * arrow_scale + head_length_scale, water_table/3 + 0.1, f"{lateral_water:.2f} kN/m", color='blue', fontsize=8, ha='center', va='center')

    ax.text(base_breadth/2, -0.1, f"{base_friction_force:.2f} kN/m", color='red', fontsize=8, ha='center', va='center')

    # Define x bound
    if (lateral_surcharge == 0 and lateral_water == 0):
        x_max = active_x_loc + active_soil_pressure * arrow_scale + head_length_scale + 0.5
    elif lateral_water == 0:
        x_max = surcharge_x_loc + lateral_surcharge * arrow_scale + head_length_scale + 0.5
    else:
        x_max = water_x_loc + lateral_water * arrow_scale + head_length_scale + 1
    x_min = -passive_soil_pressure*arrow_scale - head_length_scale - 0.5

    # Add active soil polygon
    soil_polygon = plt.Polygon([[base_breadth, 0], [top_breadth, height], [x_max, height], [x_max, 0]], closed=True, alpha=0.5, zorder=0, color='brown')
    ax.add_patch(soil_polygon)

    # Add passive soil polygon
    passive_soil_polygon = plt.Polygon([[x_min, 0], [0, 0], [0, passive_soil_height], [x_min, passive_soil_height]], closed=True, alpha=0.5, zorder=0, color='green')
    ax.add_patch(passive_soil_polygon)

    # Add force name labels
    ax.text(active_x_loc, height + 0.1, f"Active Soil", color='blue', fontsize=8, ha='center', va='center')
    if passive_soil_pressure:
        ax.text(0, passive_soil_height + 0.1, f"Passive Soil", color='red', fontsize=8, ha='right', va='center')
    if lateral_surcharge:
        ax.text(surcharge_x_loc, height + 0.1, f"Surcharge", color='blue', fontsize=8, ha='center', va='center')
    if lateral_water:
        ax.text(water_x_loc, height + 0.1, f"Water", color='blue', fontsize=8, ha='left', va='center')


    # Set plot limits and labels
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(0, 1.2 * height)
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Height (m)")
    ax.set_title("Retaining Wall, Soil, and Forces")
    ax.set_aspect("equal")

    # Save the plot as an image in cache
    # Create a buffer to save the image data
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)

    # Close the figure to prevent memory leaks
    plt.close(fig)

    # Generate a unique cache key and store the image data in the cache
    cache_key = f"wall_plot_{uuid.uuid4().hex}"
    image_data = base64.b64encode(buffer.getvalue()).decode()
    cache.set(cache_key, image_data, timeout=1000)  # Set a timeout, e.g., 5 minutes (300 seconds)

    return cache_key

