from src.utils import calculate_saturation_pressure
from src.config import MOLECULAR_WEIGHT_RATIO_OF_WATER_VAPOR_TO_DRY_AIR


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
