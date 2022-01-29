"""Generate Code Reference Documentation."""


# Standard
import pathlib

# Third-Party
import mkdocs_gen_files


# Constants
PACKAGE = pathlib.Path("pydantic_argparse")
DOCS = pathlib.Path("reference")
NAV = DOCS / pathlib.Path("SUMMARY.md")


def main() -> None:
    """Main Function."""
    # Instantiate Documentation Generator and Navigation
    gen = mkdocs_gen_files.FilesEditor.current()
    nav = mkdocs_gen_files.Nav()

    # Loop through all modules in the package
    for path in sorted(PACKAGE.glob("**/*.py")):
        # Put Dunder Files into `index.md`
        if path.stem.startswith("__") and path.stem.endswith("__"):
            # Set Docs Location
            docs = DOCS / path.parent / pathlib.Path("index.md")

            # Generate Magic String
            string = "## " + path.name.replace("_", r"\_") + "\n"

            # Get Header
            header = path.parent.stem

            # Nav Parts
            nav_parts = docs.relative_to(DOCS).parent.parts

        else:
            # Set Docs Location
            docs = DOCS / path.with_suffix(".md")

            # Initialise Magic String
            string = ""

            # Get Header
            header = path.stem

            # Nav Parts
            nav_parts = docs.relative_to(DOCS).with_suffix(".py").parts

        # Generate Magic String
        string += "::: " + ".".join(path.with_suffix("").parts) + "\n"

        # Write the Documentation
        with gen.open(docs, "a") as file_object:
            # Check if its the first time opening the file
            if not file_object.tell():
                # Write the file header
                file_object.write("# " + header + "\n")

            # Write
            file_object.write(string)

        # Append to Navigation
        nav[nav_parts] = docs.relative_to(DOCS)

    # Write the Navigation
    with gen.open(NAV, "w") as file_object:
        file_object.writelines(nav.build_literate_nav())


# Generate Docs
main()
