import sys
from pathlib import Path

# Os modulos do curriculo ficam na raiz do repositorio, fora de um pacote.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
