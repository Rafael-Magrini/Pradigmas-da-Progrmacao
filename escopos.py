from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class Variable:
    """
    Representa uma variável com suas propriedades
    
    Attributes:
        name: nome da variável
        value: valor atual
        var_type: tipo da variável (int, float, string, list)
        is_constant: se é constante (não pode ser alterada)
        line_declared: linha onde foi declarada (para debug)
    """
    name: str
    value: Any
    var_type: str
    is_constant: bool = False
    line_declared: int = 1
    
    def __str__(self):
        const_str = " (const)" if self.is_constant else ""
        return f"{self.name}: {self.var_type} = {self.value}{const_str}"

class Scope:
    """
    Representa um escopo (contexto de variáveis)
    
    Um escopo é um "ambiente" onde variáveis existem.
    Cada bloco de código (função, if, while) pode ter seu próprio escopo.
    """
    
    def __init__(self, name: str, parent: Optional['Scope'] = None):
        self.name = name
        self.parent = parent  # escopo pai (para busca hierárquica)
        self.variables: Dict[str, Variable] = {}  # variáveis deste escopo
        self.children: List['Scope'] = []  # escopos filhos
        
        if parent:
            parent.children.append(self)
    
    def define_variable(self, name: str, value: Any, var_type: str = None, 
                       is_constant: bool = False, line: int = 1) -> Variable:
        """
        Define uma nova variável neste escopo
        
        Args:
            name: nome da variável
            value: valor inicial
            var_type: tipo da variável (inferido se None)
            is_constant: se é constante
            line: linha onde foi declarada
        
        Returns:
            Variable: a variável criada
        
        Raises:
            NameError: se variável já existe neste escopo
        """
        if name in self.variables:
            existing = self.variables[name]
            raise NameError(f"Variável '{name}' já foi definida na linha {existing.line_declared}")
        
        # Inferir tipo se não especificado
        if var_type is None:
            if isinstance(value, int):
                var_type = "int"
            elif isinstance(value, float):
                var_type = "float"
            elif isinstance(value, str):
                var_type = "string"
            elif isinstance(value, list):
                var_type = "list"
            elif isinstance(value, bool):
                var_type = "bool"
            else:
                var_type = "unknown"
        
        variable = Variable(name, value, var_type, is_constant, line)
        self.variables[name] = variable
        return variable
    
    def get_variable(self, name: str) -> Optional[Variable]:
        """
        Busca uma variável neste escopo ou nos escopos pai
        
        Implementa a regra de escopo lexical:
        1. Procura no escopo atual
        2. Se não encontrar, procura no escopo pai
        3. Continua subindo até encontrar ou chegar ao escopo global
        
        Args:
            name: nome da variável
        
        Returns:
            Variable ou None se não encontrada
        """
        # Primeiro procura no escopo atual
        if name in self.variables:
            return self.variables[name]
        
        # Se não encontrou e tem escopo pai, procura lá
        if self.parent:
            return self.parent.get_variable(name)
        
        # Não encontrou em lugar nenhum
        return None
    
    def set_variable(self, name: str, value: Any, line: int = 1) -> bool:
        """
        Atribui valor a uma variável existente
        
        Args:
            name: nome da variável
            value: novo valor
            line: linha da atribuição (para mensagens de erro)
        
        Returns:
            bool: True se conseguiu atribuir, False se variável não existe
        
        Raises:
            ValueError: se tentar alterar constante
            TypeError: se tipo incompatível
        """
        variable = self.get_variable(name)
        
        if not variable:
            return False
        
        # Verifica se é constante
        if variable.is_constant:
            raise ValueError(f"Não é possível alterar constante '{name}' (linha {line})")
        
        # Verifica compatibilidade de tipos (opcional, pode ser relaxado)
        new_type = type(value).__name__
        if new_type == "int" and variable.var_type == "float":
            value = float(value)  # conversão automática int -> float
        elif new_type != variable.var_type.replace("string", "str"):
            print(f"Aviso: Mudando tipo de '{name}' de {variable.var_type} para {new_type}")
        
        variable.value = value
        return True
    
    def list_variables(self, include_parent: bool = False) -> List[Variable]:
        """
        Lista todas as variáveis do escopo
        
        Args:
            include_parent: se deve incluir variáveis dos escopos pai
        
        Returns:
            List[Variable]: lista de variáveis
        """
        variables = list(self.variables.values())
        
        if include_parent and self.parent:
            variables.extend(self.parent.list_variables(include_parent))
        
        return variables
    
    def __str__(self):
        vars_str = ", ".join([f"{name}={var.value}" for name, var in self.variables.items()])
        return f"Scope({self.name}): [{vars_str}]"

