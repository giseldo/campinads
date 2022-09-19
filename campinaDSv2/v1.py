"""
Python model 'v1.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.functions import if_then_else
from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.6.1"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 100,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Month",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="Month",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(name="quantidade de telas", comp_type="Constant", comp_subtype="Normal")
def quantidade_de_telas():
    return 300


@component.add(
    name="requirements",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_requirements": 1},
    other_deps={
        "_integ_requirements": {
            "initial": {"quantidade_de_telas": 1},
            "step": {"software_development_rate": 1},
        }
    },
)
def requirements():
    return _integ_requirements()


_integ_requirements = Integ(
    lambda: -software_development_rate(),
    lambda: quantidade_de_telas(),
    "_integ_requirements",
)


@component.add(
    name="software development rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"requirements": 1, "nominal_productivity": 1},
)
def software_development_rate():
    return if_then_else(requirements() < 0, lambda: 0, lambda: nominal_productivity())


@component.add(
    name="development software",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_development_software": 1},
    other_deps={
        "_integ_development_software": {
            "initial": {},
            "step": {"software_development_rate": 1},
        }
    },
)
def development_software():
    return _integ_development_software()


_integ_development_software = Integ(
    lambda: software_development_rate(), lambda: 0, "_integ_development_software"
)


@component.add(name="nominal productivity", comp_type="Constant", comp_subtype="Normal")
def nominal_productivity():
    return 3
