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
        This function takes a file and makes from it a list of tokens
        :return: A list of tokens from the file
        """
        keywords = {'class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char',
                    'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return'}
        symbols = set('{}()[].,;+-*/&|<>=~')
        tokens = []

        with open(input_file, 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith("//"):  # Ignore empty lines and comments
                continue

            # Split the line into "words" by spaces, but process each word for symbols and string constants
            words = line.split()  # Split the line into words
            for word in words:
                current_token = ""
                inside_string = False

                for char in word:
                    if inside_string:  # Handle string constants
                        if char == '"':  # End of the string constant
                            current_token += char
                            tokens.append(current_token)  # Add the full string constant
                            current_token = ""
                            inside_string = False
                        else:
                            current_token += char
                    elif char == '"':  # Start of a string constant
                        if current_token:  # Add any existing token before the string starts
                            tokens.append(current_token)
                            current_token = ""
                        current_token += char
                        inside_string = True
                    elif char in symbols:  # Handle symbols
                        if current_token:  # Add the current token before the symbol
                            tokens.append(current_token)
                            current_token = ""
                        tokens.append(char)  # Add the symbol as its own token
                    else:  # Build the token (keywords, identifiers, numbers)
                        current_token += char

                if current_token:  # Add the last token in the word if it exists
                    tokens.append(current_token)

        return tokens


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


    def keyWord(self):
        return self.currentToken

    def symbol(self):
        return self.currentToken

    def identifier(self):
        return self.currentToken

    def intVal(self):
        return int(self.currentToken)

    def stringVal(self):
        return self.currentToken