class ScopeManager:
    """
    Gerenciador de escopos
    
    Controla a criação e destruição de escopos durante a execução.
    Mantém uma pilha de escopos ativos.
    """
    
    def __init__(self):
        # Escopo global
    print("1. Definindo variável no escopo global:")
    manager.define_variable("x", 10, line=1)
    print(f"   x = {manager.get_variable('x').value}")
    print(f"   Escopos ativos:\n{manager.get_scope_info()}\n")
    
    # Entrando em escopo de bloco if
    print("2. Entrando em escopo 'if' (x > 5):")
    manager.enter_scope("if_block")
    
    # Definindo variável local
    manager.define_variable("y", 20, line=3)
    print(f"   y = {manager.get_variable('y').value} (local)")
    
    # Modificando variável global
    manager.set_variable("x", 15, line=4)
    print(f"   x = {manager.get_variable('x').value} (modificou global)")
    print(f"   Escopos ativos:\n{manager.get_scope_info()}\n")
    
    # Escopo aninhado
    print("3. Entrando em escopo aninhado 'if' (y > 10):")
    manager.enter_scope("nested_if")
    
    manager.define_variable("z", 30, line=6)
    print(f"   z = {manager.get_variable('z').value} (mais local)")
    
    # Testando acesso a variáveis de escopos superiores
    print(f"   Acessando x: {manager.get_variable('x').value} (do global)")
    print(f"   Acessando y: {manager.get_variable('y').value} (do pai)")
    print(f"   Escopos ativos:\n{manager.get_scope_info()}\n")
    
    # Saindo dos escopos
    print("4. Saindo do escopo aninhado:")
    manager.exit_scope()
    
    # z não deve mais estar acessível
    z_var = manager.get_variable("z")
    print(f"   z acessível? {z_var is not None}")
    print(f"   y ainda acessível: {manager.get_variable('y').value}")
    print(f"   Escopos ativos:\n{manager.get_scope_info()}\n")
    
    print("5. Saindo do escopo 'if':")
    manager.exit_scope()
    
    # y não deve mais estar acessível
    y_var = manager.get_variable("y")
    print(f"   y acessível? {y_var is not None}")
    print(f"   x ainda acessível: {manager.get_variable('x').value}")
    print(f"   Escopos ativos:\n{manager.get_scope_info()}\n")
    
    # Testando constantes
    print("6. Testando constantes:")
    try:
        manager.define_variable("PI", 3.14159, is_constant=True, line=10)
        print(f"   PI = {manager.get_variable('PI').value} (constante)")
        
        # Tentando modificar constante (deve dar erro)
        manager.set_variable("PI", 3.14, line=11)
    except ValueError as e:
        print(f"   Erro esperado: {e}")
    
    # Testando redefinição de variável
    print("\n7. Testando redefinição de variável:")
    try:
        manager.define_variable("x", 25, line=12)
    except NameError as e:
        print(f"   Erro esperado: {e}")
    
    print("\n=== RESUMO DO SISTEMA DE ESCOPOS ===")
    print("✓ Variáveis podem ser definidas em diferentes escopos")
    print("✓ Busca hierárquica: local -> pai -> avô -> ... -> global")
    print("✓ Variáveis locais 'escondem' globais com mesmo nome")
    print("✓ Constantes não podem ser modificadas")
    print("✓ Não pode redefinir variável no mesmo escopo")
    print("✓ Variáveis são destruídas ao sair do escopo")

