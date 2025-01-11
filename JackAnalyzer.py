from compilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer
import os

class JackAnalyzer:
    def _init_(self, input_path):
        """
        Initialize the analyzer with either a .jack file or a directory containing .jack files
        :param input_path: Path to file or directory
        """
        self.input_path = input_path
        self.files_to_process = []

        # Check if input is file or directory
        if os.path.isfile(input_path):
            if input_path.endswith('.jack'):
                self.files_to_process.append(input_path)
            else:
                raise ValueError(f"Input file must have .jack extension: {input_path}")
        elif os.path.isdir(input_path):
            # Get all .jack files in the directory
            for file in os.listdir(input_path):
                if file.endswith('.jack'):
                    self.files_to_process.append(os.path.join(input_path, file))
        else:
            raise ValueError(f"Input path does not exist: {input_path}")

    def analyze(self):
        """
        Process all .jack files and create corresponding .xml files
        """
        for jack_file in self.files_to_process:
            self.process_file(jack_file)

    def process_file(self, jack_file):
        """
        Process a single .jack file:
        1. Create a JackTokenizer
        2. Create an output .xml file
        3. Create a compilationEngine
        4. Call compileClass
        5. Close the output file
        """
        # Create output file name by replacing .jack with .xml
        output_file = jack_file[:-5] + '.xml'  # remove .jack and add .xml

        try:
            # Create the compilation engine (which creates the tokenizer internally)
            engine = CompilationEngine(jack_file, output_file)

            # Compile the class
            engine.compile_class()
            print(f"Successfully processed {jack_file}")

        except Exception as e:
            print(f"Error processing {jack_file}: {str(e)}")
            # Clean up the output file if it was created
            if os.path.exists(output_file):
                os.remove(output_file)
            raise


