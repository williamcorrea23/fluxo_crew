import sys, os

# Adiciona o path do projeto
project_home = '/home/elboca/webapp-crew-transform'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Exporta variáveis .env
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Importa o app Flask
from app import app as application
