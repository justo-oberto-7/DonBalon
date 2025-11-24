import sys
import os
import unittest
from unittest.mock import MagicMock, patch
from decimal import Decimal
from datetime import date

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.reserva_service import ReservaService
from schemas.reserva_transaccion_schema import ReservaTransaccionSchema, ReservaItemSchema
from classes.reserva import Reserva
from classes.turno import Turno
from classes.pago import Pago
from classes.estado_reserva.reserva_pagada import ReservaPagada
from classes.estado_reserva.reserva_pendiente import ReservaPendiente
from classes.estado_turno.turno_no_disponible import TurnoNoDisponible
from classes.metodo_pago import MetodoPago

class TestReservaService(unittest.TestCase):
    def setUp(self):
        self.mock_conn = MagicMock()
        self.service = ReservaService(connection=self.mock_conn)
        
        # Mock repositories
        self.service.repository = MagicMock()
        self.service.turno_repository = MagicMock()
        self.service.detalle_repository = MagicMock()
        self.service.pago_repository = MagicMock()
        self.service.cancha_repository = MagicMock()
        self.service.tipo_cancha_repository = MagicMock()
        self.service.metodo_pago_repository = MagicMock()

    def test_registrar_reserva_con_tarjeta_es_pagada(self):
        # Setup data
        item_data = ReservaItemSchema(id_cancha=1, id_horario=1, fecha=date.today())
        data = ReservaTransaccionSchema(id_cliente=1, id_metodo_pago=1, items=[item_data])

        # Mock repository responses
        self.service.turno_repository.get_by_cancha_horario_fecha.return_value = None
        
        mock_cancha = MagicMock()
        mock_cancha.id_tipo = 1
        self.service.cancha_repository.get_by_id.return_value = mock_cancha
        
        mock_tipo_cancha = MagicMock()
        mock_tipo_cancha.precio_hora = Decimal("100.00")
        self.service.tipo_cancha_repository.get_by_id.return_value = mock_tipo_cancha
        
        # Mock MetodoPago
        mock_metodo_pago = MetodoPago(id_metodo_pago=1, descripcion="Tarjeta de Crédito")
        self.service.metodo_pago_repository.get_by_id.return_value = mock_metodo_pago
        
        mock_reserva_creada = Reserva(id_reserva=123, estado=ReservaPagada())
        self.service.repository.create.return_value = mock_reserva_creada
        
        mock_turno_creado = Turno(id_turno=456, estado=TurnoNoDisponible())
        self.service.turno_repository.create.return_value = mock_turno_creado

        # Execute
        result = self.service.registrar_reserva_completa(data)

        # Verify
        self.service.repository.create.assert_called_once()
        args, _ = self.service.repository.create.call_args
        reserva_arg = args[0]
        self.assertIsInstance(reserva_arg.estado, ReservaPagada)
        print("Test Tarjeta -> Pagada: Passed")

    def test_registrar_reserva_con_efectivo_es_pendiente(self):
        # Setup data
        item_data = ReservaItemSchema(id_cancha=1, id_horario=1, fecha=date.today())
        data = ReservaTransaccionSchema(id_cliente=1, id_metodo_pago=2, items=[item_data])

        # Mock repository responses
        self.service.turno_repository.get_by_cancha_horario_fecha.return_value = None
        
        mock_cancha = MagicMock()
        mock_cancha.id_tipo = 1
        self.service.cancha_repository.get_by_id.return_value = mock_cancha
        
        mock_tipo_cancha = MagicMock()
        mock_tipo_cancha.precio_hora = Decimal("100.00")
        self.service.tipo_cancha_repository.get_by_id.return_value = mock_tipo_cancha
        
        # Mock MetodoPago
        mock_metodo_pago = MetodoPago(id_metodo_pago=2, descripcion="Efectivo")
        self.service.metodo_pago_repository.get_by_id.return_value = mock_metodo_pago
        
        mock_reserva_creada = Reserva(id_reserva=124, estado=ReservaPendiente())
        self.service.repository.create.return_value = mock_reserva_creada
        
        mock_turno_creado = Turno(id_turno=457, estado=TurnoNoDisponible())
        self.service.turno_repository.create.return_value = mock_turno_creado

        # Execute
        result = self.service.registrar_reserva_completa(data)

        # Verify
        self.service.repository.create.assert_called_once()
        args, _ = self.service.repository.create.call_args
        reserva_arg = args[0]
        self.assertIsInstance(reserva_arg.estado, ReservaPendiente)
        print("Test Efectivo -> Pendiente: Passed")

if __name__ == '__main__':
    unittest.main()
