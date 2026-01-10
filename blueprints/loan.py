# from flask import Flask, request, jsonify, render_template
# from database import get_db_connection
# from auth import require_login
# from dashboard import dashboard_bp
# app.register_blueprint(dashboard_bp)


# app = Flask(__name__)

# # ========== LOAN PAGE ==========
# @app.route("/loans")
# def loans_page():
#     user = require_login()
#     if not user:
#         return "Unauthorized", 401
#     return render_template("loans.html")



# # ========== GET LOANS ==========
# @app.route("/api/loans", methods=["GET"])
# def get_loans():
#     user = require_login()
#     if not user:
#         return jsonify({"error": "Unauthorized"}), 401

#     conn = get_db_connection()
#     cur = conn.cursor(dictionary=True)

#     cur.execute("SELECT * FROM loans ORDER BY id DESC")
#     rows = cur.fetchall()

#     cur.close()
#     conn.close()

#     return jsonify(rows)

# if __name__ == "__main__":
#     app.run(debug=True)
