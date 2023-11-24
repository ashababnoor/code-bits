import os


def prefix_on_filename(filepath: str, prefix: str) -> str:
    """Add prefix to filename and get full filepath

    Args:
        filepath (str): Filepath of input file
        prefix (str): String prefix to be added to the filename

    Returns:
        str: Filepath witht the prefix added
    """
    directory = os.path.dirname(filepath)
    input_filename = os.path.basename(filepath)
    
    output_filename = prefix + input_filename
    output_filepath = os.path.join(directory, output_filename)
    
    return output_filepath