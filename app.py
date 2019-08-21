from flask import Flask, render_template, flash, redirect
from pint_wrapper.form import DimensionlessForm, DimensionForm
from pint import pi_theorem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['WTF_CSRF_ENABLED'] = False

def get_pint_vars_from_form(form):
    list_of_vars = []
    for entry in form.vars.entries:
        print(entry.var_dim.data)
        print(entry.var_name.data)
        list_of_vars.append([entry.var_name.data, entry.var_dim.data])

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    dimensionless_form = DimensionlessForm()
    dimension_form = DimensionForm()
    if dimensionless_form.validate_on_submit():
        flash('Success!')
        get_pint_vars_from_form(dimensionless_form)
        return redirect('/')
    elif dimension_form.validate_on_submit():
        flash('Success!')
        return redirect('/')
    else:
        # print(dimensionless_form.vars.__dict__)
        print("Error:" + str(dimensionless_form.vars.errors)) #todo: make it ok if not all entries filled
        # flash("Error:" + str(dimensionless_form.vars.errors))
        # print(dimensionless_form.vars.entries[0].var_dim.data) #a list
        # print("\n\n Didn't work \n\n")
    return render_template('index.html', form1=dimensionless_form, form2=dimension_form)


if __name__ == '__main__':
    app.run()
