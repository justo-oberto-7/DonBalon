from .estado_reserva import EstadoReserva

class ReservaCancelada(EstadoReserva):
    def confirmar_pago(self, reserva):
        print(f"[{reserva.id}] Error: No se puede pagar una reserva cancelada.")

    def cancelar(self, reserva):
        print(f"[{reserva.id}] Error: La reserva ya está cancelada.")

    def finalizar_turno(self, reserva):
        print(f"[{reserva.id}] La reserva cancelada no necesita finalizarse.")