from flask import Flask, jsonify, render_template, request,Blueprint,redirect,url_for
import mysql.connector
import re
from middleware import require_login
from blueprints.personal_information import DB_CONFIG


leave_bp = Blueprint('apply_leave', __name__, url_prefix='/apply_leave')
@leave_bp.route('/')
def apply_leave():
    return render_template('apply_leave/apply_leave.html')
@leave_bp.route("/get_leave_details", methods=["POST"])
def get_leave_details():
    data = request.get_json()
    army_no = data.get("person_id")

    if not army_no:
        return jsonify({"success": False, "message": "Army number missing"}), 400

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT name, army_number, trade, `rank`, company
            FROM personnel
            WHERE army_number = %s
        """, (army_no,))
        personnel = cursor.fetchone()

        if not personnel:
            return jsonify({"success": False, "message": "No such soldier found"}), 404

        cursor.execute("""
            SELECT sr_no, year, al_days, cl_days, aal_days, total_days, remarks
            FROM leave_details
            WHERE army_number = %s
            ORDER BY year DESC
            LIMIT 1
        """, (army_no,))
        leaveinfo = cursor.fetchone()
        print(leaveinfo)

        cursor.close()
        conn.close()

        if not leaveinfo:
            return jsonify({
                "success": True,
                "personnel": personnel,
                "leave_balance": []
            })

        # Return leave rows as an ARRAY
        leave_balance = [
            {
                "leave_type": "AL",
                "total_leave": leaveinfo["al_days"],
                "leave_taken": 0,
                "balance_leave": leaveinfo["al_days"]
            },
            {
                "leave_type": "CL",
                "total_leave": leaveinfo["cl_days"],
                "leave_taken": 0,
                "balance_leave": leaveinfo["cl_days"]
            },
            {
                "leave_type": "AAL",
                "total_leave": leaveinfo["aal_days"],
                "leave_taken": 0,
                "balance_leave": leaveinfo["aal_days"]
            }
        ]

        return jsonify({
            "success": True,
            "personnel": personnel,
            "leave_balance": leave_balance
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@leave_bp.route("/search_personnel")
def search_personnel():
    query = request.args.get("query", "").strip()

    if query == "":
        return jsonify([])

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Search by army number (exact or partial)
        cursor.execute("""
            SELECT name, army_number,`rank`,trade 
            FROM personnel
            WHERE army_number LIKE %s
            LIMIT 1
        """, (f"%{query}%",))

        results = cursor.fetchall()

        cursor.close()
        conn.close()
        
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500