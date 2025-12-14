print("==================================================")
print("\t\t\tIncome-Expense Tracker")
print("==================================================")


"""
----------------------------------------TAX CYCLE------------------------------------------------------
Quarter	          Period Covered	                Deadline
Q1	              January 1 – March 31	            May 15
Q2	              April 1 – June 30	                August 15
Q3	              July 1 – September 30	            November 15
Q4	              October 1 – December 31	        April 15 next year (Rolled into the Annual Return)
"""


money_tracking = {
    'income' : [],
    'expense' : [],
    'input_vat' : [],
    'vat_expense' : []
}


# GET INCOME AND EXPENSE INPUTS
def input_income():
    try:
        income = float(input("Income amount ₱"))
        money_tracking['income'].append(income)
        print()
    except Exception as e:
        print("Error", e, "\n")

def input_expense():
    try:
        expense = float(input("Expense amount ₱"))
        money_tracking['expense'].append(expense)
        
        vat_included = input("Is this expense VAT-inclusive? (y/n): ").lower() == 'y'
        # Compute Input VAT only if you registered as VAT -> gross income is above 3m
        if vat_included:
            input_vat = round(expense * (12 / 112), 2)  # 12% of VAT-inclusive
            vat_expense = expense - input_vat  # for itemized deduction
        else:
            input_vat = 0
            vat_expense = expense
        money_tracking['vat_expense'].append(vat_expense)
        money_tracking['input_vat'].append(input_vat)

        print()
    except Exception as e:
        print("Error", e, "\n")
#


# CALCULATE TAXABLE NET INCOME, EXPENSES DEDUCTION
def gross_income():
    total_income = sum(money_tracking.get('income', []))

    return total_income

def deduction():
    deduct_expenses = sum(money_tracking.get('expense', []))

    return deduct_expenses

# 📌 If you have high expenses → choose itemized.
def itemized():
    itemized_deduction = sum(money_tracking.get('vat_expense', []))

    return itemized_deduction

def taxable_income_itemized():
    # For itemized deduction
    net_income = gross_income() - itemized()

    if net_income < 0:
        net_income = 0

    return net_income

# 📌 If you have low expenses → choose OSD (Optional Standard Deduction).
def osd():
    osd_deduction = gross_income() * 0.40

    return osd_deduction

def taxable_income_osd():
    # For osd deduction
    net_income = gross_income() - osd()

    if net_income < 0:
        net_income = 0

    return net_income
#


# COMPUTE TAX RATES + SUMMARY AND RECOMMENDATION REPORTS
"""
Best for businesses or self-employed individuals with high operating expenses 
or a large cost of goods sold, where deducting these costs significantly 
lowers the final taxable net income.
"""
# ⚠️ Graduated income tax rates - itemized
def income_tax_itemized():
    if taxable_income_itemized() <= 250_000:
        tax_due = 0
    elif taxable_income_itemized() <= 400_000:
        tax_due = (taxable_income_itemized() - 250_000) * 0.15
    elif taxable_income_itemized() <= 800_000:
        tax_due = 22_500 + (taxable_income_itemized() - 400_000) * 0.20
    elif taxable_income_itemized() <= 2_000_000:
        tax_due = 102_500 + (taxable_income_itemized() - 800_000) * 0.25
    elif taxable_income_itemized() <= 8_000_000:
        tax_due = 402_500 + (taxable_income_itemized() - 2_000_000) * 0.30
    else:
        tax_due = 2_202_500 + (taxable_income_itemized() - 8_000_000) * 0.35

    return tax_due

# ⚠️ Graduated income tax rates - osd
def income_tax_osd():
    if taxable_income_osd() <= 250_000:
        tax_due = 0
    elif taxable_income_osd() <= 400_000:
        tax_due = (taxable_income_osd() - 250_000) * 0.15
    elif taxable_income_osd() <= 800_000:
        tax_due = 22_500 + (taxable_income_osd() - 400_000) * 0.20
    elif taxable_income_osd() <= 2_000_000:
        tax_due = 102_500 + (taxable_income_osd() - 800_000) * 0.25
    elif taxable_income_osd() <= 8_000_000:
        tax_due = 402_500 + (taxable_income_osd() - 2_000_000) * 0.30
    else:
        tax_due = 2_202_500 + (taxable_income_osd() - 8_000_000) * 0.35

    return tax_due

