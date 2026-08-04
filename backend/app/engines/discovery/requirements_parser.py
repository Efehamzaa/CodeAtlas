import re

pattern = re.compile(
    r"""
    ^
    (?P<package>[A-Za-z0-9_.-]+)
    (?:\[(?P<extras>[^\]]+)\])?
    \s*
    (?P<operator>==|>=|<=|~=|!=|>|<)?
    \s*
    (?P<version>[^\s;]+)?
    """,
    re.VERBOSE,
)


def parse_requirements(file_content: str) -> list[dict]:
    dependencies = []

    lines = file_content.splitlines()

    for line in lines:
        line = line.strip()

        
        if not line or line.startswith("#"):
            continue

        match = pattern.match(line)

        
        if not match:
            continue

        dependency = {
            "name": match.group("package"),
            "operator": match.group("operator"),
            "version": match.group("version"),
            "extras": (
                match.group("extras").split(",")
                if match.group("extras")
                else []
            ),
            "ecosystem": "pypi"
        }

        dependencies.append(dependency)

    return dependencies