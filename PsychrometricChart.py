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
"""

import numpy as np
from typing import Tuple, List, Union
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def calculate_saturation_pressure(
    temp_rankine: Union[float, np.ndarray]
) -> Union[float, np.ndarray]:
    """
    Calculate the saturation pressure of water vapor using ASHRAE 2009 Fundamentals equation.

    The equation uses six coefficients (C1-C6) from ASHRAE 2009 Fundamentals, equation 6:
    P_ws = exp(C1/T + C2 + C3*T + C4*T^2 + C5*T^3 + C6*ln(T))
    where T is absolute temperature in Rankine and P_ws is saturation pressure in psi.

    Args:
        temp_rankine: Temperature in Rankine (°F + 459.67). Can be a single value or numpy array.

    Returns:
        Saturation pressure in psi (pounds per square inch)
    """
    # ASHRAE 2009 Fundamentals coefficients for saturation pressure calculation
    C1 = -1.0440397e4  # Temperature inverse term
    C2 = -1.1294650e1  # Constant term
    C3 = -2.7022355e-2  # Linear term T
    C4 = 1.2890360e-5  # Quadratic term T^2
    C5 = -2.4780681e-9  # Cubic term T^3
    C6 = 6.5459673  # Logarithmic term ln(T)

    # Vectorized calculation of saturation pressure using ASHRAE equation
    return np.exp(
        C1 / temp_rankine
        + C2
        + C3 * temp_rankine
        + C4 * np.power(temp_rankine, 2)
        + C5 * np.power(temp_rankine, 3)
        + C6 * np.log(temp_rankine)
    )


def generate_chart_reference_lines_imperial(
    atmospheric_pressure: float, drybulb_temps: np.ndarray
) -> Tuple[
    List[np.ndarray], List[Tuple[List[float], List[float]]], List[Tuple[List[float], List[float]]]
]:
    """
    Generate reference lines for the psychrometric chart in Imperial units.

    Args:
        atmospheric_pressure: Atmospheric pressure in psi (pounds per square inch)
        drybulb_temps: Array of dry-bulb temperatures to plot in Fahrenheit

    Returns:
        Tuple containing:
        - relative_humidity_lines: List of humidity ratio arrays for each RH percentage
        - wetbulb_reference_lines: List of wet-bulb temperature reference line coordinates
        - drybulb_reference_lines: List of dry-bulb temperature reference line coordinates
    """
    # Initialize storage for reference lines
    relative_humidity_lines = []
    wetbulb_reference_lines = []
    drybulb_reference_lines = []

    # Convert temperature array to Rankine scale for calculations
    temp_rankine = drybulb_temps + 459.67

    # Calculate saturation pressure for all temperatures at once
    saturation_pressure = calculate_saturation_pressure(temp_rankine)

    # Create relative humidity reference lines (10% to 100%)
    for relative_humidity_percent in range(10, 101, 10):
        # Calculate water vapor partial pressure at given relative humidity
        vapor_pressure = relative_humidity_percent / 100.0 * saturation_pressure

        # Calculate humidity ratio array for this relative humidity
        # 0.621945 is the ratio of molecular weight of water vapor to dry air
        humidity_ratio = 0.621945 * vapor_pressure / (atmospheric_pressure - vapor_pressure)
        relative_humidity_lines.append(humidity_ratio)

        # At saturation (100% RH), calculate reference line endpoints
        if relative_humidity_percent == 100:
            # Get indices for temperatures at 10°F intervals
            reference_temp_indices = np.where(np.mod(drybulb_temps, 10) == 0)[0]

            for index in reference_temp_indices:
                current_drybulb = drybulb_temps[index]

                # Calculate wet-bulb temperature at zero humidity
                # Using ASHRAE 2009 Fundamentals, equation 35
                # Constants: 1093.0 and 0.556 are empirical coefficients
                # 0.24 is the specific heat of air at constant pressure
                wetbulb_temp_zero_humidity = (1093.0 - 0.556 * current_drybulb) * humidity_ratio[
                    index
                ] / 0.24 + current_drybulb

                # Store reference line coordinates
                wetbulb_reference_lines.append(
                    ([current_drybulb, wetbulb_temp_zero_humidity], [humidity_ratio[index], 0])
                )
                drybulb_reference_lines.append(
                    ([current_drybulb, current_drybulb], [humidity_ratio[index], 0])
                )

    return relative_humidity_lines, wetbulb_reference_lines, drybulb_reference_lines


def generate_chart_reference_lines_metric(
    atmospheric_pressure_kpa: float, drybulb_temps_celsius: np.ndarray
) -> None:
    """
    Placeholder for generating reference lines in SI units (metric system).

    This function will be implemented in future versions to support:
    - Temperatures in Celsius
    - Pressures in kilopascals (kPa)
    - Humidity ratios in kg water vapor per kg dry air

    Args:
        atmospheric_pressure_kpa: Atmospheric pressure in kPa
        drybulb_temps_celsius: Array of dry-bulb temperatures in Celsius

    Returns:
        None (placeholder)
    """
    return


def calculate_humidity_ratio(
    atmospheric_pressure: float, drybulb_temp: float, relative_humidity_percent: float
) -> float:
    """
    Calculate the humidity ratio (moisture content) for given conditions.

    Args:
        atmospheric_pressure: Atmospheric pressure in psi
        drybulb_temp: Dry-bulb temperature in Fahrenheit
        relative_humidity_percent: Relative humidity percentage (0-100)

    Returns:
        Humidity ratio in lb water vapor per lb dry air
    """
    # Calculate saturation pressure at the given temperature
    saturation_pressure = calculate_saturation_pressure(drybulb_temp + 459.67)

    # Calculate actual water vapor pressure at the given relative humidity
    vapor_pressure = relative_humidity_percent / 100.0 * saturation_pressure

    # Calculate and return humidity ratio
    # 0.621945 is the ratio of molecular weight of water vapor to dry air
    return 0.621945 * vapor_pressure / (atmospheric_pressure - vapor_pressure)


def main() -> None:
    """
    Main function to create and display the psychrometric chart.
    """
    # Chart configuration
    units_system = "IP"  # 'IP' for Imperial, 'SI' for metric
    include_state_point = True

    # Create the matplotlib figure and axis
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)

    if units_system == "IP":
        # Standard atmospheric pressure at sea level (psi)
        atmospheric_pressure = 14.7

        # Define example state point conditions
        if include_state_point:
            state_point_drybulb = 75.0  # °F
            state_point_humidity = 45.0  # %RH
            state_point_moisture = calculate_humidity_ratio(
                atmospheric_pressure, state_point_drybulb, state_point_humidity
            )

        # Generate chart data using numpy array for temperature range
        drybulb_temps = np.arange(32, 111)  # °F (freezing to 110°F)
        relative_humidity_lines, wetbulb_lines, drybulb_lines = (
            generate_chart_reference_lines_imperial(atmospheric_pressure, drybulb_temps)
        )

        # Set axis labels for Imperial units
        plt.xlabel("Dry-Bulb Temperature (°F)")
        plt.ylabel("Humidity Ratio (lb_water/lb_dry_air)")

    elif units_system == "SI":
        # Standard atmospheric pressure at sea level (kPa)
        atmospheric_pressure = 101.325

        if include_state_point:
            state_point_drybulb = 25.0  # °C
            state_point_humidity = 45.0  # %RH
            state_point_moisture = calculate_humidity_ratio(
                atmospheric_pressure, state_point_drybulb, state_point_humidity
            )

        # Generate chart data (temperature range 0-50°C)
        drybulb_temps = np.arange(0, 51)
        relative_humidity_lines, wetbulb_lines, drybulb_lines = (
            generate_chart_reference_lines_metric(atmospheric_pressure, drybulb_temps)
        )

        # Set axis labels for SI units
        plt.xlabel("Dry-Bulb Temperature (°C)")
        plt.ylabel("Humidity Ratio (kg_water/kg_dry_air)")

    # Plot relative humidity lines with improved formatting
    for line_index, humidity_ratios in enumerate(relative_humidity_lines):
        relative_humidity = (line_index + 1) * 10
        plt.plot(
            drybulb_temps,
            humidity_ratios,
            "b",
            alpha=0.7,
            label=f"{relative_humidity}% RH" if line_index == 0 else None,
        )

    # Plot wet-bulb and dry-bulb reference lines
    for wetbulb_line in wetbulb_lines:
        plt.plot(wetbulb_line[0], wetbulb_line[1], "b:", alpha=0.5)

    for drybulb_line in drybulb_lines:
        plt.plot(drybulb_line[0], drybulb_line[1], "b:", alpha=0.5)

    # Plot state point if requested
    if include_state_point:
        plt.scatter(
            state_point_drybulb,
            state_point_moisture,
            color="r",
            s=50,
            label=f'State Point ({state_point_drybulb}°{"F" if units_system == "IP" else "C"}, '
            f"{state_point_humidity}% RH)",
        )

    # Configure axis formatting and appearance
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.001))
    plt.xlim(min(drybulb_temps), max(drybulb_temps))
    plt.ylim(0, 0.03)

    # Add grid and legend for better readability
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Add title with pressure information
    pressure_units = "psi" if units_system == "IP" else "kPa"
    plt.title(f"Psychrometric Chart (P = {atmospheric_pressure} {pressure_units})", pad=20)

    # Display the chart
    plt.show()


if __name__ == "__main__":
    main()
