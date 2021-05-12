from pathlib import Path

import pytask


from config import revealjs_pandoc


names = [
    "labour-market-wellbeing-during-covid-19-netherlands",
    "oecd-experiences-liss",
    "work-hours-pisa",
]


@pytask.mark.parametrize(
    "depends_on, produces",
    [
        (
            [f"{n}.md", "template-revealjs.html", "config.py"]
            + list((Path(__file__).parent / "2021-01").glob("*")),
            f"{n}.html",
        )
        for n in names
    ],
)
def task_convert_revealjs(depends_on, produces):
    return revealjs_pandoc(depends_on, produces)
