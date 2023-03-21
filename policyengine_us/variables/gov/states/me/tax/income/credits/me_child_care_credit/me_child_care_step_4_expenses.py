from policyengine_us.model_api import *


class me_child_care_step_4_expenses(Variable):
    value_type = float
    entity = TaxUnit
    label = "ME Child Care Step 4 Expenses"
    documentation = (
        "Expenses spent on child care which qualified as a Step 4 program"
    )
    definition_period = YEAR
    reference = "https://www.maine.gov/revenue/sites/maine.gov.revenue/files/inline-files/22_1040me_sched_a_ff.pdf"  # (y)
    default_value = 0