# Exemplo prático de avaliação de escopo
def evaluate_scope_example():
    """
    Exemplo prático: avaliação correta de variáveis em funções
    
    Simula este código:
    
    x = 100
    
    def funcao():
        x = 50      # variável local
        y = x + 10  # usa x local
        return y
    
    resultado = funcao()  # resultado = 60
    print(x)             # imprime 100 (global não foi alterado)
    """
    print("\n=== EXEMPLO PRÁTICO: FUNÇÃO COM ESCOPO LOCAL ===")
    
    manager = ScopeManager()
    
    # Variável global
    manager.define_variable("x", 100)
    print(f"Global: x = {manager.get_variable('x').value}")
    
    # Simulando entrada em função
    print("\nEntrando na função:")
    manager.enter_scope("function")
    
    # Variável local com mesmo nome
    manager.define_variable("x", 50)  # Esta é uma nova variável!
    manager.define_variable("y", manager.get_variable("x").value + 10)
    
    print(f"Local: x = {manager.get_variable('x').value}")
    print(f"Local: y = {manager.get_variable('y').value}")
    
    # Saindo da função
    print("\nSaindo da função:")
    manager.exit_scope()
    
    # Verificando que global não foi alterado
    print(f"Global: x = {manager.get_variable('x').value} (não alterado!)")
    
    # y não existe mais
    y_exists = manager.get_variable("y") is not None
    print(f"y ainda existe? {y_exists}")

if __name__ == "__main__":
    test_scope_system()
    evaluate_scope_example()
    
    print("\n" + "="*50)
    print("PRÓXIMO PASSO: Implementar tipos de dados (Capítulo 6)")
    print("="*50)opo global sempre existe
        self.global_scope = Scope("global")
        self.current_scope = self.global_scope
        self.scope_stack = [self.global_scope]
    
    def enter_scope(self, name: str) -> Scope:
        """
        Entra em um novo escopo (cria escopo filho)
        
        Args:
            name: nome do novo escopo
        
        Returns:
            Scope: o novo escopo criado
        """
        new_scope = Scope(name, self.current_scope)
        self.current_scope = new_scope
        self.scope_stack.append(new_scope)
        return new_scope
    
    def exit_scope(self) -> Optional[Scope]:
        """
        Sai do escopo atual (volta para o escopo pai)
        
        Returns:
            Scope: o escopo que foi abandonado, ou None se já no global
        """
        if len(self.scope_stack) <= 1:
            return None  # Não pode sair do escopo global
        
        old_scope = self.scope_stack.pop()
        self.current_scope = self.scope_stack[-1]
        return old_scope
    
    def define_variable(self, name: str, value: Any, **kwargs) -> Variable:
        """Define variável no escopo atual"""
        return self.current_scope.define_variable(name, value, **kwargs)
    
    def get_variable(self, name: str) -> Optional[Variable]:
        """Busca variável no escopo atual (e pais)"""
        return self.current_scope.get_variable(name)
    
    def set_variable(self, name: str, value: Any, line: int = 1) -> bool:
        """Atribui valor a variável existente"""
        return self.current_scope.set_variable(name, value, line)
    
    def get_scope_info(self) -> str:
        """Retorna informações sobre os escopos ativos"""
        info = []
        for i, scope in enumerate(self.scope_stack):
            indent = "  " * i
            info.append(f"{indent}{scope}")
        return "\n".join(info)

# Função de exemplo para testar o sistema de escopos
def test_scope_system():
    """
    Demonstra o funcionamento do sistema de escopos
    
    Simula a execução de código com diferentes escopos:
    
    x = 10          # escopo global
    if x > 5:       # novo escopo
        y = 20      # variável local
        x = 15      # modifica global
        if y > 10:  # escopo aninhado
            z = 30  # variável mais local ainda
    """
    print("=== TESTE DO SISTEMA DE ESCOPOS ===\n")
    
    manager = ScopeManager()
    
    # Esc