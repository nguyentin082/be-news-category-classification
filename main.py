from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils import TextInput, classify_text

app  = FastAPI()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Chấp nhận tất cả domain, nên đổi thành domain cụ thể trong production
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả phương thức (GET, POST, PUT, DELETE, v.v.)
    allow_headers=["*"],  # Cho phép tất cả headers
)


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/classify-text")
async def classify_category(text_input: TextInput):
    if not text_input.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")

    return classify_text(text_input.content)
