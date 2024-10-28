from flask import Blueprint

default=Blueprint('default',__name__)

@default.route('/test_default')
def test_default():
    print("Default blueprint")
    return "<h3>Default blueprint</h3>"