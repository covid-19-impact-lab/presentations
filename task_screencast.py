from pathlib import Path

import pytask



from config import plain_pandoc
from config import revealjs_pandoc


names = ["labour-market-wellbeing-during-covid-19-netherlands"]


@pytask.mark.parametrize(
    "depends_on, produces",
    [
        (
            [f"{n}.md", "template-revealjs.html", "config.py"],
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
