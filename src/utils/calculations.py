import numpy as np


def calculate_saturation_pressure(temp_rankine: float | np.ndarray) -> float | np.ndarray:
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
