from .estado_turno import EstadoTurno

class TurnoDisponible(EstadoTurno):
    
    def reservar(self, turno):
        """Permite la transición a No Disponible."""
        from .turno_no_disponible import TurnoNoDisponible
        print(f"[Turno {turno.id_turno}] Marcado como No Disponible (Reservado).")
        turno.cambiar_estado(TurnoNoDisponible())

    def liberar(self, turno):
        """Ya está disponible, no hay cambio."""
        print(f"[Turno {turno.id_turno}] Advertencia: El turno ya está Disponible.")
        pass