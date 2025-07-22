import os

# Définir la structure de l'arborescence
structure = {
    "smart_content_engine": {
        "agents": [
            "__init__.py",
            "trend_agent.py",
            "content_agent.py",
            "reviewer_agent.py",
            "posting_agent.py"
        ],
        "core": [
            "__init__.py",
            "trend_collector.py",
            "content_generator.py",
            "content_reviewer.py",
            "linkedin_poster.py"
        ],
        "data": {
            "trends": [],
            "generated_content": [],
            "reviewed_content": [],
            "posted_content": []
        },
        "templates": [
            "business_templates_fr.json",
            "business_templates_en.json"
        ],
        "config": [
            "apis.yaml",
            "prompts.yaml"
        ],
        "": [
            ".env",
            "requirements.txt",
            "main.py",
            "linkedin_auth.py",
            "README.md"
        ]
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        os.makedirs(path, exist_ok=True)
        if isinstance(content, list):
            for file in content:
                open(os.path.join(path, file), 'a').close()
        elif isinstance(content, dict):
            create_structure(path, content)

def initialize_project():
    base_path = os.getcwd()
    create_structure(base_path, structure)
    
    # Ajouter un contenu basique à README.md et requirements.txt
    readme_path = os.path.join(base_path, "smart_content_engine", "README.md")
    with open(readme_path, "w") as f:
        f.write("# 🤖 Smart Content Engine\n\nUn moteur intelligent de génération et publication de contenu basé sur les tendances en temps réel.\n")

    reqs_path = os.path.join(base_path, "smart_content_engine", "requirements.txt")
    with open(reqs_path, "w") as f:
        f.write("openai\nrequests\naiohttp\npython-dotenv\npyyaml\n")

    print("✅ Architecture du projet créée avec succès.")

if __name__ == "__main__":
    initialize_project()
