from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from contextlib import asynccontextmanager

from langchain.chat_models import ChatOpenAI
import firebase_admin
from firebase_admin import credentials

from app.config import CONFIG
from app.models.user import User, UserDAO
from app.models.translate import Word
from app.models.completion import Model

from dotenv import load_dotenv
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.db = AsyncIOMotorClient(CONFIG.mongo_uri).grawk
    app.audio_bucket = AsyncIOMotorGridFSBucket(app.db, bucket_name='audio')
    await init_beanie(
        app.db, 
        document_models=[
            User,
            UserDAO,
            Word,
            Model,
        ]
    )
    yield

app = FastAPI(
    lifespan=lifespan,
)

cred = credentials.Certificate('./firebase-key.json')
firebase_admin.initialize_app(cred)
llm = ChatOpenAI()
