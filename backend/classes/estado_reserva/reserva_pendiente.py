from .estado_reserva import EstadoReserva
from .reserva_pagada import ReservaPagada
from .reserva_cancelada import ReservaCancelada

class ReservaPendiente(EstadoReserva):
    def confirmar_pago(self, reserva):
        print(f"[{reserva.id}] Pago recibido. Confirmando reserva...")
        reserva.cambiar_estado(ReservaPagada())
        
    def cancelar(self, reserva):
        print(f"[{reserva.id}] Cancelando reserva pendiente.")
        reserva.cambiar_estado(ReservaCancelada())
        
    def finalizar_turno(self, reserva):
        print(f"[{reserva.id}] Advertencia: El turno pasó y la reserva sigue pendiente.")
        # Una reserva pendiente vencida se cancela automáticamente
        reserva.cambiar_estado(ReservaCancelada())






