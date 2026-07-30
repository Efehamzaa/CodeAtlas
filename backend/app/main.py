from fastapi import FastAPI
from app.api import health, repository ,scanner
app = FastAPI(
    title="CodeAtlas",
    description="Understand Any Repository" ,
    version="0.1.0"
)
#@ işareti bir decarotör olarak kullanılır bir fonskiyonun ne zaman ve nasıl çalışacağını belirler.

app.include_router(health.router)
app.include_router(repository.router)
app.include_router(scanner.router)


@app.get("/")
def root():
    return{
        "message" : "Welcome to CodeAtlas"
    }


         