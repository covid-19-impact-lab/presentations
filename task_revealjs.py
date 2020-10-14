import pypandoc
import pytask


@pytask.mark.depends_on(("crc-covid-data.rst", "template-revealjs.html"))
@pytask.mark.produces("crc-covid-data.html")
def task_slides(depends_on, produces):
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
