import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Any

# Definindo os tipos de tokens que nossa linguagem reconhece
class TokenType(Enum):
    # Literais
    NUMBER = "NUMBER"          # 123, 3.14
    STRING = "STRING"          # "hello"
    IDENTIFIER = "IDENTIFIER"  # variáveis, nomes
    
    # Operadores aritméticos
    PLUS = "PLUS"             # +
    MINUS = "MINUS"           # -
    MULTIPLY = "MULTIPLY"     # *
    DIVIDE = "DIVIDE"         # /
    
    # Operadores de comparação
    EQUAL = "EQUAL"           # ==
    NOT_EQUAL = "NOT_EQUAL"   # !=
    LESS_THAN = "LESS_THAN"   # <
    GREATER_THAN = "GREATER_THAN" # >
    LESS_EQUAL = "LESS_EQUAL"     # <=
    GREATER_EQUAL = "GREATER_EQUAL" # >=
    
    # Operador de atribuição
    ASSIGN = "ASSIGN"         # =
    
    # Delimitadores
    LEFT_PAREN = "LEFT_PAREN"   # (
    RIGHT_PAREN = "RIGHT_PAREN" # )
    LEFT_BRACKET = "LEFT_BRACKET"   # [
    RIGHT_BRACKET = "RIGHT_BRACKET" # ]
    COMMA = "COMMA"           # ,
    
    # Palavras-chave
    IF = "IF"
    WHILE = "WHILE"
    FOR = "FOR"
    PRINT = "PRINT"
    
    # Controle
    NEWLINE = "NEWLINE"       # \n
    EOF = "EOF"               # fim do arquivo
    WHITESPACE = "WHITESPACE" # espaços, tabs

@dataclass
class Token:
    """
    Representa um token (unidade léxica) do código
    
    Cada token contém:
    - type: que tipo de token é (número, operador, etc.)
    - value: o valor original do código
    - line: em que linha do código está
    - column: em que coluna da linha está
    """
    type: TokenType
    value: str
    line: int
    column: int
    
    def __str__(self):
        return f"Token({self.type.value}, '{self.value}', {self.line}:{self.column})"

