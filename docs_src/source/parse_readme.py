from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
SOURCE_DIR = Path(__file__).parent.resolve()
README_FILE = ROOT_DIR.joinpath('README.md')


def write_readme_section_to_file(section_name, destination, *, markdown_section_marker='#', readme_file=README_FILE):
    """
    Extracts one section of a readme file and writes it out into another file

    Parameters
    ----------
    section_name: str
        Name of the section in the README file to copy to the docs_src
    destination: str
        The path and name of the file created from the readme section relative to 'SOURCE_DIR'
    markdown_section_marker: str
        The Markdown marker that identifies the section. It can be "#", "##", etc.
    readme_file: str
        The full path to the README file

    Returns
    -------
    -: None

    """
    readme_file = Path(readme_file)
    with open(readme_file) as f:
        readme = f.read()

    if len(readme) == 0:
        raise ValueError(f"File {readme_file} is empty")

    markdown_section_marker = markdown_section_marker.strip()
    sections = [f"{x}" for x in readme.split(f"----\n\n")]
    section = [x for x in sections if x.startswith(f"{markdown_section_marker} {section_name}\n")]

    if len(section) == 0:
        raise ValueError(f"Couldn't find section {section_name} in file {readme_file}")
    if len(section) > 1:
        raise ValueError(f"There is more than 1 section with the name {section_name}. Fix README file first")
    section = section[0]

    output_file = SOURCE_DIR.joinpath(destination)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w+') as f:
        f.write(section)


def write_readme_sections_to_files(sections_dict, *, markdown_section_marker='#', readme_file=README_FILE,
                                   raise_errors=True):
    """
    Loops through different sections of a readme file and writes them out into different files

    Parameters
    ----------
    sections_dict: dict
        keys - names of the section
        values - destination of the section
    markdown_section_marker: str
        The Markdown marker that identifies the section. It can be "#", "##", etc.
    readme_file: str
        The full path to the README file
    raise_errors: bool
        If True, it will raise the errors and stop the loop.

    Returns
    -------
    -: None
    """

    for section, dest in sections_dict.items():
        try:
            write_readme_section_to_file(section, dest,
                                         markdown_section_marker=markdown_section_marker,
                                         readme_file=readme_file)
        except (ValueError, FileNotFoundError, PermissionError) as e:
            print(str(e))
            if raise_errors:
                raise
