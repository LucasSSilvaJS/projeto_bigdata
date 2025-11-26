from core.services.usuario_service import UsuarioService

try:
    print("=== Testando UsuarioService ===")
    service = UsuarioService()
    
    print("\n1. Verificando usuário...")
    resultado = service.verificar_usuario("teste_service_123")
    print(f"✅ Verificar usuário funcionou!")
    print(f"Resultado: {resultado}")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()