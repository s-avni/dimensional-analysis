from flask import Flask, render_template, flash, redirect, request
from pint_wrapper.form import DimensionlessForm, DimensionForm
from pint import pi_theorem
from pint import formatter
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['WTF_CSRF_ENABLED'] = False

ERROR = "Error: "
DUMMY = "Dummy"


def get_pint_vars_from_form(form):
    vars_dict = dict()
    for entry in form.vars.entries:
        var_name = "" if entry.var_name.data is None else entry.var_name.data
        var_dim = "" if entry.var_dim.data is None else entry.var_dim.data
        if bool(var_name.strip() == "") != bool(var_dim.strip() == ""):
            return ERROR + "you have a partly filled entry"
        elif var_name.strip() == "" and var_dim.strip() == "":
            continue  # no input
        vars_dict[var_name.strip()] = var_dim.strip()
    return vars_dict


def calc_dimensionless_form(form):
    result = get_pint_vars_from_form(form)
    if isinstance(result, str): #an ERROR string
        return result
    vars_dict = result
    result = get_combination_for(vars_dict)
    return result

def calc_dimension_form(form):
    other_vars = get_pint_vars_from_form(form)
    if isinstance(other_vars, str): #an ERROR string
        return other_vars
    desired_dim = form.desired_dim.data
    if desired_dim.strip() == "":
        return ERROR + ": the desired dimension must be provided."
    other_vars[DUMMY] = desired_dim.strip() #we'll remove dummy later, first want a dimensionless result
    result = get_combination_for(other_vars)
    if result.startswith(ERROR):
        return result
    #change dimensionless result to the combination we want
    # e.g. if want to express T using V and X, we get T*V/X = [], so want X/V
    # that is, we flip the order of the substrings, split by "/"
    if "/" not in result:
        return ERROR + ": something is wrong with our understanding of the inputs :(("
    split_result = result.split("/") #todo: var names cannot include /!
    assert len(split_result) == 2
    if DUMMY in split_result[0]:
        # todo: regex...greedy.... ends with Dummy, then try to get * on left of it (if exists)
        # todo: regex....if starts with Dummy, try to get * on right of it (if exists)
        # todo: regex... if Dummy in the middle, remove Dummy and * on the right
        # todo: combine last two cases
        if split_result[0].endswith(DUMMY):
            split_result[0] = split_result[0].replace('* ' + DUMMY, '') #ends with * DUMMY
        elif split_result[]

def get_combination_for(vars_dict):
    logging.debug('list of vars, in dict format:')
    logging.debug(vars_dict)
    if len(vars_dict) == 0:
        return ERROR + "please enter some input"
    result = pi_theorem(vars_dict)  # https://buildmedia.readthedocs.org/media/pdf/pint/latest/pint.pdf
    if len(result) == 0:
        return ERROR + "it is not possible to find a dimensionless combination for your input"
    print(formatter(result[0].items()))
    pretty_result = formatter(result[0].items())
    return pretty_result


@app.route('/', methods=['GET', 'POST'])
def index():
    dimensionless_form = DimensionlessForm()
    dimension_form = DimensionForm()
    # result="A/b"
    # https://github.com/lepture/flask-wtf/issues/58
    # wtf-form's "is_submitted()" function does not actually check which form was submitted!
    if dimensionless_form.is_submitted(): #this actually check if either form was submitted! see comment above
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
        else: #dimension form was submitted
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
