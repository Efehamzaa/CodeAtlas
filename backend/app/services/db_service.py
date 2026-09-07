from sqlalchemy.ext.asyncio import AsyncSession
from app.models.core import Repository
from app.models.analysis import Analysis, RepositoryFile
from app.models.findings import Technology
from app.models.findings import SecurityFinding

async def save_analysis_results(
    db: AsyncSession, 
    repo_data: dict, 
    parsed_dependencies: list, 
    analyzed_files: list, 
    security_findings: list,
    ai_report: dict=None,
    user_id: int = 1
):
    try:
        new_repo = Repository(
            user_id=user_id,
            github_url=repo_data.get("url", ""),
            name=repo_data.get("name", "Unknown"),
            owner=repo_data.get("owner", "Unknown"),
            status="completed"
        )
        db.add(new_repo)
        await db.flush() 

        new_analysis = Analysis(
            repository_id=new_repo.id,
            status="success",
            confidence_score=0.0,
            risk_score=ai_report.get("risk_score") if ai_report else None,
            ai_summary=ai_report.get("summary") if ai_report else None
        )
        db.add(new_analysis)
        await db.flush()

        for dep in parsed_dependencies:
            new_tech = Technology(
                analysis_id=new_analysis.id,
                category="dependency",
                name=dep.get("name"),
                version=dep.get("version")
            )
            db.add(new_tech)

        for file_data in analyzed_files:
            ext = file_data.file_path.split('.')[-1] if '.' in file_data.file_path else ""
            lang = "python" if ext == "py" else "unknown"

            new_file = RepositoryFile(
                analysis_id=new_analysis.id, 
                path=file_data.file_path,
                extension=ext,
                language=lang,
                functions=file_data.architecture.functions,
                classes=file_data.architecture.classes,
                imports=file_data.architecture.imports
            )
            db.add(new_file)

        for finding in security_findings:
            new_finding = SecurityFinding(
                analysis_id=new_analysis.id,
                severity=finding.get("severity", "High"),
                type=finding.get("type", "Unknown"),
                file_path=finding.get("file_path", "Unknown"),
                line_number=finding.get("line_number")
            )
            db.add(new_finding)

        await db.commit()
        return new_analysis.id

    except Exception as e:
        await db.rollback()
        raise e