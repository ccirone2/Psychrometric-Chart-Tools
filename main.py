from src.models import StatePoint, PsychrometricChart


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
