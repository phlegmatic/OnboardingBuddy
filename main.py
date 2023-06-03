import os
import shutil
import subprocess
import getpass
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from fastapi import FastAPI
from pydantic import BaseModel


class RepoRequest(BaseModel):
    repo_url: str


app = FastAPI()


def download_repo(repo_url: str):
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    subprocess.run(["git", "clone", repo_url, repo_name])
    process_repo(repo_name)


@app.post("/download_repo")
async def download_repo_endpoint(git_url: RepoRequest):
    download_repo(git_url.repo_url)
    return {"message": f"Repository downloaded to folder:"}


def process_repo(repo_name: str):
    root_dir = "./the-algorithm"
    docs = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            try:
                loader = TextLoader(os.path.join(dirpath, file), encoding="utf-8")
                docs.extend(loader.load_and_split())
            except Exception as e:
                pass
