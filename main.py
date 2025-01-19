import json
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from mypy_boto3_textract.type_defs import DetectDocumentTextResponseTypeDef

## arquivos para ocr
listas = ['Lista-compras.jpg','lista-material-escolar.jpeg']

def detect_file_text() -> None:
    client = boto3.client("textract")

    for items in listas:
        file_path = str(Path(__file__).parent / "images" / items)
        with open(file_path, "rb") as f:
            document_bytes = f.read()

        try:
            response = client.detect_document_text(Document={"Bytes": document_bytes})
            with open(f"{items}.json", "w") as response_file:
                response_file.write(json.dumps(response))
        except ClientError as e:
            print(f"Erro processando documento: {e}")
    # file_path = str(Path(__file__).parent / "images" / "lista-material-escolar.jpeg")
    # with open(file_path, "rb") as f:
    #     document_bytes = f.read()

    # try:
    #     response = client.detect_document_text(Document={"Bytes": document_bytes})
    #     with open("response.json", "w") as response_file:
    #         response_file.write(json.dumps(response))
    # except ClientError as e:
    #     print(f"Erro processando documento: {e}")


def get_lines() -> list[str]:
    try:
        ## iterar em cada arquivo json
        for arquivos in listas:
            with open(f"{arquivos}.json", "r") as f:
                data: DetectDocumentTextResponseTypeDef = json.loads(f.read())
                blocks = data["Blocks"]
                for block in blocks:
                    if block["BlockType"] == "LINE":
                        print(block["Text"])
            print("--------------------------------------------------\n")
        # for arquivo in listas:
        #     with open(f"{arquivo}.json", "r") as f:
        #         data: DetectDocumentTextResponseTypeDef = json.loads(f.read())
        #         blocks = data["Blocks"]
        #     return [block["Text"] for block in blocks if block["BlockType"] == "LINE"]  # type: ignore
    except IOError:
        detect_file_text()
    return []


if __name__ == "__main__":
    get_lines()
