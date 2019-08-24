from flask import Flask, render_template, flash, redirect, request
from pint_wrapper.form import DimensionlessForm, DimensionForm
from pint import pi_theorem
from pint import formatter
import logging
import re

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['WTF_CSRF_ENABLED'] = False

ERROR = "Error: "
DUMMY = "Dummy"
REMOVE_A_VAR = "REMOVE A VARIABLE" # e.g. DUMMY = [mass], m=[mass], T=[time], f=1/[time] -->
    # could return T*f because that is already a solution.
    # so, we need to ensure DUMMY is in solution! remove the other vars...


def get_pint_vars_from_form(form):
    vars_dict = dict()
    for entry in form.vars.entries:
        var_name = "" if entry.var_name.data is None else entry.var_name.data
        var_dim = "" if entry.var_dim.data is None else entry.var_dim.data
        if bool(var_name.strip() == "") != bool(var_dim.strip() == ""):
            return ERROR + "you have a partly filled entry"
        if var_name.strip() == "" and var_dim.strip() == "":
            continue  # no input
        if "/" in var_name or " " in var_name.strip():  # due to regex later, when formatting result
            return ERROR + "there can be no spaces or slashes (/) in a variable name"
        vars_dict[var_name.strip()] = var_dim.strip()
    return vars_dict


def calc_dimensionless_form(form):
    result = get_pint_vars_from_form(form)
    if isinstance(result, str):  # an ERROR string
        return result
    vars_dict = result
    result = get_combination_for(vars_dict)
    return result


def format_dimension_result(res):
    # change dimensionless result to the combination we want
    # e.g. if want to express D using V and X, we get D*V/X = [], so want X/V
    # that is, we flip the order of the substrings, split by "/
    # e.g. if T/DV =[], then D = T/V #no flipping!
    print("\n ********* \n")
    print(res)
    # Note!
    # e.g. DUMMY = [mass], m=[mass], T=[time], f=1/[time] -->
    # could return T*f because that is already a solution.
    # so, we need to ensure DUMMY is in solution! remove the other vars...
    if DUMMY not in res: #e.g. DUMMY = [mass], T=[time], f=1/[time]
        return REMOVE_A_VAR
        # return ERROR + ": there is no suitable combination to give your desired dimension."
    split_result = res.split("/")
    assert len(split_result) == 2
    fixed_parts = [None, None]  # what goes first, what goes second, split by "/"
    for i in [0, 1]:
        if DUMMY in split_result[i]:
            other_part = split_result[(i + 1) % 2]
            this_part = re.sub(" \* " + DUMMY + " \*", " \* ", split_result[i])  # e.g. V * Dummy * T
            if DUMMY in this_part:
                this_part = re.sub(DUMMY + " \* ", "", split_result[i])  # e.g. Dummy * T
                if DUMMY in this_part:
                    this_part = re.sub("\* " + DUMMY, "", split_result[i])  # e.g. T * DUMMY
                    if DUMMY in this_part:  # DUMMY is by itself
                        this_part = "1"
            fixed_parts = [other_part, this_part]

    logging.debug(fixed_parts)
    if fixed_parts[1] == "1":  # e.g. no need to write V / 1
        return fixed_parts[0]
    return fixed_parts[0] + "/" + fixed_parts[1]


def get_correct_combination_for(vars_dict):
    while len(vars_dict) != 1: #i.e. DUMMY is not the only variable
        result = get_combination_for(vars_dict)
        if result.startswith(ERROR):
            return result
        dimensionless_string = format_dimension_result(result)
        if dimensionless_string != REMOVE_A_VAR:
            return dimensionless_string

        # we have at least 1 dependent var that is not dummy
        # take the first var before the first * or / (whichever comes first); we know it's not DUMMy
        unneeded_dimension_name = result.split("*")[0]
        unneeded_dimension_name = unneeded_dimension_name.split("/")[0]
        vars_dict.pop(unneeded_dimension_name.strip())
    return ERROR + ": we could not find a combination for your desired dimension"


def calc_dimension_form(form):
    other_vars = get_pint_vars_from_form(form)
    if isinstance(other_vars, str):  # an ERROR string
        return other_vars
    desired_dim = form.desired_dim.data
    if desired_dim.strip() == "":
        return ERROR + ": the desired dimension must be provided."
    other_vars[DUMMY] = desired_dim.strip()  # we'll remove dummy later, first want a dimensionless result
    return get_correct_combination_for(other_vars)


def get_combination_for(vars_dict):
    logging.debug('list of vars, in dict format:')
    logging.debug(vars_dict)
    if len(vars_dict) == 0:
        return ERROR + "please enter some input"
    result = pi_theorem(vars_dict)  # https://buildmedia.readthedocs.org/media/pdf/pint/latest/pint.pdf
    if len(result) == 0:
        return ERROR + "it is not possible to find a dimensionless combination for your input"
    # print("\n*************\n")
    # print(result)
    # print(formatter(result[0].items()))
    # raise ValueError
    pretty_result = formatter(result[0].items())
    return pretty_result


@app.route('/', methods=['GET', 'POST'])
def index():
    dimensionless_form = DimensionlessForm()
    dimension_form = DimensionForm()
    # result="A/b"
    # https://github.com/lepture/flask-wtf/issues/58
    # wtf-form's "is_submitted()" function does not actually check which form was submitted!
    if dimensionless_form.is_submitted():  # this actually check if either form was submitted! see comment above
        if request.form["form_type"] == "dimensionless":
            logging.debug("DIMENSION --- LESS\n\n")
            logging.debug(dimensionless_form.vars.__dict__)
            result = calc_dimensionless_form(dimensionless_form)
            if result.startswith(ERROR):
                return render_template('index.html', form1=dimensionless_form,
                                       form2=dimension_form, error=result)
            else:
                return render_template('index.html', form1=dimensionless_form,
                                       form2=dimension_form, result=result)
        else:  # dimension form was submitted
            logging.debug("DIMENSION! \n\n")
            logging.debug(dimension_form.vars.__dict__)
            result = calc_dimension_form(dimension_form)
            if result.startswith(ERROR):
                return render_template('index.html', form1=dimensionless_form,
                                       form2=dimension_form, error2=result)
            else:
                return render_template('index.html', form1=dimensionless_form,
                                       form2=dimension_form, result=None, error=None, result2=result, error2=None)
    return render_template('index.html', form1=dimensionless_form, form2=dimension_form)


if __name__ == '__main__':
    app.run()
