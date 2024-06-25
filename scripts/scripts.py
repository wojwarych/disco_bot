import subprocess


def format():
    try:
        subprocess.run(["black", "."])
        subprocess.run(["isort", "disco_bot/", "tests/"])
        subprocess.run(["flake8", "disco_bot/", "tests/"])
        subprocess.run(
            [
                "autoflake",
                "-r",
                "-cd",
                "--remove-all-unused-imports",
                "--ignore-init-module-imports",
                "disco_bot",
                "tests",
            ]
        )
        subprocess.run(["pylint", "disco_bot/", "tests/"])
        subprocess.run(["mypy", "disco_bot/", "tests/"])
    except Exception as e:
        print(e)


def check():
    subprocess.run(["black", "--check", "."])
    subprocess.run(["isort", "--check", "."])
    subprocess.run(["flake8", "disco_bot/", "tests/"])
    subprocess.run(
        [
            "autoflake",
            "-r",
            "-c",
            "--remove-all-unused-imports",
            "--ignore-init-module-imports",
            "mini_sedric",
            "tests",
        ]
    )
    subprocess.run(["pylint", "disco_bot/", "tests/"])
    subprocess.run(["mypy", "disco_bot/", "tests/"])
