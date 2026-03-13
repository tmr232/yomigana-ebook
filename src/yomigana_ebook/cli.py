from pathlib import Path
from time import time
from typing import Annotated
import typer

from yomigana_ebook.process_ebook import process_ebook

app = typer.Typer()


@app.command()
def main(
    ebook_paths: list[Path],
    force: Annotated[
        bool, typer.Option("--force", "-f", help="Override existing outputs.")
    ] = False,
):
    """The fastest converter to add yomigana(readings) to Japanese epub eBooks! (Using Mecab and Unidic)"""

    process_ebooks(ebook_paths, force=force)


def process_ebooks(input_paths: list[Path], force: bool = False):
    for input_path in input_paths:
        output_path = input_path.with_name(f"with-yomigana_{input_path.name}")

        if not force and output_path.exists():
            print(
                f"Output already exists, skipping conversion. Use `--force` to override. {output_path}"
            )
            continue

        with open(input_path, "rb") as f_reader, open(output_path, "wb") as f_writer:
            start_time = time()
            print()
            print(f"[start] parsing the ebook: {input_path}")

            process_ebook(f_reader, f_writer)

            end_time = time() - start_time
            print(f"[done]  here's the parsed ebook: {output_path}")
            print(f"this ebook takes {end_time} secs to process.")
            print()


if __name__ == "__main__":
    app()
