import argparse
from usfm_grammar import USFMParser
from pdf_generator import usx_to_pdf

def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert USFM file to PDF')
    parser.add_argument('input_file', help='Path to input USFM file')
    parser.add_argument('-o', '--output', help='Path to output PDF file', default='output.pdf')
    return parser.parse_args()

def read_usfm_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

if __name__ == "__main__":
    args = parse_arguments()
    
    # Read USFM file
    input_usfm_str = read_usfm_file(args.input_file)
    
    # Parse USFM to USX
    my_parser = USFMParser(input_usfm_str)
    usx_elem = my_parser.to_usx()
    
    # Convert USX to PDF
    usx_to_pdf(usx_elem, args.output)
