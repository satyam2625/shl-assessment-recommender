from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.recommender import recommend # Only need to import recommend now
from pydantic import BaseModel
from typing import List

# ... rest of your main.py code ...