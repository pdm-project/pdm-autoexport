import shutil
from pathlib import Path

import pytest
from pdm.core import Core
from pdm.project import Project

TEMPLATE_PYPROJECT = Path(__file__).parent / "pyproject.toml"


@pytest.fixture()
def tmp_project(tmp_path: Path) -> Project:
    shutil.copy2(TEMPLATE_PYPROJECT, tmp_path / "pyproject.toml")
    core = Core()
    return core.create_project(tmp_path)


def test_pdm_autoexport(tmp_project: Project):
    tmp_project.core.main(["lock", "-v"], obj=tmp_project)
    requirements_txt = tmp_project.root.joinpath("requirements.txt").read_text()
    requirements_test_txt = tmp_project.root.joinpath(
        "requirements-test.txt"
    ).read_text()
    setup_py = tmp_project.root.joinpath("setup.py").read_text()
    assert any(line.startswith("requests==") for line in requirements_txt.splitlines())
    assert any(line.startswith("urllib3==") for line in requirements_txt.splitlines())
    assert any(
        line.strip().startswith("--hash=") for line in requirements_txt.splitlines()
    )
    assert not any(
        line.startswith("requests==") for line in requirements_test_txt.splitlines()
    )
    assert any(
        line.startswith("pytest==") for line in requirements_test_txt.splitlines()
    )
    assert not any(
        line.strip().startswith("--hash=")
        for line in requirements_test_txt.splitlines()
    )
    assert any(line.strip().startswith("'requests'") for line in setup_py.splitlines())
