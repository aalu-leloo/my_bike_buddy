import uvicorn

if __name__ == "__main__":
    uvicorn.run("fastaapi:app", host="0.0.0.0", port=8081, reload=True)
