from models.usuario import Usuario
from datetime import date

try:
    print("=== Teste 1: Criar usuário básico ===")
    usuario = Usuario(vem_hash="teste123")
    print("✅ Usuário criado!")
    print(f"Hash: {usuario.vem_hash}")
    print(f"Pontuação: {usuario.pontuacao}")
    print(f"Cadastro completo: {usuario.cadastro_completo}")
    
    print("\n=== Teste 2: Model dump ===")
    dados = usuario.model_dump()
    print("✅ Model dump funcionou!")
    print(dados)
    
    print("\n=== Teste 3: Model dump (mode='json') ===")
    dados_json = usuario.model_dump(mode='json')
    print("✅ Model dump JSON funcionou!")
    print(dados_json)
    
    print("\n=== Teste 4: Criar usuário completo ===")
    usuario2 = Usuario(
        vem_hash="teste456",
        nome="João Silva",
        email="joao@test.com",
        data_nascimento=date(1995, 5, 15)
    )
    print("✅ Usuário completo criado!")
    print(usuario2.model_dump())
    
    print("\n=== Teste 5: Calcular idade ===")
    idade = usuario2.calcular_idade()
    print(f"✅ Idade calculada: {idade} anos")
    
    print("\n✅✅✅ TODOS OS TESTES PASSARAM! ✅✅✅")
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()