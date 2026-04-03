#!/usr/bin/env python3
"""Set up a VS Code live-preview workspace for the CS179 HW1 LaTeX project."""

from __future__ import annotations

import argparse
import json
import os
import stat
import subprocess
import sys
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROJECT_DIR = ROOT / "output" / "overleaf" / "cs179-hw1-project"
DEFAULT_WORKSPACE_FILE = ROOT / "hw1-latex.code-workspace"
SOURCE_DIR_NAME = "source"
BUILD_DIR_NAME = "build"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=DEFAULT_PROJECT_DIR,
        help="Path to the existing HW1 LaTeX project directory.",
    )
    parser.add_argument(
        "--workspace-file",
        type=Path,
        default=DEFAULT_WORKSPACE_FILE,
        help="Path to the VS Code workspace file to generate.",
    )
    parser.add_argument(
        "--python",
        dest="python_executable",
        default=sys.executable,
        help="Python interpreter that LaTeX Workshop should use for the build helper.",
    )
    parser.add_argument(
        "--compile",
        action="store_true",
        help="Compile main.tex after writing the workspace files.",
    )
    return parser.parse_args()


def require_file(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Required file not found: {path}")


def write_text(path: Path, content: str, executable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if executable and os.name != "nt":
        mode = path.stat().st_mode
        path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def normalize_command(command: str) -> str:
    candidate = Path(command)
    if candidate.is_absolute():
        return str(candidate)
    if candidate.parent != Path("."):
        return str(candidate.resolve())
    return command


def ensure_tex_root_comment(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    marker = "% !TEX root = main.tex"
    if content.startswith(marker):
        return
    path.write_text(f"{marker}\n{content}", encoding="utf-8")


def workspace_folder_path(project_dir: Path) -> str:
    try:
        return project_dir.relative_to(ROOT).as_posix()
    except ValueError:
        return str(project_dir)


def source_dir(project_dir: Path) -> Path:
    return project_dir / SOURCE_DIR_NAME


def build_dir(project_dir: Path) -> Path:
    return project_dir / BUILD_DIR_NAME


def latex_workshop_settings(python_executable: str) -> dict[str, object]:
    return {
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 250,
        "workbench.editorAssociations": {
            "*.pdf": "latex-workshop-pdf-hook",
            "*.PDF": "latex-workshop-pdf-hook",
        },
        "latex-workshop.latex.autoBuild.run": "onSave",
        "latex-workshop.latex.recipe.default": "first",
        "latex-workshop.latex.outDir": "../build",
        "latex-workshop.latex.recipes": [
            {
                "name": "hw1-live-preview",
                "tools": ["hw1-build-helper"],
            }
        ],
        "latex-workshop.latex.tools": [
            {
                "name": "hw1-build-helper",
                "command": normalize_command(python_executable),
                "args": [
                    "%DIR%/../.vscode/build_hw1.py",
                    "%DIR%/main.tex",
                ],
                "env": {},
            }
        ],
        "latex-workshop.view.pdf.viewer": "tab",
        "latex-workshop.view.pdf.tab.editorGroup": "right",
        "latex-workshop.synctex.afterBuild.enabled": True,
        "latex-workshop.view.pdf.internal.synctex.keybinding": "double-click",
        "[latex]": {
            "editor.wordWrap": "on",
            "editor.wordSeparators": "`~!@#$%^&*()-=+[{]}\\\\|;:'\\\",.<>/?",
        },
    }


def extensions_payload() -> dict[str, list[str]]:
    return {
        "recommendations": ["James-Yu.latex-workshop"],
    }


def workspace_payload(project_dir: Path, python_executable: str) -> dict[str, object]:
    return {
        "folders": [
            {
                "path": workspace_folder_path(project_dir),
            }
        ],
        "settings": latex_workshop_settings(python_executable),
        "extensions": extensions_payload(),
    }


def build_helper_script() -> str:
    canonical = DEFAULT_PROJECT_DIR / ".vscode" / "build_hw1.py"
    if canonical.exists():
        return canonical.read_text(encoding="utf-8")

    return textwrap.dedent(
        """
        #!/usr/bin/env python3
        from __future__ import annotations

        import os
        import platform
        import shutil
        import subprocess
        import sys
        import tarfile
        import tempfile
        import urllib.request
        import zipfile
        from pathlib import Path

        TECTONIC_VERSION = "0.15.0"
        SCRIPT_DIR = Path(__file__).resolve().parent
        SOURCE_DIR_NAME = "source"
        BUILD_DIR_NAME = "build"


        def release_target() -> tuple[str, str]:
            system = platform.system()
            machine = platform.machine().lower()

            if system == "Darwin":
                if machine in {"arm64", "aarch64"}:
                    return "aarch64-apple-darwin", f"tectonic-{TECTONIC_VERSION}-aarch64-apple-darwin.tar.gz"
                if machine in {"x86_64", "amd64"}:
                    return "x86_64-apple-darwin", f"tectonic-{TECTONIC_VERSION}-x86_64-apple-darwin.tar.gz"
            elif system == "Windows":
                if machine in {"x86_64", "amd64"}:
                    return "x86_64-pc-windows-msvc", f"tectonic-{TECTONIC_VERSION}-x86_64-pc-windows-msvc.zip"
            elif system == "Linux":
                if machine in {"arm64", "aarch64"}:
                    return "aarch64-unknown-linux-musl", f"tectonic-{TECTONIC_VERSION}-aarch64-unknown-linux-musl.tar.gz"
                if machine in {"x86_64", "amd64"}:
                    return "x86_64-unknown-linux-gnu", f"tectonic-{TECTONIC_VERSION}-x86_64-unknown-linux-gnu.tar.gz"

            raise RuntimeError(f"Unsupported platform for Tectonic bootstrap: {system} {machine}")


        def executable_name() -> str:
            return "tectonic.exe" if os.name == "nt" else "tectonic"


        def tools_dir() -> Path:
            target, _ = release_target()
            return SCRIPT_DIR / "tools" / "tectonic" / TECTONIC_VERSION / target


        def repo_local_tectonic() -> Path:
            return tools_dir() / executable_name()


        def legacy_repo_local_tectonic() -> Path:
            return SCRIPT_DIR / "tools" / "tectonic" / TECTONIC_VERSION / executable_name()


        def normalize_executable(path: Path) -> Path:
            expected = repo_local_tectonic()
            candidates = sorted(path.rglob(executable_name()))
            if not candidates:
                raise RuntimeError(f"Tectonic archive did not contain {executable_name()}")

            source = candidates[0]
            expected.parent.mkdir(parents=True, exist_ok=True)
            if source.resolve() != expected.resolve():
                shutil.move(str(source), str(expected))

            if os.name != "nt":
                expected.chmod(expected.stat().st_mode | 0o111)
            return expected


        def bootstrap_tectonic() -> Path:
            binary = repo_local_tectonic()
            if binary.exists():
                if os.name != "nt":
                    binary.chmod(binary.stat().st_mode | 0o111)
                return binary

            legacy_binary = legacy_repo_local_tectonic()
            if legacy_binary.exists():
                if os.name != "nt":
                    legacy_binary.chmod(legacy_binary.stat().st_mode | 0o111)
                return legacy_binary

            target, asset = release_target()
            url = f"https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%40{TECTONIC_VERSION}/{asset}"
            destination = SCRIPT_DIR / "tools" / "tectonic" / TECTONIC_VERSION / target
            destination.mkdir(parents=True, exist_ok=True)

            with tempfile.TemporaryDirectory(prefix="hw1-tectonic-") as temp_dir:
                temp_root = Path(temp_dir)
                archive_path = temp_root / asset
                urllib.request.urlretrieve(url, archive_path)

                if asset.endswith(".zip"):
                    with zipfile.ZipFile(archive_path) as archive:
                        archive.extractall(destination)
                else:
                    with tarfile.open(archive_path, "r:gz") as archive:
                        archive.extractall(destination)

            return normalize_executable(destination)


        def compiler_command(kind: str, executable: str, doc_path: Path) -> tuple[list[str], Path]:
            doc_dir = doc_path.parent
            build_dir = doc_dir.parent / BUILD_DIR_NAME
            build_dir.mkdir(parents=True, exist_ok=True)
            if kind == "tectonic":
                return (
                    [
                        executable,
                        "-X",
                        "compile",
                        "--synctex",
                        "--keep-logs",
                        "--keep-intermediates",
                        "--outdir",
                        str(build_dir),
                        str(doc_path),
                    ],
                    doc_dir,
                )
            if kind == "latexmk":
                return (
                    [
                        executable,
                        "-pdf",
                        "-synctex=1",
                        "-interaction=nonstopmode",
                        "-file-line-error",
                        f"-outdir={build_dir}",
                        str(doc_path),
                    ],
                    doc_dir,
                )
            if kind == "pdflatex":
                return (
                    [
                        executable,
                        "-synctex=1",
                        "-interaction=nonstopmode",
                        "-file-line-error",
                        f"-output-directory={build_dir}",
                        doc_path.name,
                    ],
                    doc_dir,
                )
            raise RuntimeError(f"Unsupported compiler kind: {kind}")


        def first_available_compiler() -> tuple[str, str] | None:
            local_binary = repo_local_tectonic()
            if local_binary.exists():
                if os.name != "nt":
                    local_binary.chmod(local_binary.stat().st_mode | 0o111)
                return "tectonic", str(local_binary)

            legacy_binary = legacy_repo_local_tectonic()
            if legacy_binary.exists():
                if os.name != "nt":
                    legacy_binary.chmod(legacy_binary.stat().st_mode | 0o111)
                return "tectonic", str(legacy_binary)

            for name in ("tectonic", "latexmk", "pdflatex"):
                executable = shutil.which(name)
                if executable:
                    kind = "tectonic" if name == "tectonic" else name
                    return kind, executable

            return None


        def resolve_compiler() -> tuple[str, str]:
            compiler = first_available_compiler()
            if compiler is not None:
                return compiler

            try:
                return "tectonic", str(bootstrap_tectonic())
            except Exception as exc:
                raise RuntimeError(
                    "No LaTeX compiler is available. Tried repo-local Tectonic, PATH Tectonic, latexmk, "
                    "pdflatex, and Tectonic bootstrap."
                ) from exc


        def main() -> None:
            if len(sys.argv) != 2:
                print(f"Usage: {Path(sys.argv[0]).name} /absolute/path/to/main.tex", file=sys.stderr)
                raise SystemExit(2)

            doc_path = Path(sys.argv[1]).resolve()
            if not doc_path.exists():
                print(f"TeX entry point not found: {doc_path}", file=sys.stderr)
                raise SystemExit(1)

            kind, executable = resolve_compiler()
            command, cwd = compiler_command(kind, executable, doc_path)
            result = subprocess.run(command, cwd=cwd, check=False)
            raise SystemExit(result.returncode)


        if __name__ == "__main__":
            main()
        """
    ).lstrip()


def write_vscode_files(project_dir: Path, workspace_file: Path, python_executable: str) -> tuple[Path, Path, Path, Path]:
    vscode_dir = project_dir / ".vscode"
    build_script = vscode_dir / "build_hw1.py"
    settings_file = vscode_dir / "settings.json"
    extensions_file = vscode_dir / "extensions.json"

    write_text(build_script, build_helper_script(), executable=True)
    write_json(settings_file, latex_workshop_settings(python_executable))
    write_json(extensions_file, extensions_payload())
    write_json(workspace_file, workspace_payload(project_dir, python_executable))

    return build_script, settings_file, extensions_file, workspace_file


def compile_project(python_executable: str, build_script: Path, project_dir: Path) -> None:
    subprocess.run(
        [normalize_command(python_executable), str(build_script), str(source_dir(project_dir) / "main.tex")],
        check=True,
    )


def organize_project_dir(project_dir: Path) -> None:
    src_dir = source_dir(project_dir)
    out_dir = build_dir(project_dir)
    src_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    source_files = ("answers.tex", "answers.toml", "cs179-hw1.pdf", "main.tex")
    build_files = ("main.aux", "main.log", "main.pdf", "main.synctex.gz")

    for name in source_files:
        legacy = project_dir / name
        target = src_dir / name
        if legacy.exists() and not target.exists():
            legacy.rename(target)

    for name in build_files:
        legacy = project_dir / name
        target = out_dir / name
        if legacy.exists() and not target.exists():
            legacy.rename(target)


def main() -> None:
    args = parse_args()
    project_dir = args.project_dir.resolve()
    workspace_file = args.workspace_file.resolve()
    python_executable = normalize_command(args.python_executable)

    organize_project_dir(project_dir)

    require_file(source_dir(project_dir) / "main.tex")
    require_file(source_dir(project_dir) / "answers.tex")
    require_file(source_dir(project_dir) / "cs179-hw1.pdf")

    ensure_tex_root_comment(source_dir(project_dir) / "answers.tex")
    build_script, settings_file, extensions_file, workspace_path = write_vscode_files(
        project_dir=project_dir,
        workspace_file=workspace_file,
        python_executable=python_executable,
    )

    print(f"Wrote {build_script}")
    print(f"Wrote {settings_file}")
    print(f"Wrote {extensions_file}")
    print(f"Wrote {workspace_path}")

    if args.compile:
        compile_project(python_executable, build_script, project_dir)
        print(f"Compiled {build_dir(project_dir) / 'main.pdf'}")

    print("")
    print("Next steps:")
    print(f"- Open {workspace_path} in VS Code.")
    print(f"- Edit {source_dir(project_dir) / 'answers.tex'}.")
    print(f"- View {build_dir(project_dir) / 'main.pdf'} with LaTeX Workshop in the right editor group.")


if __name__ == "__main__":
    main()
