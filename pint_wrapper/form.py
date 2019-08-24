from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired

MIN_VALIDATORS = 8


class VariablesForm(FlaskForm):
    var_name = StringField('Name', validators=[DataRequired()])
    var_dim = StringField('Dimension', validators=[DataRequired()])


class DimensionlessForm(FlaskForm):
    vars = FieldList(FormField(VariablesForm), min_entries=MIN_VALIDATORS+1)
    submit = SubmitField('Find combination!')


class DimensionForm(FlaskForm):
    desired_dim = StringField('Desired dimension', validators=[DataRequired()])
    vars = FieldList(FormField(VariablesForm), min_entries=MIN_VALIDATORS)
    submit = SubmitField('Find combination!')