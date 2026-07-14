# candor/commands/doctor.py
from candor.doctor import doctor

def matches(query: str) -> bool:
    return query.lower().startswith("doctor")

def handle(query: str, console):
    _, *args = query.split()
    results = doctor(args[0] if args else None)

    console.print("\n[bold magenta]System Health Check[/]")
    for name, info in results.items():
        if info["installed"]:
            console.print(f"✓ {name} installed")
            console.print(f"   Path   : {info['path']}")
            console.print(f"   Version: {info['version']}")
        else:
            console.print(f"✗ {name} missing")
