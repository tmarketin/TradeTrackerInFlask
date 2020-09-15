from app import appInstance

@appInstance.route('/')
@appInstance.route('/index')
def index():
    return "Hello World!"