from flask import Flask,render_template
app = Flask(__name__) #Flask Constructor
# Next we create an instance of this class. The first argument is the name of the application’s module or package. __name__ is a convenient shortcut for this that is appropriate for most cases. This is needed so that Flask knows where to look for resources such as templates and static files.

# A decorator used to tell the application which URL is associated function
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    name = "Akaza"
    return render_template('about.html',name1 = name)

@app.route("/bootstrap")
def bootstrap():
    return render_template('bootstrap.html')

app.run(debug=True)

