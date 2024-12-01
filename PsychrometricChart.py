"""
PsychrometricChart.py

This module creates psychrometric charts for HVAC and meteorological applications. 
A psychrometric chart is a graphical representation of the thermodynamic properties 
of moist air, helping visualize the relationships between:
- Dry-bulb temperature
- Wet-bulb temperature
- Relative humidity
- Humidity ratio
- Other air-water vapor mixture properties

The chart is generated in IP (Imperial) units at a user-specified ambient pressure,
with a default of 14.7 psi (standard atmospheric pressure at sea level).

Dependencies:
    - matplotlib: For creating the visualization
    - math: For mathematical calculations
    - typing: For type hints (Python 3.5+)
"""

from math import exp, pow, log
from typing import List, Tuple, Optional
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def ref_linesIP(p_atm: float, T_db_range: range) -> Tuple[List[List[float]], List[Tuple[List[float], List[float]]], List[Tuple[List[float], List[float]]]]:
    """
    Generate reference lines for the psychrometric chart in Imperial units.
    
    Args:
        p_atm: Atmospheric pressure in psi (pounds per square inch)
        T_db_range: Range of dry-bulb temperatures to plot in Fahrenheit
    
    Returns:
        Tuple containing:
        - phi_ref: List of humidity ratios for each relative humidity percentage
        - wb_ref: List of wet-bulb temperature reference line coordinates
        - db_ref: List of dry-bulb temperature reference line coordinates
    
    The function calculates:
        1. Relative humidity lines from 10% to 100% in 10% increments
        2. Wet-bulb temperature reference lines
        3. Dry-bulb temperature reference lines
    
    Calculations are based on ASHRAE 2009 Fundamentals equations.
    """
    phi_ref: List[List[float]] = []
    wb_ref: List[Tuple[List[float], List[float]]] = []
    db_ref: List[Tuple[List[float], List[float]]] = []

    # Create relative humidity reference lines from 10-100%, in increments of 10%
    for i, phi in enumerate(range(10, 101, 10)):
        phi_ref.append([])
        for j, T_db in enumerate(T_db_range):
            # Convert temperature to absolute scale (Rankine) by adding 459.67°F
            T_rankine = T_db + 459.67
            
            # Calculate saturation pressure (p_ws) over liquid water
            # Using ASHRAE 2009 Fundamentals, equation 6
            p_ws = exp(
                -1.0440397E4/T_rankine  # Temperature dependent term
                -1.1294650E1            # Constant term
                -2.7022355E-2*T_rankine # Linear term
                +1.2890360E-5*pow(T_rankine, 2)  # Quadratic term
                -2.4780681E-9*pow(T_rankine, 3)  # Cubic term
                +6.5459673*log(T_rankine)        # Logarithmic term
            )
            
            # Calculate water vapor partial pressure (p_w) at given relative humidity
            p_w = phi/100.0 * p_ws
            
            # Calculate humidity ratio (mass of water vapor per mass of dry air)
            # 0.621945 is the ratio of molecular weight of water to molecular weight of air
            W = 0.621945 * p_w/(p_atm - p_w)
            phi_ref[i].append(W)
            
            # At saturation (100% RH), find reference line endpoints for plotting
            if phi == 100 and round(T_db/10) == float(T_db)/10:
                # Calculate wet-bulb temperature at zero humidity
                # Using ASHRAE 2009 Fundamentals, equation 35
                T_wbo = (1093.0 - 0.556*T_db) * phi_ref[i][j]/0.24 + T_db
                
                # Store coordinates for wet-bulb and dry-bulb reference lines
                wb_ref.append(([T_db, T_wbo], [phi_ref[i][j], 0]))
                db_ref.append(([T_db, T_db], [phi_ref[i][j], 0]))
    
    return phi_ref, wb_ref, db_ref

def ref_linesSI(p_atm: float, T_db_range: range) -> None:
    """
    Placeholder for generating reference lines in SI units (metric system).
    
    This function will be implemented in future versions to support:
    - Temperatures in Celsius
    - Pressures in kilopascals (kPa)
    - Humidity ratios in kg water vapor per kg dry air
    
    Args:
        p_atm: Atmospheric pressure in kPa
        T_db_range: Range of dry-bulb temperatures in Celsius
    
    Returns:
        None (placeholder)
    """
    return

