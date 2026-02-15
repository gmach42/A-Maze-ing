import pytest
from src import MazeGenerator, parsing_config
from pydantic import ValidationError


class TestMazeProject:

    # --- TESTS ALGORITHMIQUES ---
    def test_generator_dimensions(self):
        """Vérifie que le labyrinthe généré a les bonnes dimensions"""
        width, height = 10, 15
        generator = MazeGenerator(height, width, False)
        maze_matrix = generator.get_maze()

        assert len(maze_matrix) == height
        assert len(maze_matrix[0]) == width

    # --- TESTS DE CONFIGURATION (ERREURS) ---
    def test_parsing_invalid_file(self):
        """Vérifie que le parsing lève une erreur si le fichier n'existe pas"""
        with pytest.raises(SystemExit):
            parsing_config("fichier_inexistant.txt")

    def test_parsing_bad_values(self, tmp_path):
        """Vérifie le comportement face à des valeurs négatives"""
        # On crée un fichier temporaire corrompu
        d = tmp_path / "sub"
        d.mkdir()
        bad_config = d / "bad_config.txt"
        bad_config.write_text(
            "width=-10\nheight=20\ncell_size=10\nentry=10\n"
            "exit=10\nOUTPUT_FILE=maze.txt\nPERFECT=true\n"
        )

        # On vérifie que ton code lève bien l'erreur attendue
        with pytest.raises(SystemExit):
            parsing_config(str(bad_config))
