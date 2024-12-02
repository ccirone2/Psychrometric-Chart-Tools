"""
PsychrometricChart.py

This module creates psychrometric charts for HVAC and meteorological applications.
"""

import numpy as np
from typing import Tuple, List, Union, NamedTuple, Literal
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# Constants
MOLECULAR_WEIGHT_RATIO_OF_WATER_VAPOR_TO_DRY_AIR: float = 0.621945


class ReferenceLine(NamedTuple):
    constant: int | float  # constant value
    x_vals: np.ndarray | List[float]  # x values
    y_vals: np.ndarray | List[float]  # y values


class StatePoint:

    def __init__(
        self,
        drybulb: float = 30,
        relative_humidity: float = 20,
        pressure: float = 14.7,
    ):
        self.drybulb = drybulb
        self.relative_humidity = relative_humidity
        self.atmospheric_pressure = pressure
        self.humidity_ratio = self.calculate_humidity_ratio()

    def calculate_humidity_ratio(self) -> float:
        """Calculate the humidity ratio of air given the dry-bulb temperature and relative humidity."""
        saturation_pressure = calculate_saturation_pressure(self.drybulb + 459.67)

        vapor_pressure = self.relative_humidity / 100.0 * saturation_pressure

        return (
            MOLECULAR_WEIGHT_RATIO_OF_WATER_VAPOR_TO_DRY_AIR
            * vapor_pressure
            / (self.atmospheric_pressure - vapor_pressure)
        )


class PsychrometricChart:
    def __init__(
        self,
        unit_system: Literal["metric", "standard"] = "standard",
        pressure: float = None,
    ):
        self.unit_system = unit_system.lower()
        self.pressure = pressure
        self.state_points = []

        # Initialize plot
        self.style = ChartStyle(self)
        self.fig, self.ax = self.style.create_figure()

    def add_state_point(self, state_point: StatePoint | List[StatePoint]) -> None:
        """Add a state point to the chart"""
        if isinstance(state_point, list):
            self.state_points.extend(state_point)
        else:
            self.state_points.append(state_point)

    def _plot_reference_lines(self, relative_humidity_lines, reference_lines) -> None:
        self.style.plot_humidity_lines(self.ax, relative_humidity_lines)
        self.style.plot_reference_lines(self.ax, reference_lines)

    def _generate_reference_lines(
        self,
    ) -> Tuple[List[ReferenceLine], List[ReferenceLine]]:
        relative_humidity_lines = []
        reference_lines = []

        """Generate METRIC reference lines for the psychrometric chart."""
        if self.unit_system == "metric":
            return [], []  # Placeholder for metric implementation

        """Generate IMPERIAL reference lines for the psychrometric chart."""
        drybulb_temp_rankine = self.style.temp_range + 459.67
        saturation_pressure = calculate_saturation_pressure(drybulb_temp_rankine)

        relative_humidity_reference_lines = range(10, 101, 10)
        for relative_humidity_percent in relative_humidity_reference_lines:
            vapor_pressure = relative_humidity_percent / 100.0 * saturation_pressure
            humidity_ratio = (
                MOLECULAR_WEIGHT_RATIO_OF_WATER_VAPOR_TO_DRY_AIR
                * vapor_pressure
                / (self.pressure - vapor_pressure)
            )
            relative_humidity_lines.append(
                ReferenceLine(relative_humidity_percent, self.style.temp_range, humidity_ratio)
            )

            if relative_humidity_percent != 100:
                continue

            temp_interval = 5
            is_multiple_of_ten = np.mod(self.style.temp_range, temp_interval) == 0
            reference_temp_indices = np.where(is_multiple_of_ten)[0]

            for index in reference_temp_indices:
                current_drybulb = self.style.temp_range[index]
                current_humidity_ratio = humidity_ratio[index]

                wetbulb_temp_zero_humidity = (
                    1093.0 - 0.556 * current_drybulb
                ) * current_humidity_ratio / 0.24 + current_drybulb

                # Add wetbulb reference line
                reference_lines.append(
                    ReferenceLine(
                        wetbulb_temp_zero_humidity,
                        [current_drybulb, wetbulb_temp_zero_humidity],
                        [current_humidity_ratio, 0],
                    )
                )

                # Add drybulb reference line
                reference_lines.append(
                    ReferenceLine(
                        current_drybulb,
                        [current_drybulb, current_drybulb],
                        [current_humidity_ratio, 0],
                    )
                )

        return relative_humidity_lines, reference_lines

    def generate(self) -> None:
        ref_lines = self._generate_reference_lines()
        self._plot_reference_lines(*ref_lines)

        if self.state_points:
            self.style.plot_state_points(self.ax, self.state_points)

        self.style.configure_chart(self.ax)
        plt.show()


