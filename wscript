import shutil
from collections import OrderedDict
import os

import pypandoc

import os
import sys
from operator import attrgetter


# The project root directory and the build directory.
top = "."
out = "bld"


def set_project_paths(ctx):
    """Define the project paths."""

    pp = {}
    # The PROJECT_ROOT path will be appended to the PYTHONPATH environmental
    # variable. Do the same in the Eclipse project settings, if applicable.
    pp["PROJECT_ROOT"] = "."
    pp["BLD_SLIDES"] = "{}/slides".format(out)
    pp["BLD_HANDOUTS"] = "{}/handouts".format(out)

    # Convert the directories into waf nodes.
    for key, val in pp.items():
        pp[key] = ctx.path.make_node(val)

    return pp


def path_to(ctx, pp_key, *args):
    """Return the relative path to os.path.join(*args*) in the directory
    PROJECT_PATHS[pp_key] as seen from ctx.path (i.e. the directory of the
    current wscript).

    Use this to get the relative path---as needed by Waf---to a file in one
    of the directory trees defined in the PROJECT_PATHS dictionary above.

    We always pretend everything is in the source directory tree, Waf takes
    care of the correct placing of targets and sources.

    """

    # Implementation detail:
    #   We find the path to the directory where the file lives, so that
    #   we do not accidentally declare a node that does not exist.
    dir_path_in_tree = os.path.join(".", *args[:-1])
    # Find/declare the directory node. Use an alias to shorten the line.
    pp_key_fod = ctx.env.PROJECT_PATHS[pp_key].find_or_declare
    dir_node = pp_key_fod(dir_path_in_tree).get_src()
    # Get the relative path to the directory.
    path_to_dir = dir_node.path_from(ctx.path)
    # Return the relative path to the file.
    return os.path.join(path_to_dir, args[-1])


def configure(ctx):
    ctx.env.PYTHONPATH = os.getcwd()
    # Disable on a machine where security risks could arise
    ctx.env.PDFLATEXFLAGS = "-shell-escape"
    ctx.load("biber")
    ctx.load("run_py_script")
    ctx.load("sphinx_build")
    ctx.load("write_project_headers")


def my_copy(tsk):
    assert len(tsk.inputs) == len(tsk.outputs), "{}\n\n{}".format(
        tsk.inputs, tsk.outputs
    )
    for i in range(len(tsk.inputs)):
        shutil.copy(tsk.inputs[i].abspath(), tsk.outputs[i].abspath())


def preprocess(tsk):
    preproc.preprocess(
        inputfile=tsk.inputs[0].abspath(), outputfile=tsk.outputs[0].abspath()
    )


def create_slides(tsk):
    fl.generate_slides(
        inputfile=tsk.inputs[0].abspath(), outputfile=tsk.outputs[0].abspath()
    )


def create_handouts(tsk):
    fl.generate_handouts(
        inputfile=tsk.inputs[0].abspath(), outputfile=tsk.outputs[0].abspath()
    )


def create_handout_pdf(tsk):
    pypandoc.convert(
        tsk.inputs[0].abspath(),
        "pdf",
        outputfile=tsk.outputs[0].abspath(),
        extra_args=["--pdf-engine=xelatex"],
    )


def create_revealjs_html(tsk):
    pypandoc.convert(
        tsk.inputs[0].abspath(),
        "revealjs",
        outputfile=tsk.outputs[0].abspath(),
        # filters=['pandoc-citeproc'],
        extra_args=[
            "--template={}/template-revealjs.html".format(
                tsk.env.PROJECT_PATHS["PROJECT_ROOT"].abspath()
            ),
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


def get_lectures_copy_deps(ctx):
    def in_example(lecture, *args):
        return ctx.path_to(ctx, "SRC_EXAMPLES", lecture, *args)

    def out_example(lecture, *args):
        return ctx.path_to(ctx, "BLD_EXAMPLES", lecture, *args)

    def bld_lectures_example(lecture, *args):
        return ctx.path_to(ctx, "BLD_LECTURES_EXAMPLES", lecture, *args)

    def _copy_file_return_tgt(src, tgt):
        ctx(rule=my_copy, source=src, target=tgt)
        return tgt

    # Empty dict for all the deps.
    out = OrderedDict()

    out["feedback"] = []

    # Set dependency on template and preprocessor for all lectures.
    for jj in out:
        out[jj].append(ctx.path_to(ctx, "SRC_LECTURES", "template-revealjs.html"))
        out[jj].append(ctx.path_to(ctx, "SRC_LECTURES", "preprocessor.py"))

    return out


def build(ctx):
    ctx.env.PROJECT_PATHS = set_project_paths(ctx)
    ctx.path_to = path_to
    # ctx.env.TEXINPUTS = (
    #     ctx.env.PROJECT_PATHS["SRC_EXAMPLES"].abspath()
    #     + os.pathsep
    #     + os.path.join(ctx.env.PROJECT_PATHS["LIBRARY"].abspath(), "bib")
    # )

    # Generate header files with project paths.
    ctx(features="write_project_paths", target="project_paths.py")

    for src_node in ctx.path.ant_glob("revealjs_code/**"):
        src = src_node.path_from(ctx.path)
        tgt = ctx.path_to(
            ctx,
            "BLD_SLIDES",
            # src.split(os.sep)[1],
            os.path.join(*src.split(os.sep)[1:]),
        )
        ctx(rule="cp ${SRC} ${TGT}", source=src, target=tgt)

    folders = ("fig-econ-exp", "work-childcare", "mental-health")
    for folder in folders:
        for src_node in ctx.path.ant_glob(f"{folder}/**"):
            src = src_node.path_from(ctx.path)
            tgt = ctx.path_to(
                ctx,
                "BLD_SLIDES",
                src,
                # src.split(os.sep)[1],
                # os.path.join(*src.split(os.sep)[1:]),
            )
            ctx(rule="cp ${SRC} ${TGT}", source=src, target=tgt)

    for out_trunk in "first-results", "erste-ergebnisse", "ose-meetup":
        ctx(
            rule=create_revealjs_html,
            source=f"{out_trunk}.rst",
            target=ctx.path_to(ctx, "BLD_SLIDES", f"{out_trunk}.html"),
        )
        ctx(
            rule=create_handout_pdf,
            source=f"{out_trunk}.rst",
            target=ctx.path_to(ctx, "BLD_HANDOUTS", f"{out_trunk}.pdf"),
        )
