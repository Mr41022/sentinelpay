from fastapi import FastAPI

app = FastAPI()

print(" MAIN.PY IS LOADED ")

@app.get("/")
def root():
    return {"message": "SentinelPay is running"}