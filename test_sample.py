import pytest
from src import MazeGenerator, parsing_config, ConfigError


class TestMazeProject:

    def test_generator_dimensions(self):
        """Check if generated maze has good dimension"""
        width, height = 10, 15
        generator = MazeGenerator(height, width, False)
        maze_matrix = generator.get_maze()

        assert len(maze_matrix) == height
        assert len(maze_matrix[0]) == width

    def test_parsing_invalid_file(self):
        """Check the behavior with unknown file"""
        with pytest.raises(FileNotFoundError):
            parsing_config("unknown_file.txt")

    def test_parsing_bad_values(self, tmp_path):
        """Check the behavior with negative values"""
        # Creating a temp_file with wrong values
        d = tmp_path / "sub"
        d.mkdir()
        bad_config = d / "bad_config.txt"
        bad_config.write_text(
            "width=-10\nheight=20\ncell_size=10\nentry=10\n"
            "exit=10\nOUTPUT_FILE=maze.txt\nPERFECT=true\n"
        )

        # Check that the program raise the expected error
        with pytest.raises(ConfigError):
            parsing_config(str(bad_config))

    def test_high_sizes(self, tmp_path):
        """Vérifie le comportement face à des valeurs négatives"""
        # Creating a temp_file with wrong values
        d = tmp_path / "sub"
        d.mkdir()
        bad_config = d / "bad_config.txt"
        bad_config.write_text(
            "width=1000\nheight=20\nentry=10,19\n"
            "exit=10\nOUTPUT_FILE=maze.txt\nPERFECT=true\n"
        )

        # Check that the program raise the expected error
        with pytest.raises(ConfigError):
            parsing_config(str(bad_config))
