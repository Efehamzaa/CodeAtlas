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
    user_id: int = 1
):
    print(f"--- DB SERVİSE GELEN BAĞIMLILIKLAR: {parsed_dependencies} ---")
    
    
    new_repo = Repository(
        user_id=user_id,
        github_url=repo_data.get("url", ""),
        name=repo_data.get("name", "Unknown"),
        owner=repo_data.get("owner", "Unknown"),
        status="completed"
    )
    db.add(new_repo)
    await db.flush()  # ID'yi alabilmek için flush yapıyoruz

    
    new_analysis = Analysis(
        repository_id=new_repo.id,
        status="success",
        confidence_score=0.98
    )
    db.add(new_analysis)
    await db.flush()

    
    print(f"--- TEKNOLOJİ TABLOSUNA YAZILIYOR. Toplam adet: {len(parsed_dependencies)} ---")
    for dep in parsed_dependencies:
        new_tech = Technology(
            analysis_id=new_analysis.id,
            category="dependency",
            name=dep.get("name"),
            version=dep.get("version")
        )
        db.add(new_tech)

    
    print(f"--- MİMARİ VERİLER TABLOYA YAZILIYOR. Toplam dosya: {len(analyzed_files)} ---")
    for file_data in analyzed_files:
        # Uzantıyı ve dili dinamik olarak belirliyoruz
        ext = file_data.file_path.split('.')[-1] if '.' in file_data.file_path else ""
        lang = "python" if ext == "py" else "unknown"

        new_file = RepositoryFile(
            repository_id=new_repo.id,  # Modelin repo'ya bağlı olduğu için new_repo.id kullanıyoruz
            path=file_data.file_path,
            extension=ext,
            language=lang,
            functions=file_data.architecture.functions,
            classes=file_data.architecture.classes,
            imports=file_data.architecture.imports
        )
        db.add(new_file)

    print(f"--- GÜVENLİK BULGULARI YAZILIYOR. Toplam: {len(security_findings)} ---")
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