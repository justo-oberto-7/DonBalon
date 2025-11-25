"""Generador de muchos datos de ejemplo para pruebas de reportes.

Inserta múltiples clientes, turnos, reservas y detalles distribuidos a lo largo
de varios meses para crear reportes más grandes.
"""
import sqlite3
from pathlib import Path
from datetime import date, timedelta
import random


def generate(db_path=None, months=12):
    if db_path is None:
        db_path = Path(__file__).parent / "donbalon.db"
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    try:
        # Añadir clientes adicionales
        existing = cur.execute("SELECT COUNT(*) FROM Cliente").fetchone()[0]
        to_add = max(0, 50 - existing)
        for i in range(to_add):
            idx = existing + i + 1
            cur.execute(
                "INSERT INTO Cliente (nombre, apellido, telefono, mail, password, admin) VALUES (?, ?, ?, ?, ?, 0)",
                (f"Cliente{idx}", f"Apellido{idx}", f"{1000000000+idx}", f"cliente{idx}@example.com", "pass")
            )

        # Obtener canchas y horarios disponibles
        canchas = [r[0] for r in cur.execute("SELECT id_cancha FROM Cancha").fetchall()]
        horarios = [r[0] for r in cur.execute("SELECT id_horario FROM Horario").fetchall()]
        clientes = [r[0] for r in cur.execute("SELECT id_cliente FROM Cliente").fetchall()]

        if not canchas or not horarios or not clientes:
            print("Faltan datos base (Canchas/Horarios/Clientes). Ejecutá datos_ejemplo_db primero.")
            return

        # Crear turnos y reservas para 12 meses empezando en enero 2025
        start = date(2025, 1, 1)
        total_days = months * 30
        dia = start
        created_turnos = 0
        created_reservas = 0

        for day_offset in range(total_days):
            dia = start + timedelta(days=day_offset)
            # Para cada cancha, crear algunos turnos por día
            for cancha_id in canchas:
                # Randomly skip some days to add variety
                if random.random() < 0.6:
                    for horario_id in horarios:
                        # Crear turno
                        cur.execute(
                            "INSERT INTO Turno (id_cancha, id_horario, fecha, estado_turno) VALUES (?, ?, ?, 'DISPONIBLE')",
                            (cancha_id, horario_id, dia.isoformat())
                        )
                        turno_id = cur.lastrowid
                        created_turnos += 1

                        # Crear reservas en ~25% de los turnos
                        if random.random() < 0.25:
                            cliente_id = random.choice(clientes)
                            monto = random.choice([300.0, 350.0, 400.0, 450.0, 500.0])
                            cur.execute(
                                "INSERT INTO Reserva (id_cliente, monto_total, fecha_reserva, estado_reserva) VALUES (?, ?, ?, 'PAGADA')",
                                (cliente_id, monto, dia.isoformat())
                            )
                            reserva_id = cur.lastrowid
                            created_reservas += 1

                            # ReservaDetalle
                            cur.execute(
                                "INSERT INTO ReservaDetalle (id_reserva, id_turno, precio_total_item) VALUES (?, ?, ?)",
                                (reserva_id, turno_id, monto)
                            )

                            # Pago
                            cur.execute(
                                "INSERT INTO Pago (id_reserva, id_metodo_pago, fecha_pago, monto) VALUES (?, ?, ?, ?)",
                                (reserva_id, 1, dia.isoformat(), monto)
                            )

            # commit periodico
            if day_offset % 50 == 0:
                conn.commit()

        conn.commit()
        print(f"Generados: {created_turnos} turnos y {created_reservas} reservas en {months} meses.")

    except sqlite3.Error as e:
        print("Error al insertar datos:", e)
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    generate()
