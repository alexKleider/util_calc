#!/usr/bin/env python3

#  file: pge.py
"""
Reads a csv file containing meeter readings.
Returns a report.
See README.rst for details.
Released under the GNU General Public License of your choosing.
©Alex Kleider alex@kleider.ca
"""
import datetime
import csv

readings_file = "readings.csv"
DEFAULT_CURRENCY_SIGN = '$'

# Re: Propane
propane_info = """
Meter reads in cubic feet.
From:
https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=0ahUKEwj9xIeC-83LAhUG92MKHWOEBBIQFggdMAA&url=http%3A%2F%2Fwww.edcgov.us%2FGovernment%2FAg%2FPropane_Conversion_Chart.aspx&usg=AFQjCNFSq8UUvwTExkGq_4SSyQmdszDKbA&sig2=3z3bhV6tNB_VVqRHZZGBrw
"""
gal_in_cu_ft = 0.0278  # Convert propane from cu ft to gallons.

def get_propane_cost(prev_reading, cur_reading, cost):
    return cost * gal_in_cu_ft * (cur_reading - prev_reading)

# Re: Electricity
pge_info = """From:
http://www.pge.com/tariffs/tm2/pdf/ELEC_SCHEDS_E-1.pdf
'Basic' (E6/E1) usage in kWh/day is:
"""
summer_base = 7.0  #| 'Basic' (E6/E1)
winter_base = 8.5  #| usage in kWh/day.

winter_months = [11, 12, 1, 2, 3,4]
tier1_price = 0.18212
tier2_price = 0.25444
tier3_price = 0.37442

month_lengths = {2: 28, 1: 31,  #| Additional code
                 4: 30, 3: 31,  #| accounts for
                 6: 30, 5: 31,  #| length of February
                 9: 30, 7: 31,  #| i.e. the leap yr
                11: 30, 8: 31,  #| algorithm:
                       12: 31}  #| days_in_february().

test_data = (
        ("2016-03-19","2016-04-16", 238.0),
        ("2016-04-16","2016-05-16", 231.0),
        ("2016-12-16","2017-01-14", 246.5),
        ("2016-03-04","2016-03-26", 187.0),
        ("2016-03-04","2016-02-01", None),
        ("2016-12-31","2017-02-01", 272.0),
            )

def days_in_february(year):
    """
    Returns 29 if leap year, else 28.

    Assumes the year will NOT be less than 2000.
    If <2000 or uninterpretable as a year,
    returns None after printing a warning.
    """
    try:
        yr = int(year)
    except ValueError:
        print("Bad input for a year.")
        return
    if yr < 2000:
        print("Probably an invalid year.")
        return
    if year%400==0: return 29 # Divisible by 400: Leap year   2000
    if year%100==0: return 28 # Divisible by 100: ! leap year 2100
    if year%4==0: return 29   # Divisible by 4  : Leap year   2008
    else: return 28           # ! divisible by 4: ! leap year 2009

def daysafter(date):
    """
    Returns days remaining in the month

    _after_ the date specified.  Accounts for leap years.
    """
    if date.month == 2:
        return days_in_february(date.year) - date.day
    return month_lengths[date.month] - date.day

def daysupto(date):
    """
    Returns the number of days in the month 

    up to and including the day specified.
    """
    return date.day

def base_usage(month, days):
    """
    Returns the base usage earned

    by the given number of days in the given month.
    A helper function for the next two functions.
    """
    if month in winter_months:
        return winter_base * days
    else:
        return summer_base * days

def base_usage_after(date):
    """
    Returns usage earned by the days after

    the specified day in the specified month.
    """
    return base_usage(date.month, 
            daysafter(date))

def base_usage_upto(date):
    """
    Returns the usage earned by the days up to
    
    and including the day in the month specified by date.
    """
    return base_usage(date.month,
            daysupto(date))

def get_base_usage(date1, date2):
    """
    Returns the base usage earned by the interval
    
    after the first and up to and including 
    the second of the dates specified.
    If date2 is before or the same as date1, an
    announcement is printed and None is returned.
    """
    if (date2 - date1).days < 1:
        print("Check your input!!")
        return
    if ((date2.month == date1.month)
    and (date2.year == date1.year)):
        return base_usage(date2.month,
                        date2.day - date1.day)
    ret = base_usage_after(date1) + base_usage_upto(date2)
    month = date1.month + 1
    year = date1.year
    if month == 13:
        month = 1
        year = year + 1
    while ((date2.year >= year)
    and (date2.month > month)):
        if month == 2: month_length = days_in_february(year)
        else: month_length = month_lengths[month]
        if month in winter_months:
            ret += winter_base * month_length
        else:
            ret += summer_base * month_length
        month += 1
        if month == 13:
            month = 1
            year += 1
    return ret

def get_date(s):
    """
    Returns a datetime.Date object

    based on the string provided which must be
    of the format YYYY-MM-DD (all are integers.)
    If interpretation of the string fails, an
    announcement is printed and None is returned.
    """
    t = s.split('-')
    try:
        year = int(t[0])
        month = int(t[1])
        day = int(t[2])
    except ValueError:
        print("Unable to create a date from string provided.")
        return 
    return datetime.date(year, month, day)

