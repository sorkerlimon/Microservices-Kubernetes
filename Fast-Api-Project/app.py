from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Hello ArgoCD App")


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Root endpoint that returns HTML with "hello argo cd" message
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hello ArgoCD</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                text-align: center;
                padding: 2rem;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                backdrop-filter: blur(10px);
            }
            h1 {
                font-size: 3rem;
                margin: 0;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hello Argo CD Updated</h1>
        </div>
    </body>
    </html>
    """


@app.get("/health")
async def health():
    """
    Health check endpoint
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

