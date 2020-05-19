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

    # Introduction
    out["introduction"] = []
    for f in range(9):
        out["introduction"].append(
            _copy_file_return_tgt(
                src=in_example("prologue", "abg_{}.png".format(f + 1)),
                tgt=bld_lectures_example("prologue", "abg_{}.png".format(f + 1)),
            )
        )
    for f in range(2):
        out["introduction"].append(
            _copy_file_return_tgt(
                src=in_example("prologue", "magic_button_{}.png".format(f + 1)),
                tgt=bld_lectures_example(
                    "prologue", "magic_button_{}.png".format(f + 1)
                ),
            )
        )
    out["introduction"].append(
        _copy_file_return_tgt(
            src=in_example("outline", "McCullough09Fig1.png"),
            tgt=bld_lectures_example("outline", "McCullough09Fig1.png"),
        )
    )

    # Shell introduction
    out["shell_introduction"] = []
    for f in ("basic_directory_structure.png", "users_directory_structure.png"):
        out["shell_introduction"].append(
            _copy_file_return_tgt(
                src=in_example("shell_introduction", f),
                tgt=bld_lectures_example("shell_introduction", f),
            )
        )
    out["shell_introduction"].append(in_example("git_single_machine", "outline_v0.tex"))

    # Latex
    out["latex"] = []
    for f in (
        "math_example_rendered.png",
        "math_example.tex",
        "simplified_course_outline_rendered.png",
        "simplified_course_outline.tex",
        "smith_1776_first_par_rendered.png",
        "smith_1776_first_par.tex",
    ):
        out["latex"].append(
            _copy_file_return_tgt(
                src=in_example("latex", f), tgt=bld_lectures_example("latex", f)
            )
        )

    # Git single machine
    out["git_single_machine"] = []
    for f in (
        "phd_versions.png",
        "xkcd_git_commit.png",
        "screenshots/tortoiseGit_commit_1.png",
        "screenshots/tortoiseGit_commit_2.png",
        "screenshots/tortoiseGit_commit_3.png",
    ):
        out["git_single_machine"].append(
            _copy_file_return_tgt(
                src=in_example("git_single_machine", f),
                tgt=bld_lectures_example("git_single_machine", f),
            )
        )
    out["git_single_machine"].append(in_example("git_single_machine", "outline_v0.tex"))

    for f in (
        "dag_project_chain_0.svg",
        "dag_project_chain_1.svg",
        "dag_project_chain_2.svg",
        "dag_project_chain_3.svg",
        "dag_project_branch_0.svg",
        "dag_project_branch_1.svg",
        "dag_project_branch_2.svg",
        "dag_project_branch_3.svg",
        "dag_project_branch_4.svg",
        "dag_project_branch_5.svg",
        "dag_project_branch_6.svg",
        "dag_project_branch_tag_missing.svg",
        "dag_project_branch_tag.svg",
    ):
        out["git_single_machine"].append(
            _copy_file_return_tgt(
                src=out_example("git_single_machine", f),
                tgt=bld_lectures_example("git_single_machine", f),
            )
        )

    # Basic programming
    out["basic_programming"] = []
    for f in (
        "hello_world_no_output.png",
        "hello_world_with_output.png",
        "hydrogen_error.png",
        "legb_scope_lutz07_p313.png",
    ):
        out["basic_programming"].append(
            _copy_file_return_tgt(
                src=in_example("basic_programming", f),
                tgt=bld_lectures_example("basic_programming", f),
            )
        )
    for f in (
        "earnings_v0.py",
        "earnings_outline_scrambled.py",
        "earnings_outline.py",
        "earnings_v1.py",
        "earnings_gamma_cogn_2dot5.py",
        "earnings_for_loop_list.py",
        "earnings_for_loop_list_append.py",
        "earnings_dictionaries.py",
        "earnings_with_data.py",
        "earnings_with_missing_data.py",
        "earnings_with_function_for_skills_ouch.py",
        "earnings_with_two_functions.py",
        "cobb_douglas.py",
    ):
        out["basic_programming"].append(
            _copy_file_return_tgt(
                src=in_example("production_function_cobb_douglas", f),
                tgt=bld_lectures_example("basic_programming", f),
            )
        )

    # Basic programming
    out["waf_pre_commit_intro"] = []

    # Git collaboration
    out["git_collaboration"] = []
    for f in (
        "heart_v0.py",
        "heart_v1.py",
        "heart_v2.py",
        "heart_with_conflicts.py",
        "heart_v3.py",
        "heart_0.png",
        "heart_1.png",
        "git-clone-again.png",
        "git-visualisation.png",
        "recommended_workflow.png",
        "schematic_workflow_1.png",
        "schematic_workflow_2.png",
        "tristan_isolde_schematic_overview.png",
        "screenshots/heart_pdf_on_remote_repository.png",
        "screenshots/github_create_new_project_0.png",
        "screenshots/github_create_new_project_1.png",
        "screenshots/github_create_new_project_2.png",
        "screenshots/add_collaborator.png",
        "screenshots/github_first_commit_pushed.png",
        "screenshots/files_change_on_remote.png",
        "screenshots/merge_with_atom_0.png",
        "screenshots/merge_with_atom_1.png",
        "git_schemas/workflow-0.png",
        "git_schemas/workflow-1.png",
        "git_schemas/workflow-2.png",
        "git_schemas/workflow-3.png",
        "git_schemas/workflow-4.png",
        "git_schemas/workflow-5.png",
        "git_schemas/workflow-6.png",
        "git_schemas/workflow-7.png",
        "git_schemas/workflow-8.png",
        "git_schemas/workflow-9.png",
        "git_schemas/workflow-10.png",
        "git_schemas/workflow-11.png",
        "git_schemas/workflow-12.png",
        "git_schemas/workflow-13.png",
        "git_schemas/workflow-14.png",
        "git_schemas/tristan-isolde-only-master-0.png",
        "git_schemas/tristan-isolde-only-master-1.png",
        "git_schemas/tristan-isolde-only-master-2.png",
        "git_schemas/tristan-isolde-only-master-3.png",
        "git_schemas/tristan-isolde-only-master-4.png",
        "git_schemas/tristan-isolde-only-master-5.png",
        "git_schemas/tristan-isolde-only-master-6.png",
        "git_schemas/tristan-isolde-only-master-7.png",
        "git_schemas/tristan-isolde-only-master-8.png",
        "git_schemas/tristan-isolde-only-master-9.png",
        "git_schemas/tristan-isolde-only-master-10.png",
        "git_schemas/tristan-isolde-only-master-11.png",
        "git_schemas/tristan-isolde-only-master-12.png",
        "git_schemas/tristan-isolde-only-master-13.png",
        "git_schemas/tristan-isolde-only-master-14.png",
        "git_schemas/tristan-isolde-only-master-15.png",
        "git_schemas/tristan-isolde-separate-branches-0.png",
        "git_schemas/tristan-isolde-separate-branches-1.png",
        "git_schemas/tristan-isolde-separate-branches-2.png",
        "git_schemas/tristan-isolde-separate-branches-3.png",
        "git_schemas/tristan-isolde-separate-branches-4.png",
        "git_schemas/tristan-isolde-separate-branches-5.png",
        "git_schemas/tristan-isolde-separate-branches-6.png",
        "git_schemas/tristan-isolde-separate-branches-7.png",
    ):
        out["git_collaboration"].append(
            _copy_file_return_tgt(
                src=in_example("git_collaboration", f),
                tgt=bld_lectures_example("git_collaboration", f),
            )
        )

    out["more_on_containers"] = []
    for f in (
        "aliasing_function_bad.py",
        "aliasing_function_good.py",
        "aliasing_grid_v0.py",
        "aliasing_grid_v1.py",
        "aliasing_grid_v2.py",
    ):
        out["more_on_containers"].append(
            _copy_file_return_tgt(
                src=in_example("more_on_containers", f),
                tgt=bld_lectures_example("more_on_containers", f),
            )
        )

    out["data_management"] = []
    for f in ("example_data_relational_database.png", "relations_between_tables.png"):
        out["data_management"].append(
            _copy_file_return_tgt(
                src=in_example("data_management", f),
                tgt=bld_lectures_example("data_management", f),
            )
        )

    # Debugging
    out["exceptions_debugging"] = []
    for f in (
        "error_handling.py",
        "error_handling_multiple.py",
        "cobb_douglas_no_debugger.py",
        "cobb_douglas.py",
        "earnings.py",
    ):
        out["exceptions_debugging"].append(
            _copy_file_return_tgt(
                src=in_example("exceptions_debugging", f),
                tgt=bld_lectures_example("exceptions_debugging", f),
            )
        )

    # Testing
    out["testing"] = []
    for f in (
        "floating_point_5bit_representable_values.png",
        "floating_point_5bit.png",
        "floating_point_32bit.png",
        "utility_crra.py",
        "utility_crra_test_manual.py",
        "utility_crra_test.py",
    ):
        out["testing"].append(
            _copy_file_return_tgt(
                src=in_example("testing", f), tgt=bld_lectures_example("testing", f)
            )
        )

    out["speedup"] = []

    out["plotting_optimising"] = []
    out["waf_project_layouts"] = []

    # Documentation
    out["documentation"] = []
    for f in (
        "documentation_structure.png",
        "output_autodoc.png",
        "output_statadoc.png",
        "paragraph_html_output.png",
        "paragraph_latex_output.png",
    ):
        out["documentation"].append(
            _copy_file_return_tgt(
                src=in_example("documentation", f),
                tgt=bld_lectures_example("documentation", f),
            )
        )

    # # Objects
    # out["objects"] = []
    # for f in (
    #     "agent.py",
    #     "agent_utility.py",
    #     "inheritance.py",
    #     "inheritance_placeholder.py",
    #     "horizontal.py",
    #     "bht_figure_1.png",
    #     "horizontal_relationships.png",
    #     "inheritance_diagram.png",
    # ):
    #     out["objects"].append(
    #         _copy_file_return_tgt(
    #             src=in_example("objects", f), tgt=bld_lectures_example("objects", f)
    #         )
    #     )

    out["files_strings"] = []
    for f in (
        "ahold_reported_strings_content.png",
        "allais_1953_section_1.png",
        "allais_1953_section_1.txt",
        "exercise_solution_template.tex",
        "with_statement.py",
    ):
        out["files_strings"].append(
            _copy_file_return_tgt(
                src=in_example("files_strings", f),
                tgt=bld_lectures_example("files_strings", f),
            )
        )

    out["regular_expressions"] = []
    for f in (
        "lab.txt",
        "cp.csv",
        "regex_start.py",
        "first_lines_of_data.txt",
        "matches_nov_no_regex.txt",
        "matches_nov_regex.txt",
        "matches_nov_dec_function.txt",
        "matches_nov_dec_function_wrong.txt",
        "matches_nov_dec_parentheses.txt",
        "matches_nov_dec_context.txt",
        "extract_nov_dec_full_match.txt",
        "extract_nov_dec_group_1.txt",
        "extract_date_using_string_operations.txt",
        "txt_strings.txt",
        "matches_txt_strings.txt",
        "extract_date_matches_too_much.txt",
        "extract_date_lazy.txt",
        "extract_date_more_structure.txt",
        "extract_date_using_character_set.txt",
        "atom_file_replace.png",
        "atom_file_search.png",
    ):
        out["regular_expressions"].append(
            _copy_file_return_tgt(
                src=in_example("regular_expressions", f),
                tgt=bld_lectures_example("regular_expressions", f),
            )
        )

    out["shell_remote"] = []
    # for f in ("language_speed_1.png", "language_speed_2.png"):
    #     out["tool_choice"].append(
    #         _copy_file_return_tgt(
    #             src=in_example("tool_choice", f),
    #             tgt=bld_lectures_example("tool_choice", f),
    #         )
    #     )

    out["tool_choice"] = []
    for f in ("language_speed_1.png", "language_speed_2.png"):
        out["tool_choice"].append(
            _copy_file_return_tgt(
                src=in_example("tool_choice", f),
                tgt=bld_lectures_example("tool_choice", f),
            )
        )
    # final thoughts
    out["final_thoughts"] = []
    for f in (
        "overview-1.png",
        "overview-2.png",
        "overview-3.png",
        "overview-4.png",
        "overview-5.png",
        "overview-6.png",
    ):
        out["final_thoughts"].append(
            _copy_file_return_tgt(
                src=in_example("final_thoughts", f),
                tgt=bld_lectures_example("final_thoughts", f),
            )
        )

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

    out_trunk = "first-results"
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
    out_trunk = "ose-meetup"
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
