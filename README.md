# Automated Dimensional Analysis 

An automated online dimensional analysis tool. Plug in your variable names and dimensions, and get either a
dimensionless combination or the combination giving your desired dimension."

## About the project

The only automatic dinmensional analysis tool that I found online is that of Wolfram Alpha, but it does not work well. Python's Pint library has a great dimensional anlaysis tool, but requires the end-user to know how to code in Python. This motivated me to create a quick website to wrap the Pint code and make a friendly user interface for non-techy people.

The website is implemented with Flask on the backend, and basic HTML/Bootstrap/CSS and Flask methods on the frontend.

## Try it out

http://www.dimensionalanalysis.org/

## Todos

1. Dynamic number of inputs (more than the current MAX)
2. Allow units as input, e.g. "meter"
3. Cookies -- remembering previous inputs

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
