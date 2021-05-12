from pathlib import Path

import pypandoc


SRC = Path(__file__).parent
OUT = SRC.joinpath("out")
TMP = SRC.joinpath("_tmp")


def plain_pandoc(depends_on, produces):
    if produces.suffix == ".html":
        pypandoc.convert(
            str(depends_on),
            "html",
            outputfile=str(produces),
            extra_args=[
                "--standalone",
                "--self-contained",
                "--mathjax",
                f"--resource-path={depends_on.parent}",
            ],
        )
    elif produces.suffix == ".pdf":
        pypandoc.convert(
            str(depends_on),
            "pdf",
            outputfile=str(produces),
            extra_args=["--pdf-engine=xelatex"],
        )
    else:
        raise NotImplementedError(produces.suffix)


def revealjs_pandoc(depends_on, produces):
    pypandoc.convert(
        str(depends_on[0]),
        "revealjs",
        outputfile=str(produces),
        extra_args=[
            "--template=" + str(depends_on[1]),
            "--section-divs",
            "--mathjax",
            "-t",
            "html5",
            "-V",
            "theme:night",
            "-V",
            "revealjs-url=file://" + str(SRC.absolute()),
            "--no-highlight",
            "--standalone",
            "--self-contained",
            f"--resource-path={depends_on[0].parent}",
        ],
    )
