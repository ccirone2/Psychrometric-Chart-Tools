import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from typing import Tuple, List

from ..models.reference_line import ReferenceLine


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

    def plot_state_points(self, ax: plt.Axes, state_points: List["StatePoint"]) -> None:
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
