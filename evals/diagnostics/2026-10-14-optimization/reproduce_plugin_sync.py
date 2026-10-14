"""Exercise plugin file additions/edits/deletions/renames in an isolated checkout subset."""
from pathlib import Path
import argparse, json, shutil, subprocess, sys, tempfile

def run(source):
    source = source.resolve()
    results = {}
    with tempfile.TemporaryDirectory(prefix="toolkit-plugin-sync-") as temp:
        root = Path(temp).resolve()
        for folder in ("scripts", "references", "plugins"):
            shutil.copytree(source/folder, root/folder, ignore=shutil.ignore_patterns("__pycache__"))
        for name in ("VERSION", "SKILL.md", "SKILL.zh-CN.md", "LICENSE", "requirements-mcp.txt", "CHANGELOG.md", "CHANGELOG.zh-CN.md"):
            shutil.copyfile(source/name, root/name)
        (root/"docs").mkdir()
        for path in (source/"docs").glob("*.md"):
            shutil.copyfile(path, root/"docs"/path.name)
        shutil.copytree(source/"docs/releases", root/"docs/releases")
        def command(check=False):
            p=subprocess.run([sys.executable, str(root/"scripts/build_plugin.py"), *(["--check"] if check else [])], capture_output=True, text=True, encoding="utf-8")
            return {"exit":p.returncode,"output":(p.stdout+p.stderr).strip()}
        def snapshot():
            return {p.relative_to(root).as_posix():p.read_bytes() for p in (root/"plugins").rglob("*") if p.is_file()}
        assert command()["exit"] == 0
        source_file=root/"references/sync-probe.md"
        target=root/"plugins/research-toolkit/references/sync-probe.md"
        source_file.write_text("# Isolated build probe\n",encoding="utf-8")
        results["add"]={"check":command(True),"build":command(),"copied":target.is_file()}
        source_file.write_text("# Edited probe\n",encoding="utf-8")
        results["modify"]={"check":command(True),"build":command(),"copied":target.read_bytes()==source_file.read_bytes()}
        assert source_file.resolve().is_relative_to(root)
        source_file.unlink()
        before=snapshot(); check=command(True)
        results["delete"]={"check":check,"check_read_only":before==snapshot(),"build":command(),"stale_copy_remains":target.exists()}
        source_file.write_text("# Rename probe\n",encoding="utf-8");assert command()["exit"]==0
        renamed=source_file.with_name("sync-probe-renamed.md")
        assert source_file.resolve().is_relative_to(root) and renamed.resolve().is_relative_to(root)
        source_file.rename(renamed)
        results["rename"]={"check":command(True),"build":command(),"old_copy_remains":target.exists(),"new_copy_exists":target.with_name(renamed.name).exists()}
        before=snapshot(); results["idempotence"]={"build":command(),"unchanged":before==snapshot(),"check":command(True)}
    return results

if __name__ == "__main__":
    p=argparse.ArgumentParser();p.add_argument("--source",type=Path,default=Path(__file__).resolve().parents[3]);p.add_argument("--output",type=Path)
    args=p.parse_args();result=run(args.source);text=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if args.output:args.output.write_text(text,encoding="utf-8")
    print(text)
