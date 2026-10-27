import uvicorn

if __name__ == "__main__":
    uvicorn.run("fastaapi", host="127.0.0.1", port=8081, reload=True)
