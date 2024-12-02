import numpy as np
from typing import Tuple, List, Literal
import matplotlib.pyplot as plt

# Use direct imports instead of from src.models
from .reference_line import ReferenceLine
from .state_point import StatePoint
from ..utils.calculations import calculate_saturation_pressure
from ..config.constants import MOLECULAR_WEIGHT_RATIO_OF_WATER_VAPOR_TO_DRY_AIR
from ..config.chart_style import ChartStyle


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
