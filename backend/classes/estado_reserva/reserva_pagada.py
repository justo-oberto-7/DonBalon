from .estado_reserva import EstadoReserva
from .reserva_cancelada import ReservaCancelada
from .reserva_finalizada import ReservaFinalizada


class ReservaPagada(EstadoReserva):
    
    def __str__(self):
        # Permite imprimir el nombre del estado (Pagada)
        return self.__class__.__name__.replace("Reserva", "") 

    def confirmar_pago(self, reserva):
        print(f"[{reserva.id_reserva}] Advertencia: La reserva ya se encuentra pagada.")

    def cancelar(self, reserva):
        print(f"[{reserva.id_reserva}] Cancelando reserva pagada. Se procesará un reembolso.")
        # Cambia a Cancelada (donde se gestiona el reembolso)
        reserva.cambiar_estado(ReservaCancelada())
        
    def finalizar_turno(self, reserva):
        print(f"[{reserva.id_reserva}] Turno finalizado. Marcando reserva como Finalizada.")
        # Cambia a Finalizada
        reserva.cambiar_estado(ReservaFinalizada())