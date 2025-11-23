from .estado_turno import EstadoTurno
# Las importaciones circulares se evitan importando dentro de los métodos


class TurnoNoDisponible(EstadoTurno):
    
    def reservar(self, turno):
        """Ya está reservado, no hay cambio."""
        print(f"[Turno {turno.id_turno}] Advertencia: El turno ya está No Disponible.")
        pass

    def liberar(self, turno):
        """Permite la transición a Disponible."""
        from .turno_disponible import TurnoDisponible
        print(f"[Turno {turno.id_turno}] Marcado como Disponible (Liberado).")
        turno.cambiar_estado(TurnoDisponible())