"""
Best for self-employed individuals, freelancers, and small business owners.
Low operating expenses and annual gross income of less than 3 million.
Gross income is less than 3M -> non-vat | no percentage tax
"""
def flat_8_percent_tax():
    if gross_income() > 250_000:
        return (gross_income() - 250_000) * 0.08

    return 0

"""
Percentage tax is paid monthly or quarterly if 8% option is not chosen.
Graduated income tax + non-vat = 3% percentage tax - 3M below
Graduated income tax + vat = 12% value added tax - More than 3M
"""
def percentage_tax():
    # Only apply if gross income is 3m below and not choose 8% - Non-Vat
    if gross_income() <= 3_000_000:
        non_vat = gross_income() * 0.03
        return non_vat

    return 0

def value_added_tax():
    # This will only apply when the gross income is above 3m - Vat registered
    if gross_income() > 3_000_000:
        output_vat = gross_income() * 0.12
        input_vat = sum(money_tracking.get('input_vat', []))

        vat_payable = output_vat - input_vat
        return max(vat_payable, 0)  # VAT cannot be negative

    return 0
#


# TOTAL TAX DUE & DISPOSABLE INCOME(SAFE TO SPEND FOR PERSONAL USE)
def display_total():
    print("---Total Tax to Pay & Disposable Income---\n")
    if gross_income() > 3_000_000:
        # Vat
        total_tax_osd = value_added_tax() + income_tax_osd()
        total_tax_itemized = value_added_tax() + income_tax_itemized()

        disposable_income_osd = gross_income() - total_tax_osd
        disposable_income_itemized = gross_income() - total_tax_itemized
    else:
        # Non-Vat
        total_tax_osd = percentage_tax() + income_tax_osd()
        total_tax_itemized = percentage_tax() + income_tax_itemized()

        disposable_income_osd = gross_income() - total_tax_osd
        disposable_income_itemized = gross_income() - total_tax_itemized

        disposable_income_8 = (gross_income() - flat_8_percent_tax()) - deduction()
        print(f"total tax due (8%): ₱{flat_8_percent_tax():,.2f}")
        print(f"disposable income (8%): ₱{disposable_income_8:,.2f}\n")

    print(f"total tax due (osd): ₱{total_tax_osd:,.2f}")
    print(f"disposable income (osd): ₱{disposable_income_osd:,.2f}\n")

    print(f"total tax due (itemized): ₱{total_tax_itemized:,.2f}")
    print(f"disposable income (itemized): ₱{disposable_income_itemized:,.2f}\n")
    print("======================================================\n")


#START
def menu():
    menu_list = ("input income", "input expense", "show records")

    i = 0
    for x in menu_list:
        i+=1
        print(i, x)
    print()


def main():
    menu()

    try:
        pick = int(input("Pick: "))
        print()

        if pick == 1:
            input_income()
        elif pick == 2:
            input_expense()
        elif pick == 3:
            # record
            print(money_tracking, "\n")

            # total gross income
            print("---Total Annual---")
            print(f"gross income: ₱{gross_income():,.2f}\n\n")

            # osd - deduction and net taxable income
            print("---Deductions & Taxable Income---")
            print(f"optional standard deduction (osd): ₱{osd():,.2f}")
            print(f"net taxable income (osd): ₱{taxable_income_osd():,.2f}\n")

            # itemized - deduction and net taxable income
            print(f"itemized deduction: ₱{itemized():,.2f}")
            print(f"net taxable income (itemized): ₱{taxable_income_itemized():,.2f}\n\n")

            # Vat and Non-Vat condition
            print("---Vat & Non-Vat---")
            # Vat - gross income more than 3m
            print(f"value added tax (vat): ₱{value_added_tax():,.2f}")
            # Non-Vat - gross income 3m below
            print(f"percentage tax (non-vat): ₱{percentage_tax():,.2f}\n\n")

            # Tax due / Tax fee
            print("---Graduated Tax due---")
            print(f"graduated income tax due (osd): ₱{income_tax_osd():,.2f}")
            print(f"graduated income tax due (itemized): ₱{income_tax_itemized():,.2f}\n\n")

            display_total()
        else:
            print("-invalid input\n try again-\n")
    except Exception as e:
        print("\nError", e, "\n")

    main()

main()