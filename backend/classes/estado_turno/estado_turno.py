from abc import ABC, abstractmethod

class EstadoTurno(ABC):
    """Interfaz para los objetos de estado de un Turno."""
    
    @abstractmethod
    def reservar(self, turno):
        """Intenta cambiar el estado a No Disponible (reservado)."""
        pass

    @abstractmethod
    def liberar(self, turno):
        """Intenta cambiar el estado a Disponible."""
        pass

    def __str__(self):
        """Devuelve la representación serializable del estado."""
        # Esto nos da 'Disponible' o 'NoDisponible'
        return self.__class__.__name__.replace("Turno", "")