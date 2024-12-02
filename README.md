# Psychrometric Chart Tools

A comprehensive Python library for generating interactive psychrometric charts with customizable state points and reference lines. This tool is designed for HVAC engineers, building scientists, and researchers working with psychrometric calculations and visualizations.

## Features

- Generate psychrometric charts in both Standard and Metric units
- Customizable atmospheric pressure settings (default: 14.7 psi / 101.325 kPa)
- Plot multiple state points with temperature and relative humidity
- Automatic calculation of humidity ratios
- Reference lines for:
  - Relative humidity (10% to 100%)
  - Dry bulb temperature
  - Wet bulb temperature
- Save charts as PNG, PDF, or SVG files
- Interactive chart manipulation
- Dew point temperature lines

## Usage

```python
from src.models import StatePoint, PsychrometricChart

# Create a new chart (standard/IP units)
chart = PsychrometricChart(unit_system="standard", pressure=14.7)

# Add state points
state_point = StatePoint(
    drybulb=75.0,           # Temperature (°F)
    relative_humidity=45.0,  # RH (%)
    pressure=14.7           # Pressure (psi)
)
chart.add_state_point(state_point)

# Generate and display the chart
chart.generate()
```

## Installation

Clone the repository:
```bash
git clone https:github.com/ccirone2/psychrometric-chart-tools.git
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

- Numpy
- Matplotlib
