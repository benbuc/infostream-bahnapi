from infostream_bahnapi.get_arrivals import get_cached_arrivals, get_arrivals
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root_timetable():
    return get_cached_arrivals()


@app.get("/{duration}")
def arrivals_duration(duration: int):
    return get_arrivals(duration)
