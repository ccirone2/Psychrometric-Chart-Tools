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
    - numpy: For efficient numerical computations and array operations
    - matplotlib: For creating the visualization
    - typing: For type hints (Python 3.5+)

The code uses vectorized operations through NumPy for improved performance
compared to iterative calculations.
"""

import numpy as np
from typing import Tuple, List, Union, Optional
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def calculate_saturation_pressure(T_rankine: np.ndarray) -> np.ndarray:
    """
    Calculate the saturation pressure of water vapor using vectorized operations.
    
    Args:
        T_rankine: Temperature in Rankine (°F + 459.67)
    
    Returns:
        Array of saturation pressures in psi
    
    Uses ASHRAE 2009 Fundamentals, equation 6, vectorized for efficiency.
    """
    return np.exp(
        -1.0440397E4/T_rankine     # Temperature dependent term
        - 1.1294650E1              # Constant term
        - 2.7022355E-2*T_rankine   # Linear term
        + 1.2890360E-5*T_rankine**2  # Quadratic term
        - 2.4780681E-9*T_rankine**3  # Cubic term
        + 6.5459673*np.log(T_rankine)  # Logarithmic term
    )

def ref_linesIP(p_atm: float, T_db_range: np.ndarray) -> Tuple[List[np.ndarray], List[Tuple[List[float], List[float]]], List[Tuple[List[float], List[float]]]]:
    """
    Generate reference lines for the psychrometric chart in Imperial units using vectorized operations.
    
    Args:
        p_atm: Atmospheric pressure in psi (pounds per square inch)
        T_db_range: Array of dry-bulb temperatures to plot in Fahrenheit
    
    Returns:
        Tuple containing:
        - phi_ref: List of humidity ratio arrays for each relative humidity percentage
        - wb_ref: List of wet-bulb temperature reference line coordinates
        - db_ref: List of dry-bulb temperature reference line coordinates
    
    The function uses NumPy's vectorized operations for efficient calculation of:
        1. Relative humidity lines from 10% to 100% in 10% increments
        2. Wet-bulb temperature reference lines
        3. Dry-bulb temperature reference lines
    """
    # Initialize lists to store results
    phi_ref = []
    wb_ref = []
    db_ref = []
    
    # Convert temperature range to Rankine once for all calculations
    T_rankine = T_db_range + 459.67
    
    # Calculate saturation pressure for all temperatures at once
    p_ws = calculate_saturation_pressure(T_rankine)
    
    # Create relative humidity reference lines from 10-100%, in increments of 10%
    for phi in range(10, 101, 10):
        # Vectorized calculation of water vapor pressure
        p_w = phi/100.0 * p_ws
        
        # Vectorized calculation of humidity ratio
        W = 0.621945 * p_w/(p_atm - p_w)
        phi_ref.append(W)
        
        # At saturation conditions, calculate reference line endpoints
        if phi == 100:
            # Find points where temperature is a multiple of 10
            temp_indices = np.where(T_db_range % 10 == 0)[0]
            
            for idx in temp_indices:
                T_db = T_db_range[idx]
                # Calculate wet-bulb temperature at zero humidity using vectorized operations
                T_wbo = (1093.0 - 0.556*T_db) * W[idx]/0.24 + T_db
                
                # Store coordinates for reference lines
                wb_ref.append(([T_db, T_wbo], [W[idx], 0]))
                db_ref.append(([T_db, T_db], [W[idx], 0]))
    
    return phi_ref, wb_ref, db_ref

def ref_linesSI(p_atm: float, T_db_range: np.ndarray) -> None:
    """
    Placeholder for generating reference lines in SI units (metric system).
    
    This function will be implemented in future versions to support:
    - Temperatures in Celsius
    - Pressures in kilopascals (kPa)
    - Humidity ratios in kg water vapor per kg dry air
    
    The implementation will use NumPy for vectorized calculations.
    """
    return

def humidity_ratio(p: float, T_db: Union[float, np.ndarray], phi: float) -> Union[float, np.ndarray]:
    """
    Calculate the humidity ratio (W) for given conditions using vectorized operations.
    
    Args:
        p: Atmospheric pressure in psi
        T_db: Dry-bulb temperature(s) in Fahrenheit (scalar or array)
        phi: Relative humidity percentage (0-100)
    
    Returns:
        Humidity ratio in lb water vapor per lb dry air (scalar or array)
    """
    # Convert temperature to Rankine
    T_rankine = T_db + 459.67
    
    # Calculate saturation pressure using vectorized operations
    p_ws = calculate_saturation_pressure(T_rankine)
    
    # Calculate water vapor pressure and humidity ratio
    p_w = phi/100.0 * p_ws
    return 0.621945 * p_w/(p - p_w)

def main() -> None:
    """
    Main function to create and display the psychrometric chart.
    
    This function uses NumPy arrays for efficient data handling and
    matplotlib for visualization. All calculations are vectorized
    for improved performance.
    """
    # Set default parameters
    units = 'IP'  # Imperial units
    set_point = 'y'  # Include a state point on the chart
    
    # Create the matplotlib figure and axis
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    if units == 'IP':
        # Set up Imperial units parameters
        p_atm_input = 14.7  # Standard atmospheric pressure in psi
        
        # Create temperature range array using NumPy
        T_db_range = np.arange(32, 111)  # Temperature range from freezing to 110°F
        
        # Define state point if requested
        if set_point == 'y':
            st_point_Tdb = 75   # State point dry-bulb temperature (°F)
            st_point_rh = 45    # State point relative humidity (%)
            st_point_W = humidity_ratio(p_atm_input, st_point_Tdb, st_point_rh)
        
        # Generate chart data using vectorized calculations
        phi_ref, wb_ref, db_ref = ref_linesIP(float(p_atm_input), T_db_range)
        
        # Set axis labels for Imperial units
        plt.xlabel('Dry Bulb Temperature (°F)')
        plt.ylabel('Humidity Ratio (lb_w/lb_da)')
    
    elif units == 'SI':
        # Set up SI units parameters (placeholder)
        p_atm_input = 101.325  # Standard atmospheric pressure in kPa
        
        # Create temperature range array using NumPy
        T_db_range = np.arange(0, 51)  # Temperature range 0-50°C
        
        if set_point == 'y':
            st_point_Tdb = 25   # State point dry-bulb temperature (°C)
            st_point_rh = 45    # State point relative humidity (%)
            st_point_W = humidity_ratio(p_atm_input, st_point_Tdb, st_point_rh)
        
        phi_ref, wb_ref, db_ref = ref_linesSI(float(p_atm_input), T_db_range)
        
        # Set axis labels for SI units
        plt.xlabel('Dry Bulb Temperature (°C)')
        plt.ylabel('Humidity Ratio (kg_w/kg_da)')
    
    # Plot relative humidity lines using vectorized data
    for i, w_values in enumerate(phi_ref):
        plt.plot(T_db_range, w_values, 'b')
    
    # Plot wet-bulb and dry-bulb reference lines
    for wb in wb_ref:
        plt.plot(wb[0], wb[1], 'b:')
    
    for db in db_ref:
        plt.plot(db[0], db[1], 'b:')
    
    # Plot state point if requested
    if set_point == 'y':
        plt.scatter(st_point_Tdb, st_point_W, color='r')
    
    # Configure axis formatting
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))  # Minor tick every 1°
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.001))  # Minor tick every 0.001
    plt.xlim(T_db_range[0], T_db_range[-1])
    plt.ylim(0, 0.03)  # Set humidity ratio range
    
    # Display the chart
    plt.show()

if __name__ == '__main__':
    main()