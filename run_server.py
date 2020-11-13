import uvicorn
# don't delete the import below
import main

if __name__ == '__main__':
    # Development
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)