function abrirModal(id) {
    const modal = document.getElementById(id);

    modal.classList.add('modal--open');
    modal.setAttribute('aria-hidden', 'false');
}

function cerrarModal(id) {
    const modal = document.getElementById(id);

    modal.classList.remove('modal--open');
    modal.setAttribute('aria-hidden', 'true');
}

function abrirModalAgregar()  { abrirModal('modalAgregar'); }
function cerrarModalAgregar() { cerrarModal('modalAgregar'); }

function mostrarDetalleMateria(nombre, nota, fecha) {
    document.getElementById('detalleMateriaNombre').textContent = nombre;
    document.getElementById('detalleMateriaNota').textContent   = nota;
    document.getElementById('detalleMateriaFecha').textContent  = fecha;
    abrirModal('modalDetalleMateria');
}

function cerrarModalDetalleMateria() { cerrarModal('modalDetalleMateria'); }

async function mostrarAlumnosMateria(codigo) {
    document.getElementById('nombreMateriaModal').textContent = codigo;

    const tabla = document.getElementById('alumnosMateriaTabla');

    tabla.innerHTML = '<tr><td colspan="3" style="text-align:center;color:#888;">Cargando...</td></tr>';
    
    abrirModal('modalAlumnosMateria');

    try {
        const res = await fetch(`/materias/${encodeURIComponent(codigo)}/alumnos`);
        const alumnos = await res.json();

        if (!alumnos.length) {
            tabla.innerHTML = '<tr><td colspan="3" style="text-align:center;color:#888;">No hay alumnos cursando esta materia.</td></tr>';
            return;
        }

        tabla.innerHTML = '';
        alumnos.forEach(a => {
            const fila = document.createElement('tr');
            fila.innerHTML = `<td>${a.padron}</td><td>${a.nombre}</td><td>${a.apellido}</td>`;
            tabla.appendChild(fila);
        });
    } catch (e) {
        tabla.innerHTML = '<tr><td colspan="3" style="text-align:center;color:#c00;">Error al cargar los alumnos.</td></tr>';
    }
}
function cerrarModalAlumnosMateria() { cerrarModal('modalAlumnosMateria'); }

// Cerrar modales al hacer click fuera o con ESC
window.addEventListener('click', function (event) {
    document.querySelectorAll('.modal--open').forEach(m => {
        if (event.target === m) cerrarModal(m.id);
    });
});

window.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
        document.querySelectorAll('.modal--open').forEach(m => cerrarModal(m.id));
    }
});
