from pathlib import Path

import pytask

# from config import plain_pandoc
# from config import revealjs_pandoc


import pypandoc


SRC = Path(__file__).parent
OUT = SRC.joinpath("out")
STUD = SRC.parent.joinpath("epp-materials")
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


names = [
    # "labour-market-wellbeing-during-covid-19-netherlands",
    "panel_discussion_law"
]


@pytask.mark.parametrize(
    "depends_on, produces",
    [
        (
            [f"{n}.md", "template-revealjs.html"]
            + list((Path(__file__).parent / "2021-01").glob("*")),
            f"{n}.html",
        )
        for n in names
    ],
)
def task_convert_revealjs(depends_on, produces):
    return revealjs_pandoc(depends_on, produces)


# @pytask.mark.parametrize(
#     "depends_on, produces",
#     [
#         (
#             f"{n}-{typ}.md",
#             d / this_week / f"{n}-{typ}.html",
#         )
#         for n in names
#         for typ, d in (("script", OUT), ("screencast", OUT), ("screencast", STUD))
#         if (Path(__file__).parent / f"{n}-{typ}.md").is_file()
#     ],
# )
# def task_convert_plain(depends_on, produces):
#     return plain_pandoc(depends_on, produces)
