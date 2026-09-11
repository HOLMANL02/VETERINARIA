"""
Carga datos de prueba realistas para TODOS los módulos del sistema
(clientes, mascotas, historias clínicas, consultas, vacunas,
medicamentos, tratamientos, inventario, servicios, facturas, pagos).

Requisito previo: haber corrido seed_inicial.py (roles + usuario admin).

Uso (dentro del contenedor backend, WORKDIR ya es /app):
    docker compose exec backend python scripts/seed_datos_completos.py

Es seguro volver a ejecutarlo: verifica antes de insertar para no duplicar.
"""
import sys
import os
from datetime import date, datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import SessionLocal, Base, engine
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.mascota import Mascota
from app.models.historia_clinica import HistoriaClinica
from app.models.consulta import Consulta
from app.models.vacuna import Vacuna
from app.models.medicamento import Medicamento
from app.models.tratamiento import Tratamiento
from app.models.movimiento_inventario import MovimientoInventario
from app.models.servicio import Servicio
from app.models.factura import Factura
from app.models.detalle_factura import DetalleFactura
from app.models.pago import Pago
from app.security.password import hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()


def obtener_o_crear_usuario(nombre, correo, rol_nombre):
    rol = db.query(Rol).filter(Rol.nombre == rol_nombre).first()
    if rol is None:
        raise RuntimeError(
            f"El rol '{rol_nombre}' no existe. Corre primero seed_inicial.py"
        )
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if usuario is None:
        usuario = Usuario(
            nombre=nombre,
            correo=correo,
            password_hash=hash_password("Prueba123!"),
            rol_id=rol.id,
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
    return usuario


try:
    # --- 1. Usuarios de prueba (veterinarios, recepcionista, auxiliar, caja) ---
    vet1 = obtener_o_crear_usuario("Dra. Camila Rojas", "camila.rojas@veterinaria.com", "veterinario")
    vet2 = obtener_o_crear_usuario("Dr. Santiago Pardo", "santiago.pardo@veterinaria.com", "veterinario")
    recepcion = obtener_o_crear_usuario("Laura Gómez", "laura.gomez@veterinaria.com", "recepcionista")
    auxiliar = obtener_o_crear_usuario("Andrés Torres", "andres.torres@veterinaria.com", "auxiliar")
    caja = obtener_o_crear_usuario("Diana Ruiz", "diana.ruiz@veterinaria.com", "caja")

    # --- 2. Clientes ---
    datos_clientes = [
        ("María Fernanda López", "3001234567", "mflopez@correo.com", "Cra 15 #45-20, Bogotá"),
        ("Carlos Alberto Méndez", "3012345678", "camendez@correo.com", "Cl 80 #12-34, Bogotá"),
        ("Juliana Castro", "3023456789", "jcastro@correo.com", "Av 68 #23-10, Bogotá"),
        ("Pedro Nel Sánchez", "3034567890", "pnsanchez@correo.com", "Cl 100 #55-12, Bogotá"),
        ("Valentina Ríos", "3045678901", "vrios@correo.com", "Cra 7 #30-45, Bogotá"),
    ]
    clientes = []
    for nombres, telefono, correo, direccion in datos_clientes:
        cliente = db.query(Cliente).filter(Cliente.correo == correo).first()
        if cliente is None:
            cliente = Cliente(nombres=nombres, telefono=telefono, correo=correo, direccion=direccion)
            db.add(cliente)
            db.commit()
            db.refresh(cliente)
        clientes.append(cliente)

    # --- 3. Mascotas (cada una asociada a un cliente) ---
    datos_mascotas = [
        (clientes[0], "Firulais", "Perro", "Labrador", "Macho", date(2021, 3, 15), 28.5),
        (clientes[0], "Michi", "Gato", "Criollo", "Hembra", date(2022, 7, 1), 4.2),
        (clientes[1], "Rocky", "Perro", "Bulldog Francés", "Macho", date(2020, 11, 20), 12.0),
        (clientes[2], "Luna", "Gato", "Siamés", "Hembra", date(2023, 1, 10), 3.8),
        (clientes[3], "Max", "Perro", "Golden Retriever", "Macho", date(2019, 5, 5), 32.0),
        (clientes[4], "Bella", "Perro", "Poodle", "Hembra", date(2022, 9, 30), 6.5),
    ]
    mascotas = []
    for cliente, nombre, especie, raza, sexo, nacimiento, peso in datos_mascotas:
        mascota = (
            db.query(Mascota)
            .filter(Mascota.nombre == nombre, Mascota.cliente_id == cliente.id)
            .first()
        )
        if mascota is None:
            mascota = Mascota(
                cliente_id=cliente.id,
                nombre=nombre,
                especie=especie,
                raza=raza,
                sexo=sexo,
                fecha_nacimiento=nacimiento,
                peso=peso,
            )
            db.add(mascota)
            db.commit()
            db.refresh(mascota)
        mascotas.append(mascota)

    # --- 4. Historias clínicas (una por mascota) ---
    historias = []
    for mascota in mascotas:
        historia = db.query(HistoriaClinica).filter(HistoriaClinica.mascota_id == mascota.id).first()
        if historia is None:
            historia = HistoriaClinica(
                mascota_id=mascota.id,
                fecha_apertura=mascota.fecha_nacimiento or date(2023, 1, 1),
                antecedentes="Sin antecedentes relevantes reportados por el propietario.",
                observaciones="Paciente en control periódico.",
            )
            db.add(historia)
            db.commit()
            db.refresh(historia)
        historias.append(historia)

    # --- 5. Medicamentos (catálogo de inventario) ---
    datos_medicamentos = [
        ("Amoxicilina 250mg", "Antibiótico de amplio espectro", 120, 20, 8500),
        ("Meloxicam 1.5mg/ml", "Antiinflamatorio para perros y gatos", 60, 10, 15000),
        ("Vacuna Antirrábica", "Vacuna contra la rabia, dosis única anual", 40, 15, 22000),
        ("Ivermectina 1%", "Antiparasitario de uso general", 80, 15, 9500),
        ("Suero fisiológico 500ml", "Hidratación y limpieza de heridas", 100, 25, 6000),
    ]
    medicamentos = []
    for nombre, desc, stock, minimo, precio in datos_medicamentos:
        medicamento = db.query(Medicamento).filter(Medicamento.nombre == nombre).first()
        if medicamento is None:
            medicamento = Medicamento(
                nombre=nombre, descripcion=desc, stock=stock, stock_minimo=minimo, precio=precio
            )
            db.add(medicamento)
            db.commit()
            db.refresh(medicamento)
        medicamentos.append(medicamento)

    # --- 6. Servicios (catálogo facturable) ---
    datos_servicios = [
        ("Consulta general", "Valoración veterinaria estándar", 45000),
        ("Vacunación", "Aplicación de vacuna, sin incluir el biológico", 20000),
        ("Baño y peluquería", "Baño medicado y corte de pelo", 35000),
        ("Cirugía menor", "Procedimiento ambulatorio de baja complejidad", 180000),
    ]
    servicios = []
    for nombre, desc, precio in datos_servicios:
        servicio = db.query(Servicio).filter(Servicio.nombre == nombre).first()
        if servicio is None:
            servicio = Servicio(nombre=nombre, descripcion=desc, precio=precio)
            db.add(servicio)
            db.commit()
            db.refresh(servicio)
        servicios.append(servicio)

    # --- 7. Vacunas aplicadas ---
    if db.query(Vacuna).count() == 0:
        db.add_all([
            Vacuna(mascota_id=mascotas[0].id, nombre="Antirrábica", fecha_aplicacion=date(2024, 3, 20), proxima_dosis=date(2025, 3, 20), lote="LT-2201"),
            Vacuna(mascota_id=mascotas[2].id, nombre="Polivalente", fecha_aplicacion=date(2024, 6, 10), proxima_dosis=date(2025, 6, 10), lote="LT-3390"),
            Vacuna(mascota_id=mascotas[4].id, nombre="Antirrábica", fecha_aplicacion=date(2024, 1, 5), proxima_dosis=date(2025, 1, 5), lote="LT-2201"),
        ])
        db.commit()

    # --- 8. Consultas + tratamientos (asociadas a la historia clínica) ---
    if db.query(Consulta).count() == 0:
        consulta1 = Consulta(
            historia_id=historias[0].id,
            veterinario_id=vet1.id,
            fecha=datetime(2024, 8, 12, 10, 30, tzinfo=timezone.utc),
            motivo="Decaimiento y falta de apetito",
            examen="Temperatura 39.2°C, mucosas normales, abdomen sin dolor a la palpación.",
            diagnostico="Gastroenteritis leve",
            tratamiento="Dieta blanda y antiinflamatorio por 5 días",
        )
        consulta2 = Consulta(
            historia_id=historias[2].id,
            veterinario_id=vet2.id,
            fecha=datetime(2024, 9, 3, 15, 0, tzinfo=timezone.utc),
            motivo="Control postoperatorio",
            examen="Herida en buen proceso de cicatrización, sin signos de infección.",
            diagnostico="Evolución favorable",
            tratamiento="Continuar antibiótico y retirar puntos en 7 días",
        )
        db.add_all([consulta1, consulta2])
        db.commit()
        db.refresh(consulta1)
        db.refresh(consulta2)

        db.add_all([
            Tratamiento(
                consulta_id=consulta1.id,
                medicamento_id=medicamentos[1].id,
                dosis="0.2 ml/kg",
                frecuencia="Cada 24 horas",
                duracion="5 días",
                indicaciones="Administrar con alimento",
            ),
            Tratamiento(
                consulta_id=consulta2.id,
                medicamento_id=medicamentos[0].id,
                dosis="1 tableta",
                frecuencia="Cada 12 horas",
                duracion="7 días",
                indicaciones="Completar el ciclo aunque mejore antes",
            ),
        ])
        db.commit()

    # --- 9. Movimientos de inventario (salidas por los tratamientos anteriores) ---
    if db.query(MovimientoInventario).count() == 0:
        db.add_all([
            MovimientoInventario(
                medicamento_id=medicamentos[1].id, tipo="salida", cantidad=1,
                lote="LT-9001", fecha=datetime(2024, 8, 12, 11, 0, tzinfo=timezone.utc),
                usuario_id=auxiliar.id,
            ),
            MovimientoInventario(
                medicamento_id=medicamentos[0].id, tipo="salida", cantidad=1,
                lote="LT-9002", fecha=datetime(2024, 9, 3, 15, 30, tzinfo=timezone.utc),
                usuario_id=auxiliar.id,
            ),
            MovimientoInventario(
                medicamento_id=medicamentos[3].id, tipo="entrada", cantidad=40,
                lote="LT-9003", fecha=datetime(2024, 7, 1, 9, 0, tzinfo=timezone.utc),
                usuario_id=auxiliar.id,
            ),
        ])
        db.commit()

    # --- 10. Facturas + detalle + pagos ---
    if db.query(Factura).count() == 0:
        factura1 = Factura(
            cliente_id=clientes[0].id,
            fecha=datetime(2024, 8, 12, 11, 15, tzinfo=timezone.utc),
            subtotal=65000, impuestos=0, total=65000, estado="pagada",
        )
        factura2 = Factura(
            cliente_id=clientes[2].id,
            fecha=datetime(2024, 9, 3, 15, 45, tzinfo=timezone.utc),
            subtotal=225000, impuestos=0, total=225000, estado="pendiente",
        )
        db.add_all([factura1, factura2])
        db.commit()
        db.refresh(factura1)
        db.refresh(factura2)

        db.add_all([
            DetalleFactura(factura_id=factura1.id, servicio_id=servicios[0].id, cantidad=1, precio=45000),
            DetalleFactura(factura_id=factura1.id, medicamento_id=medicamentos[1].id, cantidad=1, precio=15000),
            DetalleFactura(factura_id=factura2.id, servicio_id=servicios[3].id, cantidad=1, precio=180000),
            DetalleFactura(factura_id=factura2.id, medicamento_id=medicamentos[0].id, cantidad=1, precio=8500),
        ])
        db.add(Pago(
            factura_id=factura1.id, metodo="tarjeta", valor=65000,
            fecha=datetime(2024, 8, 12, 11, 20, tzinfo=timezone.utc), estado="confirmado",
        ))
        db.commit()

    print("Datos de prueba cargados correctamente.")
    print(f"  Clientes: {db.query(Cliente).count()}")
    print(f"  Mascotas: {db.query(Mascota).count()}")
    print(f"  Historias clínicas: {db.query(HistoriaClinica).count()}")
    print(f"  Consultas: {db.query(Consulta).count()}")
    print(f"  Medicamentos: {db.query(Medicamento).count()}")
    print(f"  Servicios: {db.query(Servicio).count()}")
    print(f"  Facturas: {db.query(Factura).count()}")

finally:
    db.close()
