from pathlib import Path

KNOWLEDGE_BASE_DIR = (Path(__file__).parent.parent.parent / "knowledge_base")

def load_documents() -> list[dict]:
    documents =[]

    for file_path in KNOWLEDGE_BASE_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")
        documents.append(
            {
                "source" : file_path.name,
                "content" : content
            }
        )
    return documents