def humidity_ratio(p: float, T_db: float, phi: float) -> float:
    """
    Calculate the humidity ratio (W) for given conditions.
    
    Args:
        p: Atmospheric pressure in psi
        T_db: Dry-bulb temperature in Fahrenheit
        phi: Relative humidity percentage (0-100)
    
    Returns:
        Humidity ratio in lb water vapor per lb dry air
    
    The humidity ratio represents the mass of water vapor present per unit mass
    of dry air at the specified conditions.
    """
    # Calculate saturation pressure using ASHRAE 2009 equation
    p_ws = exp(-1.0440397E4/(T_db + 459.67) - 1.1294650E1 - 
               2.7022355E-2*(T_db + 459.67) + 
               1.2890360E-5*pow(T_db + 459.67, 2) - 
               2.4780681E-9*pow(T_db + 459.67, 3) + 
               6.5459673*log(T_db + 459.67))
    
    # Calculate actual water vapor pressure at given relative humidity
    p_w = phi/100.0 * p_ws
    
    # Calculate and return humidity ratio
    W = 0.621945 * p_w/(p - p_w)
    return W

def main() -> None:
    """
    Main function to create and display the psychrometric chart.
    
    This function:
    1. Sets up the chart parameters (units, pressure, state point)
    2. Generates the reference lines
    3. Creates the visualization using matplotlib
    4. Displays the chart with proper labels and formatting
    """
    # Set default parameters (can be modified for user input)
    units = 'IP'  # Imperial units
    set_point = 'y'  # Include a state point on the chart
    
    # Create the matplotlib figure and axis
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    if units == 'IP':
        # Set up Imperial units parameters
        p_atm_input = 14.7  # Standard atmospheric pressure in psi
        
        # Define state point if requested
        if set_point == 'y':
            st_point_Tdb = 75   # State point dry-bulb temperature (°F)
            st_point_rh = 45    # State point relative humidity (%)
            st_point_W = humidity_ratio(p_atm_input, st_point_Tdb, st_point_rh)
        
        # Generate chart data
        T_db_range = range(32, 111)  # Temperature range from freezing to 110°F
        phi_ref, wb_ref, db_ref = ref_linesIP(float(p_atm_input), T_db_range)
        
        # Set axis labels for Imperial units
        plt.xlabel('Dry Bulb Temperature (°F)')
        plt.ylabel('Humidity Ratio (lb_w/lb_da)')
    
    if units == 'SI':
        # Set up SI units parameters (placeholder)
        p_atm_input = 101.325  # Standard atmospheric pressure in kPa
        
        if set_point == 'y':
            st_point_Tdb = 25   # State point dry-bulb temperature (°C)
            st_point_rh = 45    # State point relative humidity (%)
            st_point_W = humidity_ratio(p_atm_input, st_point_Tdb, st_point_rh)
        
        T_db_range = range(0, 51)  # Temperature range 0-50°C
        phi_ref, wb_ref, db_ref = ref_linesSI(float(p_atm_input), T_db_range)
        
        # Set axis labels for SI units
        plt.xlabel('Dry Bulb Temperature (°C)')
        plt.ylabel('Humidity Ratio (kg_w/kg_da)')
    
    # Plot relative humidity lines
    for i in range(0, len(phi_ref)):
        plt.plot(T_db_range, phi_ref[i], 'b')
    
    # Plot wet-bulb temperature reference lines
    for i in range(0, len(wb_ref)):
        plt.plot(wb_ref[i][0], wb_ref[i][1], 'b:')
    
    # Plot dry-bulb temperature reference lines
    for i in range(0, len(db_ref)):
        plt.plot(db_ref[i][0], db_ref[i][1], 'b:')
    
    # Plot state point if requested
    if set_point == 'y':
        plt.scatter(st_point_Tdb, st_point_W, color='r')
    
    # Configure axis formatting
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))  # Minor tick every 1°
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.001))  # Minor tick every 0.001
    plt.xlim(min(T_db_range), max(T_db_range))
    plt.ylim(0, 0.03)  # Set humidity ratio range
    
    # Display the chart
    plt.show()

if __name__ == '__main__':
    main()