import argparse
import glob
import os
from usfm_grammar import USFMParser
from pdf_generator import usx_to_pdf

def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert USFM file to PDF')
    parser.add_argument('input_pattern', help='Path or glob pattern for input USFM file(s)')
    parser.add_argument('-o', '--output', help='Path to output PDF file (ignored if multiple files are processed)')
    parser.add_argument('-d', '--output-dir', help='Directory for output files (default: same as input)')
    parser.add_argument('--header', help='Header text to display', default='')
    parser.add_argument('--noto-url', help='Custom Noto font URL (Google Fonts) to support specific script', default=None)
    return parser.parse_args()

def read_usfm_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def get_output_filename(input_file, output_dir=None):
    """Generate output filename by replacing extension with .pdf"""
    # Get the base filename without path
    base_name = os.path.basename(input_file)

    # Replace the extension with .pdf
    name_without_ext = os.path.splitext(base_name)[0]
    pdf_filename = f"{name_without_ext}.pdf"

    # If output directory is specified, use it
    if output_dir:
        # Create the directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        return os.path.join(output_dir, pdf_filename)

    # Otherwise, use the same directory as the input file
    input_dir = os.path.dirname(input_file)
    return os.path.join(input_dir, pdf_filename)

if __name__ == "__main__":
    args = parse_arguments()
    
    # Expand the glob pattern to get all matching files
    input_files = glob.glob(os.path.expanduser(args.input_pattern))

    if not input_files:
        print(f"No files found matching pattern: {args.input_pattern}")
        exit(1)

    # Process each file
    for input_file in input_files:
        try:
            # Determine output filename
            if len(input_files) == 1 and args.output:
                # If only one file and output is specified, use the specified output
                output_file = args.output
            else:
                # Otherwise, generate output filename based on input filename
                output_file = get_output_filename(input_file, args.output_dir)

            print(f"Processing {input_file} -> {output_file}")

            # Read USFM file
            input_usfm_str = read_usfm_file(input_file)

            # Parse USFM to USX
            my_parser = USFMParser(input_usfm_str)
            usx_elem = my_parser.to_usx(ignore_errors=True)

            # Check if output_file exists and confirm overwrite
            if os.path.exists(output_file):
                response = input(f"File {output_file} already exists. Overwrite? (y/n): ").strip().lower()
                if response != 'y':
                    print(f"Skipping {input_file}")
                    continue

            # Convert USX to PDF
            usx_to_pdf(usx_elem, output_file, header=args.header, custom_noto_url=args.noto_url)

        except Exception as e:
            print(f"Error processing {input_file}: {str(e)}")

    print(f"Processed {len(input_files)} file(s)")
