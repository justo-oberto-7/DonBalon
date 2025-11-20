"""
Script de verificación para el atributo ambito en Estado.
"""
import sys
import os
import sqlite3
from pathlib import Path

# Agregar el directorio padre al path para importar los módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from services.estado_service import EstadoService
from classes.estado import Estado

def verify_ambito():
    print("\n=== Verificando Ambito en Estado ===")
    service = EstadoService()
    
    # Create
    nuevo = Estado(nombre="Estado Test", ambito="test_scope")
    creado = service.insert(nuevo)
    print(f"✓ Creado: {creado}")
    
    if creado.ambito != "test_scope":
        print(f"✗ Error: Ambito esperado 'test_scope', obtenido '{creado.ambito}'")
        return

    # Read
    leido = service.get_by_id(creado.id_estado)
    print(f"✓ Leido: {leido}")
    
    if leido.ambito != "test_scope":
        print(f"✗ Error: Ambito leido esperado 'test_scope', obtenido '{leido.ambito}'")
        return

    # Update
    leido.ambito = "updated_scope"
    service.update(leido)
    
    actualizado = service.get_by_id(leido.id_estado)
    print(f"✓ Actualizado: {actualizado}")
    
    if actualizado.ambito != "updated_scope":
        print(f"✗ Error: Ambito actualizado esperado 'updated_scope', obtenido '{actualizado.ambito}'")
        return
        
    print("✓ Verificación de ambito EXITOSA")

if __name__ == "__main__":
    try:
        verify_ambito()
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
