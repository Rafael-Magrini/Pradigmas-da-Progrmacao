class MiniLanguageSpec:
    """
    Especificação da Mini Linguagem
    
    Esta classe define as características e objetivos da nossa linguagem.
    É uma documentação viva que serve como referência para todo o projeto.
    """
    
    def __init__(self):
        self.name = "MiniLang"
        self.version = "1.0"
        self.description = "Uma mini linguagem para demonstrar conceitos de interpretadores"
        
        # Definindo o público-alvo
        self.target_audience = [
            "Estudantes de Ciência da Computação",
            "Desenvolvedores iniciantes",
            "Pessoas interessadas em linguagens de programação"
        ]
        
        # Casos de uso principais
        self.use_cases = [
            "Cálculos matemáticos simples",
            "Manipulação básica de dados",
            "Aprendizado de programação",
            "Prototipagem rápida de algoritmos"
        ]
        
        # Tipos de dados suportados
        self.supported_types = {
            'int': 'Números inteiros (ex: 42, -10)',
            'float': 'Números decimais (ex: 3.14, -2.5)',
            'string': 'Texto entre aspas (ex: "Hello")',
            'list': 'Listas de elementos (ex: [1, 2, 3])',
            'bool': 'Valores lógicos (True, False)'
        }
        
        # Operadores suportados
        self.operators = {
            '+': 'Adição',
            '-': 'Subtração',
            '*': 'Multiplicação',
            '/': 'Divisão',
            '=': 'Atribuição',
            '==': 'Igualdade',
            '!=': 'Diferença',
            '<': 'Menor que',
            '>': 'Maior que',
            '<=': 'Menor ou igual',
            '>=': 'Maior ou igual'
        }
        
    def get_language_overview(self):
        """Retorna um resumo completo da linguagem"""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'target_audience': self.target_audience,
            'use_cases': self.use_cases,
            'supported_types': self.supported_types,
            'operators': self.operators
        }
    
    def print_specification(self):
        """Imprime a especificação completa da linguagem"""
        print(f"=== {self.name} v{self.version} ===")
        print(f"Descrição: {self.description}\n")
        
        print("Público-alvo:")
        for audience in self.target_audience:
            print(f"  - {audience}")
        
        print("\nCasos de uso:")
        for use_case in self.use_cases:
            print(f"  - {use_case}")
        
        print("\nTipos de dados suportados:")
        for type_name, description in self.supported_types.items():
            print(f"  {type_name}: {description}")
        
        print("\nOperadores:")
        for op, description in self.operators.items():
            print(f"  '{op}': {description}")

# Exemplo de uso da especificação
if __name__ == "__main__":
    # Criando a especificação da linguagem
    spec = MiniLanguageSpec()
    
    # Exibindo a especificação
    spec.print_specification()
    
    print("\n" + "="*50)
    print("DOCUMENTO DE ESPECIFICAÇÃO GERADO")
    print("="*50)
    print("\nEste documento define claramente:")
    print("1. Para que serve a linguagem")
    print("2. Quem vai usar")
    print("3. Que tipos de problemas resolve")
    print("4. Quais recursos oferece")