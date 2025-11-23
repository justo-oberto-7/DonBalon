from abc import ABC, abstractmethod

class EstadoReserva(ABC):
    """
    Interfaz para todos los estados concretos de Reserva.
    Define las acciones que pueden ocurrir.
    """
    
    @abstractmethod
    def confirmar_pago(self, reserva):
        pass
        
    @abstractmethod
    def cancelar(self, reserva):
        pass
        
    @abstractmethod
    def finalizar_turno(self, reserva):
        pass
        
    def __str__(self):
        # Permite imprimir el nombre del estado
        return self.__class__.__name__.replace("Reserva", "")