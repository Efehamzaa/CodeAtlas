from fastapi import FastAPI

app = FastAPI(
    title="CodeAtlas",
    description="Understand Any Repository" ,
    version="0.1.0"
)
#@ işareti bir decarotör olarak kullanılır bir fonskiyonun ne zaman ve nasıl çalışacağını belirler.
@app.get("/")
def root():
    return{
        "message" : "Welcome to CodeAtlas"
    }
         