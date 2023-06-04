import openai
from indexing import indexing
from retrieval import single_emb_search


class ProcessQuery:
    def __init__(self) -> None:
        self.indexer = indexing()
        openai.api_key = ""
        pass

    def process(self, input: str, repoName: str, repoAddress: str) -> str:
        queryEmb = self.indexer.indexQuery(input)
        retrievedOutput = single_emb_search(repoName, queryEmb, 2)
        queryFileName = retrievedOutput["fileName"].iloc[0]
        queryContext = (
            retrievedOutput["summary"].iloc[0] + retrievedOutput["summary"].iloc[1]
        )
        f = open(repoAddress + queryFileName, "r")
        queryFileText = f.read()

        finalQuery = (
            input
            + """
        """
            + queryFileText
            + """
        """
            + queryContext
        )
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": finalQuery}]
        )
        finalResponse = completion.choices[0].message["content"]

        return finalResponse