def get_pge_cost(kwh_used, base):
    """
    Returns the cost of the kwh_used
    
    Requires the base usage for its calculations.
    Provides closure around the tier pricing.
    """
    if kwh_used > (2 * base):
        return ((kwh_used - 2 * base) * tier3_price
                            + base * tier2_price
                            + base * tier1_price  )
    elif kwh_used > base:
        return (( kwh_used - base) * tier2_price
                            + base * tier1_price  )
    else:
        return kwh_used * tier1_price

def get_readings(readings_file):
    """
    Returns a string showing content of the CSV input file.
    """
    with open(readings_file) as csvfile:
        reader = csv.DictReader(csvfile)
        ret = ["""\nRAW DATA:
Date          cuft   Price/gal    kWh    Paid      Comments
----------   ------  ---------   -----  -------  --------------- """]
        for row in reader:
            ret.append(
"{} {:>8}{:>10}{:>9}{:>9}  {}"
            .format(row['Date'], row['cu_ft'],
                row['current price of propane/gal'] ,row['kwh'],
                row['paid'], row['comment']))
        return '\n'.join(ret)

def testing():
    """
    A little test routine.
    
    It can be made into a unit test in a future version.
    """
    prev_date = datetime.date(2016,4,16)
    cur_date = datetime.date(2016,5,23)
    print(cur_date)

    delta = cur_date - prev_date
    print("delta days => {}.".format(delta.days))
    print("Printing daysupto: {}.".format(daysupto(cur_date)))
    print("base usage up to: {}.".format(base_usage_upto(cur_date)))
    print("Printing days after: {}".format(daysafter(prev_date)))
    print("base usage after: {}.".format(base_usage_after(prev_date)))
    print("get_base_usage => {}."
            .format(get_base_usage(prev_date, cur_date)))

    print("=========================")
    for prev, cur, result in test_data:
        prev_date = get_date(prev)
        cur_date = get_date(cur)
        print(prev_date, cur_date)
        print(get_base_usage(prev_date, cur_date), result)
        print
    print("Expect 28 x 6:")
    for year in (2009, 2010, 2011, 1800, 1900, 2100):
        print(days_in_february(year))
    print("Expect 29 x 5:")
    for year in (2008, 2012, 2016, 2000, 2400):
        print(days_in_february(year))

    kwh_used = 60063 - 59708
    date1 = "2016-04-16"
    date2 = "2016-05-23"
    owing = get_pge_cost(kwh_used, get_base_usage(
            get_date(date1), get_date(date2)))
    print("Calculated cost is ${:0.2f}".format(owing))

def normalizeValue(val):
    """
    Normalizes currency values.

    Provides for parens as an alternative to minus
    and eliminates currency sign if present.
    If both are used, the currency sign is expected
    to be with in the parens.
    """
    if val.startswith('(') and val.endswith(')'):
       val = '-' + val[1:-1]
    return val.replace(DEFAULT_CURRENCY_SIGN,'')

def get_report(readings_file):
    """
    Prepares a report and returns it as a string.

    Report includes starting and ending readings,
    amount consumed and cost of each utility,
    as well as the total, how much if any was paid,
    and the amount outstanding.
    """
    with open(readings_file) as csvfile:
        reader = csv.DictReader(csvfile)
        report = ["\nUTILITIES REPORT\n"]
        report.append(
"""{}
    {:<12}  cuft  Cost
    {:<12}  kWh   Cost
  {} | {} | {}\n"""
.format(
"Date Range", "Propane", "Electricity", "Total", "Paid", "Owing"))
        row_number = 0
        owing = 0
        for row in reader:
            row_number += 1
            if row_number == 1:
                cur_date = row['Date']
                cur_gas = float(row['cu_ft'])
                cur_kwh = float(row['kwh'])
                continue
            else:
                prev_date = cur_date
                prev_gas = float(cur_gas)
                prev_kwh = float(cur_kwh)
                cur_date = row['Date']
                cur_gas = float(row['cu_ft'])
                cur_kwh = float(row['kwh'])
                gas_price = float(normalizeValue(
                            row['current price of propane/gal']))
                paid = float(normalizeValue(row['paid']))
                comment = row['comment']
                cost_of_propane = get_propane_cost(
                            prev_gas, cur_gas, gas_price)
                cost_of_electricity = get_pge_cost(
                    cur_kwh - prev_kwh,
                    get_base_usage(get_date(prev_date),
                                    get_date(cur_date)))
                total_cost = cost_of_propane + cost_of_electricity
                owing += (total_cost - paid)
                report.append(
"""from {} to {}
    {} - {} = {:0.1f}   ${:0.2f}
    {} - {} = {:0.1f}   ${:0.2f}
  ${:0.2f} | ${:0.2f} | ${:0.2f}\n""".format(prev_date, cur_date,
        cur_gas, prev_gas, cur_gas - prev_gas, cost_of_propane,
        cur_kwh, prev_kwh, cur_kwh - prev_kwh, cost_of_electricity,
        total_cost, paid, owing) )
                row_number += 1
        report.append("""
Amount owed at end of current rent cycle: ${:0.2f}.
(The last dollar amount given above.)
""".format(owing))
        return "\n".join(report)

if __name__ == "__main__":
    print(get_readings(readings_file))
    print
    print(get_report(readings_file))
