from JackAnalyzer import JackAnalyzer
import sys
import os


def main():
    """
    Main entry point. Usage: python JackAnalyzer.py <input_path>
    where input_path is either a .jack file or a directory containing .jack files
    """
    if len(sys.argv) != 2:
        print("Usage: python JackAnalyzer.py <input_path>")
        sys.exit(1)

    input_path = sys.argv[1]

    try:
        analyzer = JackAnalyzer(input_path)
        analyzer.analyze()
        print("Analysis completed successfully")
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":  # Fixed the dunder main check
    main()