from JackTokenizer import JackTokenizer
class Main:
    def __init__(self):
        pass

    def test_cleanFile(self):
        """
        Test the cleanFile function using a sample input file.
        """
        # Create a sample file to test
        test_filename = "test_file.txt"
        with open(test_filename, "w") as test_file:
            test_file.write("if (x < 0) {\n")
            test_file.write("// some comment\n")
            test_file.write("let sign = \"negative\";\n")
            test_file.write("}\n")

        # Create an instance of JackTokenizer and test cleanFile
        tokenizer = JackTokenizer(test_filename)
        cleaned_tokens = tokenizer.claenFile(test_filename)

        # Output the cleaned tokens
        print("Cleaned Tokens:", cleaned_tokens)

if __name__ == "__main__":
    main = Main()
    main.test_cleanFile()
