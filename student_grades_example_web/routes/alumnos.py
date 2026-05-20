from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from ..services.alumnos import obtener_alumno, obtener_notas_alumno, agregar_nota
from ..services.materias import obtener_alumnos_materia
from ..constants import NOTA_MIN, NOTA_MAX

alumnos_bp = Blueprint('alumnos', __name__)


@alumnos_bp.route('/', methods=['GET', 'POST'])
def index():
    """Pagina principal: formulario para buscar un alumno por padron."""
    if request.method == 'POST':
        padron = request.form.get('padron', '').strip()

        if not padron:
            flash('Debes ingresar un numero de padron.', 'error')

            return redirect(url_for('alumnos.index'))

        return redirect(url_for('alumnos.detalle_alumno', padron=padron))

    return render_template('index.html')


@alumnos_bp.route('/detalle/<padron>', methods=['GET', 'POST'])
def detalle_alumno(padron):
    """Pagina de detalle del alumno: info personal + materias cursadas + alta de nota."""
    if request.method == 'POST':
        codigo = request.form.get('codigo', '').strip()
        nota_raw = request.form.get('nota', '').strip()
        fecha = request.form.get('fecha', '').strip()

        errores = []

        if not codigo:
            errores.append('El codigo de materia es obligatorio.')

        try:
            nota = int(nota_raw)
            if nota < NOTA_MIN or nota > NOTA_MAX:
                errores.append(f'La nota debe estar entre {NOTA_MIN} y {NOTA_MAX}.')
        except ValueError:
            errores.append('La nota debe ser un numero entero.')
            nota = None

        if not fecha:
            errores.append('La fecha es obligatoria.')

        if errores:
            for e in errores:
                flash(e, 'error')

            return redirect(url_for('alumnos.detalle_alumno', padron=padron))

        resultado = agregar_nota(padron, codigo, nota, fecha)

        if resultado.get('ok'):
            flash('Nota agregada con exito.', 'success')
        else:
            for e in resultado.get('errores', ['Error al guardar la nota.']):
                flash(e, 'error')

        return redirect(url_for('alumnos.detalle_alumno', padron=padron))

    alumno = obtener_alumno(padron)

    if not alumno:
        flash(f'No se encontro un alumno con padron {padron}.', 'error')

        return redirect(url_for('alumnos.index'))

    materias = obtener_notas_alumno(padron)

    return render_template('detalle.html', alumno=alumno, materias=materias)


@alumnos_bp.route('/materias/<codigo>/alumnos')
def alumnos_materia(codigo):
    """Endpoint JSON usado por el modal para listar alumnos que cursan una materia."""
    return jsonify(obtener_alumnos_materia(codigo))
