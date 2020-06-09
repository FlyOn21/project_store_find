import os

def standard_icon():
    basedir = os.path.abspath(os.path.dirname(__file__))
    standard_icon_path = basedir + '\\images\\' + 'smile.png'
    return standard_icon_path