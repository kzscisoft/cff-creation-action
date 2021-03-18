import pytest
import os
import subprocess
import tempfile
import pathlib
import yaml


TEST_DIR = os.path.dirname(__file__)


@pytest.mark.Julia
def test_julia_citation_file():
    temp_dir_ = tempfile.mkdtemp()
    curr_dir_ = os.getcwd()
    os.chdir(temp_dir_)

    run_r_ = subprocess.Popen(
        [
            'python',
            os.path.join(
                pathlib.Path(TEST_DIR).parent,
                'language_scripts',
                'julia_metadata.py'
            ),
            os.path.join(TEST_DIR, 'Project.toml')
        ],
        shell=False
    )

    run_r_.wait()

    output_file_ = os.path.join(temp_dir_, 'CITATION.cff')
    os.chdir(curr_dir_)
    print(output_file_)
    assert os.path.exists(output_file_)
    assert yaml.safe_load(output_file_)