class Lexer:
    """
    Analisador Léxico (Lexer)
    
    Responsável por transformar o código fonte (string) em uma lista de tokens.
    É o primeiro passo na análise de qualquer linguagem de programação.
    
    Processo:
    1. Lê o código caractere por caractere
    2. Identifica padrões (números, palavras, operadores)
    3. Cria tokens correspondentes
    4. Retorna lista de tokens para o parser
    """
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0  # posição atual no texto
        self.line = 1 # linha atual
        self.column = 1 # coluna atual
        
        # Palavras-chave da linguagem
        self.keywords = {
            'if': TokenType.IF,
            'while': TokenType.WHILE,
            'for': TokenType.FOR,
            'print': TokenType.PRINT,
        }
    
    def current_char(self) -> Optional[str]:
        """Retorna o caractere atual ou None se chegou ao fim"""
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Olha para frente sem avançar a posição"""
        peek_pos = self.pos + offset
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def advance(self):
        """Avança para o próximo caractere"""
        if self.pos < len(self.text) and self.text[self.pos] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
    
    def skip_whitespace(self):
        """Pula espaços em branco (exceto quebras de linha)"""
        while self.current_char() and self.current_char() in ' \t':
            self.advance()
    
    def read_number(self) -> Token:
        """
        Lê um número (inteiro ou decimal)
        
        Exemplos: 123, 3.14, -42
        """
        start_column = self.column
        result = ""
        
        # Lê dígitos antes do ponto decimal
        while self.current_char() and self.current_char().isdigit():
            result += self.current_char()
            self.advance()
        
        # Verifica se há ponto decimal
        if self.current_char() == '.':
            result += self.current_char()
            self.advance()
            
            # Lê dígitos após o ponto decimal
            while self.current_char() and self.current_char().isdigit():
                result += self.current_char()
                self.advance()
        
        return Token(TokenType.NUMBER, result, self.line, start_column)
    
    def read_string(self) -> Token:
        """
        Lê uma string entre aspas
        
        Exemplo: "Hello, World!"
        """
        start_column = self.column
        quote_char = self.current_char()  # ' ou "
        result = ""
        
        self.advance()  # pula a aspa inicial
        
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':  # escape sequences
                self.advance()
                if self.current_char() == 'n':
                    result += '\n'
                elif self.current_char() == 't':
                    result += '\t'
                elif self.current_char() == '\\':
                    result += '\\'
                elif self.current_char() == quote_char:
                    result += quote_char
                else:
                    result += self.current_char()
            else:
                result += self.current_char()
            self.advance()
        
        if self.current_char() == quote_char:
            self.advance()  # pula a aspa final
        else:
            raise SyntaxError(f"String não fechada na linha {self.line}, coluna {start_column}")
        
        return Token(TokenType.STRING, result, self.line, start_column)
    
    def read_identifier(self) -> Token:
        """
        Lê um identificador (nome de variável ou palavra-chave)
        
        Exemplos: x, nome_variavel, if, while
        """
        start_column = self.column
        result = ""
        
        # Primeiro caractere deve ser letra ou _
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() == '_')):
            result += self.current_char()
            self.advance()
        
        # Verifica se é palavra-chave
        token_type = self.keywords.get(result, TokenType.IDENTIFIER)
        
        return Token(token_type, result, self.line, start_column)
    
    def tokenize(self) -> List[Token]:
        """
        Método principal que converte todo o texto em tokens
        
        Retorna uma lista de tokens que representa o código fonte
        """
        tokens = []
        
        while self.current_char():
            # Pula espaços em branco
            if self.current_char() in ' \t':
                self.skip_whitespace()
                continue
            
            # Quebra de linha
            if self.current_char() == '\n':
                tokens.append(Token(TokenType.NEWLINE, '\\n', self.line, self.column))
                self.advance()
                continue
            
            # Números
            if self.current_char().isdigit():
                tokens.append(self.read_number())
                continue
            
            # Strings
            if self.current_char() in '"\'':
                tokens.append(self.read_string())
                continue
            
            # Identificadores e palavras-chave
            if self.current_char().isalpha() or self.current_char() == '_':
                tokens.append(self.read_identifier())
                continue
            
            # Operadores de dois caracteres
            if self.current_char() == '=' and self.peek_char() == '=':
                tokens.append(Token(TokenType.EQUAL, '==', self.line, self.column))
                self.advance()
                self.advance()
                continue
            
            if self.current_char() == '!' and self.peek_char() == '=':
                tokens.append(Token(TokenType.NOT_EQUAL, '!=', self.line, self.column))
                self.advance()
                self.advance()
                continue
            
            if self.current_char() == '<' and self.peek_char() == '=':
                tokens.append(Token(TokenType.LESS_EQUAL, '<=', self.line, self.column))
                self.advance()
                self.advance()
                continue
            
            if self.current_char() == '>' and self.peek_char() == '=':
                tokens.append(Token(TokenType.GREATER_EQUAL, '>=', self.line, self.column))
                self.advance()
                self.advance()
                continue
            
            # Operadores de um caractere
            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '=': TokenType.ASSIGN,
                '<': TokenType.LESS_THAN,
                '>': TokenType.GREATER_THAN,
                '(': TokenType.LEFT_PAREN,
                ')': TokenType.RIGHT_PAREN,
                '[': TokenType.LEFT_BRACKET,
                ']': TokenType.RIGHT_BRACKET,
                ',': TokenType.COMMA,
            }
            
            if self.current_char() in single_char_tokens:
                token_type = single_char_tokens[self.current_char()]
                tokens.append(Token(token_type, self.current_char(), self.line, self.column))
                self.advance()
                continue
            
            # Caractere não reconhecido
            raise SyntaxError(f"Caractere não reconhecido '{self.current_char()}' na linha {self.line}, coluna {self.column}")
        
        # Adiciona token de fim de arquivo
        tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return tokens

# Exemplo de uso e teste
if __name__ == "__main__":
    # Código de exemplo para testar
    code = '''
    x = 2 + 3
    y = x * 4
    name = "João"
    if x > 0:
        print("Número positivo")
    '''
    
    print("=== ANÁLISE LÉXICA ===")
    print(f"Código fonte:\n{code}")
    print("\nTokens gerados:")
    print("-" * 40)
    
    # Criando o lexer e tokenizando
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Exibindo cada token
    for token in tokens:
        if token.type != TokenType.NEWLINE:  # Não mostra quebras de linha para clareza
            print(token)
    
    print(f"\nTotal de tokens: {len(tokens)}")