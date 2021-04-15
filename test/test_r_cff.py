import pytest
import subprocess
import os
import pathlib
import yaml
import tempfile


TEST_DIR = os.path.dirname(__file__)


@pytest.mark.R
def test_r_citation_file():
    # temp_dir_ = tempfile.mkdtemp()
    # curr_dir_ = os.getcwd()
    # os.chdir(temp_dir_)

    # run_r_ = subprocess.Popen(
    #     [
    #         'Rscript',
    #         os.path.join(
    #             pathlib.Path(TEST_DIR).parent,
    #             'language_scripts',
    #             'R_metadata.R'
    #         ),
    #         '-i',
    #         os.path.join(TEST_DIR, 'DESCRIPTION')
    #     ],
    #     shell=False
    # )

    # run_r_.wait()

    # output_file_ = os.path.join(temp_dir_, 'CITATION.cff')
    # os.chdir(curr_dir_)
    # assert os.path.exists(output_file_)
    # assert yaml.safe_load(output_file_)
    pass
