from sqlalchemy.ext.asyncio import AsyncSession
from app.models.core import Repository
from app.models.analysis import Analysis, RepositoryFile
from app.models.findings import Technology, SecurityFinding

async def save_analysis_results(
    db: AsyncSession, 
    repo_url: str, 
    risk_score: int,
    dependencies: list, 
    frameworks: list,
    analyzed_files: list, 
    security_findings: list,
    user_id: int = 1
):
    try:
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        owner = repo_url.split("/")[-2] if "github.com" in repo_url else "Unknown"

        
        new_repo = Repository(
            user_id=user_id,
            github_url=repo_url,
            name=repo_name,
            owner=owner,
            status="completed"
        )
        db.add(new_repo)
        await db.flush() 

        
        new_analysis = Analysis(
            repository_id=new_repo.id,
            status="success",
            risk_score=risk_score
        )
        db.add(new_analysis)
        await db.flush()

        
        for dep in dependencies:
            name = getattr(dep, "name", dep.get("name") if isinstance(dep, dict) else "")
            version = getattr(dep, "version", dep.get("version") if isinstance(dep, dict) else "")
            if name:
                db.add(Technology(analysis_id=new_analysis.id, category="dependency", name=name, version=version))
            
        for fw in frameworks:
            name = getattr(fw, "name", fw.get("name") if isinstance(fw, dict) else "")
            if name:
                db.add(Technology(analysis_id=new_analysis.id, category="framework", name=name, version=""))

        
        for file_data in analyzed_files:
            path = file_data.get("file_path", "")
            ext = path.split('.')[-1] if '.' in path else ""
            arch = file_data.get("architecture", {})

            db.add(RepositoryFile(
                analysis_id=new_analysis.id, 
                path=path,
                extension=ext,
                language="python" if ext == "py" else "unknown",
                functions=arch.get("functions", []),
                classes=arch.get("classes", []),
                imports=arch.get("imports", [])
            ))

        
        for finding in security_findings:
            db.add(SecurityFinding(
                analysis_id=new_analysis.id,
                severity=getattr(finding, "severity", "High"),
                type=getattr(finding, "type", "Unknown"),
                file_path=getattr(finding, "file_path", "Unknown"),
                line_number=getattr(finding, "line_number", 0)
            ))

        await db.commit()
        return new_analysis.id

    except Exception as e:
        await db.rollback()
        print(f"[!] DB Kayıt Hatası: {e}")
        raise e