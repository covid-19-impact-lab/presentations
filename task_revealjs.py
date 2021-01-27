import itertools
import pypandoc
import pytask


names = [
    "social-protection-during-covid-a-view-from-western-europe",
    "covid-19-gender-division-of-market-and-household-work"
]
output_formats = ["html", "pdf"]


@pytask.mark.parametrize(
    "depends_on, produces",
    [
        (
            [f"{name}.rst", "template-revealjs.html"],
            f"{name}.{output_format}",
        )
        for name, output_format in itertools.product(names, output_formats)
    ]
)
def xtask_slides(depends_on, produces):
    if produces.suffix == ".html":
        pypandoc.convert(
            str(depends_on[0]),
            "revealjs",
            outputfile=str(produces),
            # filters=['pandoc-citeproc'],
            extra_args=[
                "--template=" + str(depends_on[1]),
                # '--standalone',
                "--section-divs",
                "--mathjax",
                "-t",
                "html5",
                "-V",
                "theme:night",
                "--no-highlight",
                # '--bibliography="src/library/bib/hmg.bib"'
            ],
        )
    elif produces.suffix == ".pdf":
        pypandoc.convert(
            str(depends_on[0]),
            "pdf",
            outputfile=str(produces),
            extra_args=["--pdf-engine=xelatex"],
        )
    else:
        raise NotImplementedError(produces.suffix)
