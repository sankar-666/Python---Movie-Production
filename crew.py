from flask import *
from database import *


crew=Blueprint('crew',__name__)

@crew.route('/crewhome')
def crewhome():
    return render_template('crewhome.html')