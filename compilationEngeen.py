from JackTokenizer import JackTokenizer

class compilationEngeen:
    def _init_(self, input_file_path, output_path):
        """
        :param fileToRead:
        """
        self.indent_level = 0
        self.tokenizer = JackTokenizer(input_file_path)
        self.output = open(output_path, "w+")

    def write_element(self, tag, value):
        """Writes an XML element with the given tag and value."""
        indent = '  ' * self.indent_level
        self.output.write(f'{indent}<{tag}> {value} </{tag}>\n')

    def write_xml_tag(self, tag):
        """Writes an XML tag, handling indentation for nested structures."""
        indent = '  ' * self.indent_level
        if tag.startswith('/'):  # Closing tag
            self.indent_level -= 1
            indent = '  ' * self.indent_level
            self.output.write(f'{indent}<{tag}>\n')
        else:  # Opening tag
            self.output.write(f'{indent}<{tag}>\n')
            self.indent_level += 1


    def write_current_token(self):
        """Writes the current token to the output file with appropriate XML tags."""
        token_type = self.tokenizer.token_type()
        if token_type == 'KEYWORD':
            self.write_element('keyword', self.tokenizer.keyWord())
        elif token_type == 'SYMBOL':
            symbol = self.tokenizer.symbol()
            # Handle special XML characters
            if symbol == '<':
                symbol = '&lt;'
            elif symbol == '>':
                symbol = '&gt;'
            elif symbol == '&':
                symbol = '&amp;'
            self.write_element('symbol', symbol)
        elif token_type == 'IDENTIFIER':
            self.write_element('identifier', self.tokenizer.identifier())
        elif token_type == 'INT_CONST':
            self.write_element('integerConstant', str(self.tokenizer.intVal()))
        elif token_type == 'STRING_CONST':
            self.write_element('stringConstant', self.tokenizer.stringVal())



    def compile_term(self):
        """Compiles a term. Terms can be:
        - integerConstant
        - stringConstant
        - keywordConstant (true/false/null/this)
        - varName
        - varName[expression]
        - subroutineCall
        - (expression)
        - unaryOp term
        """
        self.write_xml_tag('term')  # Start the term XML block

        if self.tokenizer.token_type() == 'INT_CONST':
            # Handle integer constants (like "42")
            self.write_current_token()
            self.tokenizer.advance()

        elif self.tokenizer.token_type() == 'STRING_CONST':
            # Handle string constants (like "hello")
            self.write_current_token()
            self.tokenizer.advance()

        elif self.tokenizer.token_type() == 'KEYWORD':
            # Handle keyword constants (true/false/null/this)
            self.write_current_token()
            self.tokenizer.advance()

        elif self.tokenizer.token_type() == 'IDENTIFIER':
            # 1. A simple variable (like "x")
            # 2. An array access (like "arr[5]")
            # 3. A subroutine call (like "foo()" or "obj.foo()")
            self.write_current_token()  # Write the identifier
            self.tokenizer.advance()

            # Look at the next token to determine what kind of term this is
            if self.tokenizer.token_type() == 'SYMBOL':
                if self.tokenizer.symbol() == '[':  # Array access
                    # Handle array access like arr[expression]
                    self.write_current_token()  # Write '['
                    self.tokenizer.advance()
                    self.compile_expression()  # Compile the index expression
                    if self.tokenizer.symbol() == ']':
                        self.write_current_token()  # Write ']'
                        self.tokenizer.advance()

                elif self.tokenizer.symbol() in '(.':  # Subroutine call
                    # Handle either:
                    # - direct call like foo()
                    # - method call like obj.foo()
                    self.compile_subroutine_call_continuation()

        elif self.tokenizer.token_type() == 'SYMBOL':
            if self.tokenizer.symbol() == '(':  # Parenthesized expression
                # Handle (expression)
                self.write_current_token()  # Write '('
                self.tokenizer.advance()
                self.compile_expression()
                if self.tokenizer.symbol() == ')':
                    self.write_current_token()  # Write ')'
                    self.tokenizer.advance()

            elif self.tokenizer.symbol() in '-~':  # Unary operator
                # Handle unary operations like -x or ~bool
                self.write_current_token()  # Write the operator
                self.tokenizer.advance()
                self.compile_term()  # Compile the term after the operator

        self.write_xml_tag('/term')  # End the term XML block



    def compile_expression(self):
        """Compiles an expression."""
        self.write_xml_tag('expression')
        # First term
        self.compile_term()
        # Dealing with a few symbols such as +=
        while self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() in '+-*/&|<>=':
            self.write_current_token()  # Write operator
            self.tokenizer.advance()
            self.compile_term()

        self.write_xml_tag('/expression')

    def compile_subroutine(self):
        """Compiles a complete method, function, or constructor."""
        self.write_xml_tag('subroutineDec')

        # Subroutine type (constructor/function/method)
        self.write_current_token()
        self.tokenizer.advance()

        # Return type
        self.write_current_token()
        self.tokenizer.advance()

        # Subroutine name
        self.write_current_token()
        self.tokenizer.advance()

        # Parameter list
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == '(':
            self.write_current_token()
            self.tokenizer.advance()
            self.compile_parameter_list()

            if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == ')':
                self.write_current_token()
                self.tokenizer.advance()

        # Subroutine body
        self.compile_subroutine_body()

        self.write_xml_tag('/subroutineDec')

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list. Does not handle the enclosing parentheses."""
        self.write_xml_tag('parameterList')

        while self.tokenizer.token_type() != 'SYMBOL' or self.tokenizer.symbol() != ')':
            # Type
            self.write_current_token()
            self.tokenizer.advance()

            # Parameter name
            self.write_current_token()
            self.tokenizer.advance()

            # Check for more parameters
            if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == ',':
                self.write_current_token()
                self.tokenizer.advance()

        self.write_xml_tag('/parameterList')


    def compile_subroutine_body(self):
        """Compiles a subroutine's body"""
        self.write_xml_tag('subroutineBody')

        # Opening brace
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == '{':
            self.write_current_token()
            self.tokenizer.advance()

            # Variable declarations
            while self.tokenizer.token_type() == 'KEYWORD' and self.tokenizer.keyWord() == 'var':
                self.compile_var_dec()

            # Statements
            self.compile_statements()

            # Closing brace
            if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == '}':
                self.write_current_token()
                self.tokenizer.advance()

        self.write_xml_tag('/subroutineBody')

    def compile_var_dec(self):
        """Compiles a var declaration."""
        self.write_xml_tag('varDec')

        # 'var' keyword
        self.write_current_token()
        self.tokenizer.advance()

        # Type
        self.write_current_token()
        self.tokenizer.advance()

        # Variable names (comma-separated)
        while True:
            self.write_current_token()  # Variable name
            self.tokenizer.advance()

            if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == ',':
                self.write_current_token()
                self.tokenizer.advance()
            else:
                break

        # Semicolon
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == ';':
            self.write_current_token()
            self.tokenizer.advance()

        self.write_xml_tag('/varDec')


    def compile_return(self):
        """Compiles a return statement."""
        self.write_xml_tag('returnStatement')

        # 'return' keyword
        self.write_current_token()
        self.tokenizer.advance()

        # Optional expression
        if not (self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == ';'):
            self.compile_expression()

        # Semicolon
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == ';':
            self.write_current_token()
            self.tokenizer.advance()

        self.write_xml_tag('/returnStatement')

    def compile_do(self):
        """Compiles a do statement.
        Structure:
        'do' subroutineCall ';'
        """
        self.write_xml_tag('doStatement')

        # Write 'do' keyword
        self.write_current_token()  # writes "do"
        self.tokenizer.advance()

        # Handle subroutine call
        # Write subroutine name or object/class name
        self.write_current_token()  # writes identifier (subroutine name or object/class name)
        self.tokenizer.advance()

        # Handle possible dot operator for method calls
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == '.':
            self.write_current_token()  # writes '.'
            self.tokenizer.advance()
            self.write_current_token()  # writes method name
            self.tokenizer.advance()

        # Handle parameter list
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == '(':
            self.write_current_token()  # writes '('
            self.tokenizer.advance()

            # Compile the expression list (parameters)
            self.compile_expression_list()

            # Write closing parenthesis
            if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == ')':
                self.write_current_token()  # writes ')'
                self.tokenizer.advance()

        # Handle semicolon at end of statement
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == ';':
            self.write_current_token()  # writes ';'
            self.tokenizer.advance()

        self.write_xml_tag('/doStatement')

    def compile_while(self):
        """Compiles a while statement."""
        self.write_xml_tag('whileStatement')

        # 'while' keyword
        self.write_current_token()
        self.tokenizer.advance()

        # Opening parenthesis
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == '(':
            self.write_current_token()
            self.tokenizer.advance()

        # Condition
        self.compile_expression()

        # Closing parenthesis
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == ')':
            self.write_current_token()
            self.tokenizer.advance()

        # Opening brace
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == '{':
            self.write_current_token()
            self.tokenizer.advance()

        # While body statements
        self.compile_statements()

        # Closing brace
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == '}':
            self.write_current_token()
            self.tokenizer.advance()

        self.write_xml_tag('/whileStatement')

    def compile_if(self):
        """Compiles an if statement, possibly with a trailing else clause."""
        self.write_xml_tag('ifStatement')

        # 'if' keyword
        self.write_current_token()
        self.tokenizer.advance()

        # Opening parenthesis
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == '(':
            self.write_current_token()
            self.tokenizer.advance()

        # Condition
        self.compile_expression()

        # Closing parenthesis
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == ')':
            self.write_current_token()
            self.tokenizer.advance()

        # Opening brace
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == '{':
            self.write_current_token()
            self.tokenizer.advance()

        # If body statements
        self.compile_statements()

        # Closing brace
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == '}':
            self.write_current_token()
            self.tokenizer.advance()

        # Optional else clause
        if self.tokenizer.token_type() == 'KEYWORD' and self.tokenizer.keyWord() == 'else':
            self.write_current_token()
            self.tokenizer.advance()

            # Opening brace
            if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == '{':
                self.write_current_token()
                self.tokenizer.advance()

            # Else body statements
            self.compile_statements()

            # Closing brace
            if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == '}':
                self.write_current_token()
                self.tokenizer.advance()

        self.write_xml_tag('/ifStatement')

    def compile_let(self):
        """Compiles a let statement."""
        self.write_xml_tag('letStatement')

        # 'let' keyword
        self.write_current_token()
        self.tokenizer.advance()

        # Variable name
        self.write_current_token()
        self.tokenizer.advance()

        # Optional array indexing
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == '[':
            self.write_current_token()
            self.tokenizer.advance()
            self.compile_expression()

            if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == ']':
                self.write_current_token()
                self.tokenizer.advance()

        # '=' symbol
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == '=':
            self.write_current_token()
            self.tokenizer.advance()

        # Expression
        self.compile_expression()

        # Semicolon
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == ';':
            self.write_current_token()
            self.tokenizer.advance()

        self.write_xml_tag('/letStatement')


    def compile_statements(self):
        """Compiles a sequence of statements. Does not handle the enclosing curly brackets."""
        self.write_xml_tag('statements')

        while self.tokenizer.token_type() == 'KEYWORD':
            keyword = self.tokenizer.keyWord()
            if keyword == 'let':
                self.compile_let()
            elif keyword == 'if':
                self.compile_if()
            elif keyword == 'while':
                self.compile_while()
            elif keyword == 'do':
                self.compile_do()
            elif keyword == 'return':
                self.compile_return()
            else:
                break

        self.write_xml_tag('/statements')

    def compile_class_var_dec(self):
        """Compiles a static variable declaration or field declaration.
        """
        self.write_xml_tag('classVarDec')

        # Write static/field
        self.write_current_token()  # writes 'static' or 'field'
        self.tokenizer.advance()

        # Type (int, char, boolean, or className)
        self.write_current_token()  # writes type
        self.tokenizer.advance()

        # Variable names (comma-separated)
        while True:
            # Write variable name
            self.write_current_token()  # writes variable name
            self.tokenizer.advance()

            # Check for more variables (comma)
            if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == ',':
                self.write_current_token()  # writes comma
                self.tokenizer.advance()
            else:
                break

        # Semicolon
        if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == ';':
            self.write_current_token()  # writes semicolon
            self.tokenizer.advance()

        self.write_xml_tag('/classVarDec')

    def compile_class(self):
        """Compiles a complete class."""
        # Start with 'class' keyword
        if self.tokenizer.token_type() == 'KEYWORD' and self.tokenizer.keyWord() == 'class':
            self.write_xml_tag('class')
            self.write_current_token()  # Write 'class'
            self.tokenizer.advance()

            # Class name (identifier)
            if self.tokenizer.token_type() == 'IDENTIFIER':
                self.write_current_token()
                self.tokenizer.advance()

                # Opening brace
                if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == '{':
                    self.write_current_token()
                    self.tokenizer.advance()

                    # Compile class var declarations and subroutines
                    while self.tokenizer.token_type() == 'KEYWORD':
                        if self.tokenizer.keyWord() in ['static', 'field']:
                            self.compile_class_var_dec()
                        elif self.tokenizer.keyWord() in ['constructor', 'function', 'method']:
                            self.compile_subroutine()

                    # Closing brace
                    if self.tokenizer.token_type() == 'SYMBOL' and self.tokenizer.symbol() == '}':
                        self.write_current_token()

            self.write_xml_tag('/class')
