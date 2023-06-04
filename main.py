import os
import shutil
import subprocess
import getpass

# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import DeepLake
from fastapi import FastAPI
from pydantic import BaseModel
from processing import ProcessCode
from queryChat import ProcessQuery


class RepoRequest(BaseModel):
    repo_url: str


class PromptRequest(BaseModel):
    prompt: str


app = FastAPI()


def download_repo(repo_url: str):
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    subprocess.run(["git", "clone", repo_url, repo_name])
    ProcessCode(
        "/home/sashetye2001/mumhack/OnboardingBuddy/Sorting-Algorithms/",
        ["process_files"],
    ).processRepo("/home/sashetye2001/mumhack/OnboardingBuddy/Sorting-Algorithms/")


@app.post("/download_repo")
async def download_repo_endpoint(git_url: RepoRequest):
    download_repo(git_url.repo_url)
    return {"message": "Repository processed"}


@app.post("/chat_with_repo")
async def chat_repo_endpoint(prompt: PromptRequest):
    output = ProcessQuery().process(
        "Give ELI5 version of  all algorithms in repository ",
        "Sorting-Algorithms",
        "/home/sashetye2001/mumhack/OnboardingBuddy/Sorting-Algorithms/",
    )
    return {"answer": output}
