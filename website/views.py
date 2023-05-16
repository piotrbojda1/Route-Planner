from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from website import db
import requests
from dotenv import load_dotenv
import os

load_dotenv()

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        pass
    # Render the home page
    return render_template("home.html", user=current_user)