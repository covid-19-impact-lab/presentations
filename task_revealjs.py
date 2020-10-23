import pypandoc
import pytask


@pytask.mark.depends_on(("social-protection-during-covid-a-view-from-western-europe.rst", "template-revealjs.html"))
@pytask.mark.produces("social-protection-during-covid-a-view-from-western-europe.html")
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


@pytask.mark.depends_on("social-protection-during-covid-a-view-from-western-europe.rst")
@pytask.mark.produces("social-protection-during-covid-a-view-from-western-europe.pdf")
def task_pdf(depends_on, produces):
    pypandoc.convert(
        str(depends_on),
        "pdf",
        outputfile=str(produces),
        extra_args=["--pdf-engine=xelatex"],
    )
