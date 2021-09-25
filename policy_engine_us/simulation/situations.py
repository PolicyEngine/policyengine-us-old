"""
Functions to convert URL query parameters into OpenFisca situation initialiser functions.
"""

from typing import Callable
from openfisca_us import CountryTaxBenefitSystem
from openfisca_us.entities import *

variables = CountryTaxBenefitSystem().variables


def create_situation(params: dict) -> Callable:
    def situation(sim):
        household = {}
        families = {}
        tax_unit_members = {}
        people = {}
        for key in params:
            components = key.split("_")
            if components[0] != "policy":
                variable = "_".join(components[:-1])
                entity_id = components[-1]
                try:
                    value = float(params[key])
                except:
                    value = params[key]
                if value == "true":
                    value = True
                elif value == "false":
                    value = False
                if variable not in variables and variable != "tax_unit":
                    print(f"Skipping variable {variable}")
                if (
                    variable == "tax_unit"
                    or variables[variable].entity.key == "person"
                ):
                    if entity_id not in people:
                        people[entity_id] = {}
                    if variable == "tax_unit":
                        if isinstance(value, float):
                            value = str(int(value))
                        if value not in tax_unit_members:
                            tax_unit_members[value] = []
                        tax_unit_members[value] += [entity_id]
                    else:
                        people[entity_id][variable] = value
                elif variables[variable].entity.key == "tax_unit":
                    if entity_id not in families:
                        families[entity_id] = {}
                    families[entity_id][variable] = value
                else:
                    household[variable] = value
        members_of_families = sum(map(list, tax_unit_members.values()), [])

        def is_adult(p_id):
            return people[p_id]["age"] >= 18

        def is_child(p_id):
            return not is_adult(p_id)

        for person in people:
            if "age" not in people[person]:
                people[person]["age"] = 18
            if person not in members_of_families:
                tax_unit_names = list(tax_unit_members.keys())
                i = 0
                if i == len(tax_unit_names):
                    families[str(i + 1)] = {}
                    tax_unit_names += [str(i + 1)]
                    tax_unit_members[str(i + 1)] = []
                adoptive_tax_unit = tax_unit_names[i]
                while (
                    len(
                        list(
                            filter(
                                is_adult, tax_unit_members[adoptive_tax_unit]
                            )
                        )
                    )
                    >= 2
                ):
                    i += 1
                    if i == len(families):
                        families[str(i + 1)] = {}
                        tax_unit_names += [str(i + 1)]
                        tax_unit_members[str(i + 1)] = []
                    adoptive_tax_unit = tax_unit_names[i]
                tax_unit_members[adoptive_tax_unit] += [person]
        i = 0
        for person_id, person in people.items():
            if i == 0:
                id_vars = dict(is_household_head=True, is_tax_unit_head=True)
                i += 1
            else:
                id_vars = dict()
            sim.add_person(**person, **id_vars, name=person_id)
        for tax_unit_id, tax_unit in families.items():
            sim.add_tax_unit(
                **tax_unit, members=tax_unit_members[tax_unit_id],
            )
        sim.add_household(**household, members=list(people))
        return sim

    return situation