class ChartStyle:
    """Encapsulates all chart styling and format settings"""

    def __init__(self, chart: "PsychrometricChart"):
        self.unit_system = chart.unit_system
        self.display_pressure = chart.pressure

        if self.unit_system == "metric":
            self.temp_range = np.arange(0, 51)
            self.temp_unit = "°C"
            self.pressure_unit = "kPa"
            self.humidity_unit = "kg_water/kg_dry_air"
            self.temp_min = 0
            self.temp_max = 50
        else:
            self.temp_range = np.arange(32, 111)
            self.temp_unit = "°F"
            self.pressure_unit = "psi"
            self.humidity_unit = "lb_water/lb_dry_air"
            self.temp_min = 32
            self.temp_max = 110

        # Figure settings
        self.figure_size = (12, 8)
        self.margins = {
            "top": 0.95,
            "bottom": 0.065,
            "left": 0.065,
            "right": 0.985,
        }

        # Font sizes
        self.fonts = {
            "label": 8,
            "title": 10,
            "tick": 8,
            "legend": 8,
        }

        # Line styles
        self.reference_lines = {
            "saturation": {
                "color": "b",
                "style": "-",
                "alpha": 0.7,
                "thickness": 1.5,
            },
            "relative_humidity": {
                "color": "b",
                "style": ":",
                "alpha": 0.6,
                "thickness": 1.0,
            },
            "reference": {
                "color": "k",
                "style": ":",
                "alpha": 0.5,
                "thickness": 0.75,
            },
        }

        # State point style
        self.state_point = {"color": "r", "size": 50}

        # Axis settings
        self.axis = {
            "x_minor_interval": 1,
            "y_minor_interval": 0.001,
            "y_limit": 0.03,
        }

        # Legend settings
        self.legend = {"location": "upper left"}

    def create_figure(self) -> Tuple[plt.Figure, plt.Axes]:
        """Create and initialize the figure and axes"""
        fig = plt.figure(figsize=self.figure_size)
        ax = fig.add_subplot(111)
        ax.tick_params(axis="both", labelsize=self.fonts["tick"])
        fig.subplots_adjust(**self.margins)
        return fig, ax

    def plot_humidity_lines(self, ax: plt.Axes, humidity_lines: List[ReferenceLine]) -> None:
        """Plot relative humidity lines"""
        for line in humidity_lines:
            relative_humidity = line.constant
            style = self.reference_lines[
                "saturation" if relative_humidity == 100 else "relative_humidity"
            ]

            ax.plot(
                line.x_vals,
                line.y_vals,
                f"{style['color']}{style['style']}",
                linewidth=style["thickness"],
                alpha=style["alpha"],
                label=f"{relative_humidity}% RH" if relative_humidity == 100 else None,
            )

    def plot_reference_lines(self, ax: plt.Axes, reference_lines: List[ReferenceLine]) -> None:
        """Plot reference lines for wetbulb and drybulb"""
        style = self.reference_lines["reference"]
        for line in reference_lines:
            ax.plot(
                line.x_vals,
                line.y_vals,
                f"{style['color']}{style['style']}",
                alpha=style["alpha"],
                linewidth=style["thickness"],
            )

    def plot_state_points(self, ax: plt.Axes, state_points: List[StatePoint]) -> None:
        """Plot state points on the chart"""
        for point in state_points:
            ax.scatter(
                point.drybulb,
                point.humidity_ratio,
                color=self.state_point["color"],
                s=self.state_point["size"],
                label=f"State Point ({point.drybulb}{self.temp_unit}, {point.relative_humidity}% RH)",
            )

    def configure_chart(self, ax: plt.Axes) -> None:
        """Configure the chart axes, labels, and appearance"""
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(self.axis["x_minor_interval"]))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(self.axis["y_minor_interval"]))
        plt.xlim(min(self.temp_range), max(self.temp_range))
        plt.ylim(0, self.axis["y_limit"])
        plt.legend(loc=self.legend["location"], fontsize=self.fonts["legend"])

        plt.xlabel(
            f"Dry-Bulb Temperature ({self.temp_unit})",
            fontsize=self.fonts["label"],
        )
        plt.ylabel(
            f"Humidity Ratio ({self.humidity_unit})",
            fontsize=self.fonts["label"],
        )
        plt.title(
            f"Psychrometric Chart (P_atm = {self.display_pressure} {self.pressure_unit})",
            pad=10,
            fontsize=self.fonts["title"],
        )


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


def main() -> None:

    STD_ATM_PRESSURE = 14.7  # 14.7 psi = 101.325 kPa (standard atmospheric pressure at sea level)

    chart = PsychrometricChart(unit_system="standard", pressure=STD_ATM_PRESSURE)

    state_0 = StatePoint(75.0, 45.0, STD_ATM_PRESSURE)
    state_1 = StatePoint(75.0, 60.0, STD_ATM_PRESSURE)
    state_2 = StatePoint(75.0, 75.0, STD_ATM_PRESSURE)
    chart.add_state_point(state_0)
    chart.add_state_point([state_1, state_2])

    chart.generate()


if __name__ == "__main__":
    main()
