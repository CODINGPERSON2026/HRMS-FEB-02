from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    Blueprint,
    redirect,
    url_for,
    flash,
    make_response
)

import mysql.connector
from mysql.connector import Error
import mysql

import re
import json
import os
import pandas as pd
from datetime import datetime

from middleware import require_login, jwt, JWT_ALGO, JWT_SECRET

from blueprints.personal_information import personnel_info
from blueprints.weight_ms import weight_ms
from blueprints.apply_leave import leave_bp
