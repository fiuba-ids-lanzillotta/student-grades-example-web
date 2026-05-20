import logging
from flask import Flask
from student_grades_example_web.routes.alumnos import alumnos_bp

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(name)s - %(message)s')

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
app.json.sort_keys = False
app.secret_key = 'supersecretkey'

app.register_blueprint(alumnos_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
