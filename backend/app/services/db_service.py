from sqlalchemy.ext.asyncio import AsyncSession
from app.models.core import Repository
from app.models.analysis import Analysis
from app.models.findings import Technology

async def save_analysis_results(db: AsyncSession, repo_data: dict, parsed_dependencies: list, user_id: int = 1):
    print(f"--- DB SERVİSE GELEN BAĞIMLILIKLAR: {parsed_dependencies} ---")
    
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
        confidence_score=0.98
    )
    db.add(new_analysis)
    await db.flush()

    print(f"--- TEKNOLOJİ TABlosuna YAZILIYOR. Toplam adet: {len(parsed_dependencies)} ---")
    for dep in parsed_dependencies:
        new_tech = Technology(
            analysis_id=new_analysis.id,
            category="dependency",
            name=dep.get("name"),
            version=dep.get("version")
        )
        db.add(new_tech)

    await db.commit()
    return new_analysis.id