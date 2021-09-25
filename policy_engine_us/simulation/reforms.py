"""
Functions to convert JSON web app parameters into OpenFisca reform objects.
"""

from openfisca_core import periods
from openfisca_core.model_api import *
from openfisca_us.entities import *
from openfisca_us.api import *
from openfisca_us import CountryTaxBenefitSystem
from openfisca_us import reforms as ref

baseline_system = CountryTaxBenefitSystem()


def add_empty_UBI():
    def add_age_params(parameters: ParameterNode):
        parameters.benefit.add_child(
            "UBI",
            ParameterNode(
                data={
                    "all": {"values": {"0000-01-01": 0.00}},
                    "child": {"values": {"0000-01-01": 0.00}},
                    "WA_adult": {"values": {"0000-01-01": 0.00}},
                    "senior": {"values": {"0000-01-01": 0.00}},
                }
            ),
        )
        return parameters

    class UBI(Variable):
        entity = Person
        definition_period = YEAR
        label = "UBI"
        value_type = float

        def formula(person, period, parameters):
            UBI_params = parameters(period).benefit.UBI
            basic_income = UBI_params.all
            return basic_income

    baseline_SPM_unit_net_income = type(
        baseline_system.variables["SPM_unit_net_income"]
    )

    class SPM_unit_net_income(baseline_SPM_unit_net_income):
        def formula(spm_unit, period, parameters):
            ubi = spm_unit.sum(spm_unit.members("UBI", period))
            return (
                baseline_SPM_unit_net_income.formula(
                    spm_unit, period, parameters
                )
                + ubi
            )

    class add_UBI(Reform):
        def apply(self):
            self.modify_parameters(add_age_params)
            self.add_variable(UBI)
            self.update_variable(SPM_unit_net_income)

    return add_UBI


BASELINE_REFORM = add_empty_UBI()


def neutralizer_reform(variable):
    class reform(Reform):
        def apply(self):
            self.neutralize_variable(variable)

    return reform


def create_reform(parameters: dict, return_names=False):
    params = {}
    for key, value in parameters.items():
        components = key.split("_")
        if components[0] == "policy":
            name = "_".join(components[1:])
            try:
                params[name] = float(value)
            except:
                params[name] = value
    reforms = []
    names = []
    if "UBI" in params:
        names += ["UBI"]
        reforms += [ref.set_parameter("benefit.UBI.all", 12 * params["UBI"])]
    first_reform, later_reforms = (), ()
    if len(reforms) > 0:
        first_reform = reforms[0]
    if len(reforms) > 1:
        later_reforms = reforms[1:]
    reform_tuple = tuple(((add_empty_UBI(), first_reform), *later_reforms))
    if not return_names:
        return reform_tuple
    else:
        return reform_tuple, names
