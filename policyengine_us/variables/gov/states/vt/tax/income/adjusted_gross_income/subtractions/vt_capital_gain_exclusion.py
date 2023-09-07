from policyengine_us.model_api import *


class vt_capital_gain_exclusion(Variable):
    value_type = float
    entity = TaxUnit
    label = "Vermont capital gain exclusion"
    unit = USD
    documentation = "This is subtracted from federal adjusted gross income in Vermont as captial gain exclusion."
    definition_period = YEAR
    defined_for = StateCode.VT
    reference = (
        "https://tax.vermont.gov/sites/tax/files/documents/IN-153-2022.pdf#page=1"  # 2022 Schedule IN-153 Vermont Capital Gains Exclusion Calculation
        "https://legislature.vermont.gov/statutes/section/32/151/05811"  # Titl. 32 V.S.A. § 5811(21)(B)(ii)
        "https://tax.vermont.gov/sites/tax/files/documents/IN-153%20Instr-2022.pdf"
    )

    def formula(tax_unit, period, parameters):
        # Get adjusted net capital gain
        adjusted_net_capital_gain = tax_unit(
            "adjusted_net_capital_gain", period
        )
        p = parameters(
            period
        ).gov.states.vt.tax.income.agi.capital_gain_exclusion
        # The flat exclusion is the less of $5,000 or the actual amount of net adjusted capital gains
        flat_exclusion = min_(adjusted_net_capital_gain, p.flat.max)
        # The percentage exclusion equals to 40% of the adjusted net capital gain and has a maximum value
        percentage_exclusion = (
            adjusted_net_capital_gain * p.percentage.percentage
        )
        percentage_exclusion = min_(percentage_exclusion, p.percentage.max)
        # Filer can choose from flat or percentage exclusion. Assume the filer will always choose the larger one
        chosen_exclusion = max_(flat_exclusion, percentage_exclusion)
        # The chosen exclusion should not exceed 40% of federal taxable income
        federal_taxable_income = tax_unit("taxable_income", period)
        cap = federal_taxable_income * p.cap
        return min_(chosen_exclusion, cap)
