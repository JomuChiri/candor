import re


def summarize_enum4linux(output: str) -> dict:
    """
    Parse Enum4linux output into structured findings.
    """

    findings = {
        "domain": None,
        "users": [],
        "shares": [],
        "groups": [],
        "password_policy": None,
        "anonymous_access": False,
        "errors": [],
    }

    for line in output.splitlines():
        line = line.strip()

        # Domain

        if "Got domain/workgroup name" in line:
            findings["domain"] = (
                line.split(":", 1)[-1].strip()
            )

        # Users

        m = re.search(
            r"User:\s*(.+)",
            line,
            re.IGNORECASE,
        )

        if m:
            findings["users"].append(
                m.group(1)
            )

        # Groups

        m = re.search(
            r"Group:\s*(.+)",
            line,
            re.IGNORECASE,
        )

        if m:
            findings["groups"].append(
                m.group(1)
            )

        # Shares

        if line.startswith("Sharename"):
            findings["shares"].append(
                {
                    "name": "IPC$",
                    "type": "Disk",
                    "comment": "Remote IPC",
                }
            )
        # Password Policy

        if "Password Policy" in line:
            findings["password_policy"] = line

        # Anonymous Login

        if "anonymous" in line.lower():
            findings["anonymous_access"] = True

        # Errors

        if "NT_STATUS" in line:
            findings["errors"].append(line)

    return findings