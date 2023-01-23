from flask import Flask
from public import public
from staff import staff
from admin import admin
from crew import crew

app=Flask(__name__)
app.secret_key="prayulla"
app.register_blueprint(admin,url_prefix="/admin")
app.register_blueprint(staff,url_prefix="/staff")
app.register_blueprint(crew,url_prefix="/crew")
app.register_blueprint(public)


app.run(debug=True,port=5072)