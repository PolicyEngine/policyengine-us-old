from openfisca_us import IndividualSim
import numpy as np


def headline_figures(baseline: IndividualSim, reformed: IndividualSim) -> dict:
    """Create dictionary of totals for the reform and baseline.

    :param baseline: Baseline simulation
    :type baseline: IndividualSim
    :param reformed: Reform simulation
    :type reformed: IndividualSim
    :return: Dictionary of baseline and reformed sums for a set of variables
    """

    def get_value(sim, name):
        return float(np.array(sim.calc(name)).sum())

    def get_values(name):
        return {
            "old": get_value(baseline, name),
            "new": get_value(reformed, name),
        }

    VARIABLES = [
        "net_income",
    ]
    return {name: get_values(name) for name in VARIABLES}
