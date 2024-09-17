import sys, os
from flask import Flask, render_template, url_for
from flask_flatpages import FlatPages
from flask_frozen import Freezer

# some configuration, ensures
#1. Pages are loaded on request
#2. File name extensions for pages in Markdown

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = ['.md']
FLATPAGES_ROOT = 'pages'  # Ensure this points to the correct directory

app = Flask(__name__)  # URL Routing — Home Page
app.config.from_object(__name__)  # Load Configuration from this file
pages = FlatPages(app)  # Load pages
freezer = Freezer(app) # Added

# URL Routing — Home Page
@app.route("/")
def index():
    return render_template('index.html', pages=pages)

# URL Routing — About Page
@app.route("/about.html")
def about():
    # Define the page variable with the necessary attributes
    page = {
        'title': 'About Us',
        'html': '<p>This is the about page content.</p>'
    }
    return render_template('about.html', page=page)

# URL Routing — Contact Page
@app.route("/contact.html")
def contact():
    page = pages.get_or_404('contact')
    return render_template('contact.html', page=page)

# URL Routing - Flat Pages
# Retrieves the page path and returns the content
@app.route("/<path:path>/")
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)

# URL generator for the 'page' endpoint
@freezer.register_generator
def page_url_generator():
    for page in pages:
        yield 'page', {'path': page.path}

# Main Function, Runs at http://0.0.0.0:8000
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(port=8000)