"""
Python model 'brook_law.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.functions import if_then_else
from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.7.1"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 400,
    "time_step": lambda: 1 / 4,
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
    name="INITIAL TIME", units="Months", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="FINAL TIME", units="Months", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="TIME STEP", units="Months", comp_type="Constant", comp_subtype="Normal"
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


@component.add(
    name="SAVEPER",
    units="Months",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The save time step for the simulation.
    """
    return __data["time"].saveper()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(name="nominal productivity", comp_type="Constant", comp_subtype="Normal")
def nominal_productivity():
    return 0.1


@component.add(
    name="experienced personnel needed for training",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"new_personnel": 1, "training_overhead_fte_experienced": 1},
)
def experienced_personnel_needed_for_training():
    return new_personnel() * training_overhead_fte_experienced() / 100


@component.add(
    name="communication overhead",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"experienced_personnel": 1, "new_personnel": 1},
)
def communication_overhead():
    return np.interp(
        experienced_personnel() + new_personnel(),
        [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0],
        [0.0, 1.5, 6.0, 13.5, 24.0, 37.5, 54.0],
    )


@component.add(
    name="training overhead FTE experienced",
    comp_type="Constant",
    comp_subtype="Normal",
)
def training_overhead_fte_experienced():
    return 25


@component.add(
    name="planned software",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def planned_software():
    return np.interp(
        time(),
        [0.0, 20.0, 40.0, 60.0, 80.0, 100.0, 120.0, 140.0, 160.0, 180.0, 200.0],
        [0.0, 50.0, 100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 450.0, 500.0],
    )


@component.add(
    name="personnel alocation rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "developed_software": 1,
        "planned_software": 1,
        "personnel_new_hire": 1,
        "time": 1,
    },
)
def personnel_alocation_rate():
    return if_then_else(
        developed_software() - planned_software() < -75,
        lambda: if_then_else(time() < 112, lambda: personnel_new_hire(), lambda: 0),
        lambda: 0,
    )


@component.add(
    name="assimilation rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"new_personnel": 1},
)
def assimilation_rate():
    return new_personnel() / 20


@component.add(
    name="software development rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "requirements": 1,
        "communication_overhead": 1,
        "new_personnel": 1,
        "experienced_personnel": 1,
        "experienced_personnel_needed_for_training": 1,
        "nominal_productivity": 1,
    },
)
def software_development_rate():
    return if_then_else(
        requirements() > 0,
        lambda: nominal_productivity()
        * (1 - communication_overhead() / 100)
        * (
            0.8 * new_personnel()
            + 1.2
            * (experienced_personnel() - experienced_personnel_needed_for_training())
        ),
        lambda: 0,
    )


@component.add(
    name="qunatidade de pessoas",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"new_personnel": 1, "experienced_personnel": 1},
)
def qunatidade_de_pessoas():
    return new_personnel() + experienced_personnel()


@component.add(name="personnel new hire", comp_type="Constant", comp_subtype="Normal")
def personnel_new_hire():
    return 10


@component.add(
    name="requirements",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_requirements": 1},
    other_deps={
        "_integ_requirements": {"initial": {}, "step": {"software_development_rate": 1}}
    },
)
def requirements():
    return _integ_requirements()


_integ_requirements = Integ(
    lambda: -software_development_rate(), lambda: 500, "_integ_requirements"
)


@component.add(
    name="developed software",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_developed_software": 1},
    other_deps={
        "_integ_developed_software": {
            "initial": {},
            "step": {"software_development_rate": 1},
        }
    },
)
def developed_software():
    return _integ_developed_software()


_integ_developed_software = Integ(
    lambda: software_development_rate(), lambda: 0, "_integ_developed_software"
)


@component.add(
    name="new personnel",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_new_personnel": 1},
    other_deps={
        "_integ_new_personnel": {
            "initial": {},
            "step": {"personnel_alocation_rate": 1, "assimilation_rate": 1},
        }
    },
)
def new_personnel():
    return _integ_new_personnel()


_integ_new_personnel = Integ(
    lambda: personnel_alocation_rate() - assimilation_rate(),
    lambda: 0,
    "_integ_new_personnel",
)


@component.add(
    name="experienced personnel",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_experienced_personnel": 1},
    other_deps={
        "_integ_experienced_personnel": {
            "initial": {},
            "step": {"assimilation_rate": 1},
        }
    },
)
def experienced_personnel():
    return _integ_experienced_personnel()


_integ_experienced_personnel = Integ(
    lambda: assimilation_rate(), lambda: 20, "_integ_experienced_personnel"
)
