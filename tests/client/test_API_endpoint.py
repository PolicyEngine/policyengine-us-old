from pathlib import Path

REPO = Path(__file__).parents[2]


def in_text_files(folder: Path, text: str):
    for child in folder.iterdir():
        if child.is_dir():
            if in_text_files(child, text):
                return True, child
        else:
            with open(child, encoding="utf-8") as f:
                try:
                    contents = f.read()
                    if text in contents:
                        return True, child
                except:
                    pass


def test_localhost_included():
    assert not in_text_files(REPO / "client" / "src", "localhost")
