import hashlib
import re
from models.user import User
from flask import Blueprint, request, session, render_template, redirect, url_for, make_response

blog = Blueprint('blog', __name__)