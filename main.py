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
    repo: str
    query: str


app = FastAPI()


def download_repo(repo_url: str):
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    subprocess.run(["git", "clone", repo_url, repo_name])
    folder_name = "process_files"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created successfully.")
    else:
        print(f"Folder '{folder_name}' already exists.")
    ProcessCode(
        f"/home/sashetye2001/mumhack/OnboardingBuddy/{repo_name}/",
        [f"{folder_name}"],
    ).processRepo(f"/home/sashetye2001/mumhack/OnboardingBuddy/{repo_name}/")
    return repo_name


@app.post("/download_repo")
async def download_repo_endpoint(git_url: RepoRequest):
    repo_name = download_repo(git_url.repo_url)
    return {"message": repo_name}


@app.post("/chat_with_repo")
async def chat_repo_endpoint(prompt: PromptRequest):
    output = ProcessQuery().process(
        prompt.query,
        prompt.repo,
        f"/home/sashetye2001/mumhack/OnboardingBuddy/{prompt.repo}/",
    )
    return {"answer": output}
