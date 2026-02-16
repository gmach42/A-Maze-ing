import pytest
from pathlib import Path
from src import (
    MazeGenerator,
    MissingKey,
    parsing_config,
    FormatError,
    ConfigError
    )


class TestMazeProject:

    def test_generator_dimensions(self) -> None:
        """Check if generated maze has good dimension"""
        width, height = 10, 15
        generator = MazeGenerator(height, width, False)
        maze_matrix = generator.get_maze()

        assert len(maze_matrix) == height
        assert len(maze_matrix[0]) == width

    def test_parsing_invalid_file(self) -> None:
        """Check the behavior with unknown file"""
        with pytest.raises(FileNotFoundError):
            parsing_config("unknown_file.txt")

    def test_parsing_bad_values(self, tmp_path: Path) -> None:
        """Check the behavior with negative values"""

        # Creating a temp_file with wrong values
        d = tmp_path / "sub"
        d.mkdir()
        bad_config = d / "bad_config.txt"
        bad_config.write_text("width=-10\nheight=20\ncell_size=10\nentry=10\n"
                              "exit=10\nOUTPUT_FILE=maze.txt\nPERFECT=true\n")

        # Check that the program raise the expected error
        with pytest.raises(ConfigError):
            parsing_config(str(bad_config))

    def test_high_sizes(self, tmp_path: Path) -> None:
        """Check the behavior with out of range values"""
        # Creating a temp_file with wrong values
        d = tmp_path / "sub"
        d.mkdir()
        bad_config = d / "bad_config.txt"
        bad_config.write_text("width=1000\nheight=20\nentry=10,19\n"
                              "exit=10\nOUTPUT_FILE=maze.txt\nPERFECT=true\n")

        # Check that the program raise the expected error
        with pytest.raises(ConfigError):
            parsing_config(str(bad_config))

    def test_wrong_output_file(self, tmp_path: Path) -> None:
        """Check the behavior with an output file not in .txt"""
        # Creating a temp_file with wrong values
        d = tmp_path / "sub"
        d.mkdir()
        bad_config = d / "bad_config.txt"
        bad_config.write_text("width=30\nheight=20\nentry=10,19\n"
                              "exit=10,6\nOUTPUT_FILE=maze.py\nPERFECT=true\n")

        # Check that the program raise the expected error
        with pytest.raises(FormatError):
            parsing_config(str(bad_config))

    def test_missing_value(self, tmp_path: Path) -> None:
        """Check the behavior with a uncomplete config file"""
        # Creating a temp_file with wrong values
        d = tmp_path / "sub"
        d.mkdir()
        bad_config = d / "bad_config.txt"
        bad_config.write_text("width=30\nheight=20\nentry=10,19\n"
                              "exit=10,6\nPERFECT=true\n")

        # Check that the program raise the expected error
        with pytest.raises(MissingKey):
            parsing_config(str(bad_config))
