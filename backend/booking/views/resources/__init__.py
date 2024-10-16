from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, request
)

bp = Blueprint('resources', __name__, url_prefix = '/resources')

from . import api
