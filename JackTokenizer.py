from PIL.ImageChops import constant
from numpy.ma.core import append

class JackTokenizer:
    def __init__(self, input_file):
        self.listOfTokens = self.claenFile(input_file)
        self.tokenLength = len(self.listOfTokens)
        self.currentToken = self.listOfTokens[0]
        self.input_file = input_file
        self.currentTokenIndex = 0


    def hasMoreTokens(self):
        """
               This function tells us if we have more tokens to read in the files
               :return - True or false
               """
        return self.currentTokenIndex < self.tokenLength-1

    def advance(self):
        if self.hasMoreTokens():
            self.currentTokenIndex +=1
            self.currentToken = self.listOfTokens[self.currentTokenIndex]

    def claenFile(self, input_file):
        """
        :param input_file:
        :return a list of each word (token) in the file. Takes only the relevant words
        """
        # Open the file and list its contents
        with open('filename.txt', 'r') as file:
            raw_lines = file.readlines()  # Returns a list where each line is an item

        clean_words = []
        for line in raw_lines:
            line = line.strip()  # Remove extra spaces from the ends
            if line and not line.startswith("\\"):  # Ignore empty and comment lines
                words = line.split()  # Split line into words
                clean_words.extend(words)  # Add words to the clean_words list

        return clean_words

    def token_type(self):
        """
        Returns:
            str: KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST as token types
        """

        symbol_type = None
        token = self.currentToken
        if token in ('class', 'constructor', 'function', 'method',
                     'field', 'static', 'var', 'int', 'char', 'if',
                     'boolean', 'void', 'true', 'false', 'null',
                     'this', 'let', 'do', 'return', 'else', 'while'):
            symbol_type = 'KEYWORD'
        elif token in '{}()[].,;+-*/&|<>=~':
            symbol_type = 'SYMBOL'
        elif token.isdigit():
            symbol_type = 'INT_CONST'
        elif token.startswith('"'):
            symbol_type = 'STRING_CONST'
        elif (not token[0].isdigit()):
            symbol_type = 'IDENTIFIER'
        else:
            raise SyntaxError('Invalid token : {}'.format(token))
        return symbol_type


    def keyword(self):
        """
        The function takes the current token
        :return - a constant of the token
        """
        keyword = self.currentToken.upper()
        if keyword in { 'CLASS', 'METHOD', 'FUNCTION', 'CONSTRUCTOR', 'INT', 'BOOLEAN', 'CHAR', 'VOID', 'VAR', 'STATIC', 'FIELD', 'LET', 'DO', 'IF', 'ELSE', 'WHILE', 'RETURN', 'TRUE', 'FALSE',}:
            return keyword

    def symbol(self):
        if self.token_type() == "SYMBOL":
            return self.currentToken





