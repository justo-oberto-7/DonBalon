from .estado_reserva import EstadoReserva

class ReservaFinalizada(EstadoReserva):
    def confirmar_pago(self, reserva):
        print(f"[{reserva.id}] Error: La reserva ya ha finalizado.")

    def cancelar(self, reserva):
        print(f"[{reserva.id}] Error: Una reserva finalizada no puede ser cancelada.")

    def finalizar_turno(self, reserva):
        print(f"[{reserva.id}] Error: La reserva ya ha finalizado.")