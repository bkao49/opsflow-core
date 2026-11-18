import os

# pytest lit conftest.py AVANT d'importer tes fichiers de test.
# On définit donc la variable ici, avant que "app.database" soit importé.
os.environ["DATA_BASE_URL"] = "sqlite://"   # base SQLite en mémoire, jetable