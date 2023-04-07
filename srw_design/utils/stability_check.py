def stability_check(mu=0.5, **kwargs):

    #Unwrapped **kwargs
    height = kwargs.get("height")    
    top_breadth = kwargs.get("top_breadth")    
    base_breadth = kwargs.get("base_breadth")    
    Ka = kwargs.get("Ka")    
    gamma_soil = kwargs.get("gamma_soil")    
    gamma_stone = kwargs.get("gamma_stone")    
    passive_soil_height = kwargs.get("passive_soil_height")    
    surcharge = kwargs.get("surcharge")    
    water_table = kwargs.get("water_table")    
    Kp = kwargs.get("Kp")


    # Calculate geometry and weight parameters
    area = 0.5 * (top_breadth + base_breadth) * height
    weight = area * gamma_stone

    # Calculate moment arm for weight
    centroid_x = (2 * base_breadth + top_breadth) / 3 / (base_breadth + top_breadth)
    moment_arm_weight = height - centroid_x

    # Calculate soil pressure
    active_soil_pressure = 0.5 * gamma_soil * height**2 * Ka
    effective_passive_soil_height = max(0, passive_soil_height - 0.3)
    passive_soil_pressure = 0.5 * gamma_soil * effective_passive_soil_height**2 * Kp

    # Calcuate surcharge
    lateral_surcharge = Ka * surcharge

    # Calculate water pressure
    lateral_water = 10 * water_table

    # Calculate moment arm for soil pressure
    moment_arm_active_soil_pressure = height / 3
    moment_arm_passive_soil_pressure = effective_passive_soil_height / 3
    moment_arm_surcharge = height / 2
    moment_arm_water = water_table / 3 

    # Calculate moments
    moment_stone = weight * moment_arm_weight
    moment_active_soil = active_soil_pressure * moment_arm_active_soil_pressure
    moment_passive_soil = passive_soil_pressure * moment_arm_passive_soil_pressure
    moment_surcharge = lateral_surcharge * moment_arm_surcharge
    moment_water = lateral_water * moment_arm_water

    # Check overturning stability
    stability_factor_overturning =  (moment_stone + moment_passive_soil) / ((moment_active_soil + moment_surcharge + moment_water))

    # Check sliding stability
    base_friction_force = mu * weight
    sliding_force = active_soil_pressure + lateral_surcharge + lateral_water
    stability_factor_sliding =  (base_friction_force + passive_soil_pressure) / sliding_force

    return {"stability_factor_overturning": stability_factor_overturning, 
            "stability_factor_sliding":stability_factor_sliding, 
            "weight":weight, 
            "active_soil_pressure":active_soil_pressure, 
            "passive_soil_pressure":passive_soil_pressure, 
            "lateral_surcharge":lateral_surcharge, 
            "lateral_water":lateral_water, 
            "base_friction_force":base_friction_force,
            }
