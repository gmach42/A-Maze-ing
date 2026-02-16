import sys
from pydantic import (
    BaseModel,
    Field,
    StrictBool,
    ValidationError,
    field_validator,
    model_validator,
)
from typing import Any
from .errors import FormatError, MissingKey, ConfigError, TooManyVar
from .constants import (
    MIN_PIXEL_WIDTH,
    MIN_PIXEL_HEIGHT,
    MIN_ROWS,
    MIN_COLS,
    PANEL_WIDTH,
)


class EnvVariables(BaseModel):
    """
    A Pydantic model to represent the environment variables
    for the maze generation.

    Attributes:
        width (int): The width of the maze in number of cells.
        height (int): The height of the maze in number of cells.
        entry (tuple[int, int]): The coordinates of the entry point (x, y).
        exit (tuple[int, int]): The coordinates of the exit point (x, y).
        output_file (str): The name of the output file for the maze image.
        perfect (StrictBool): Whether to generate a perfect maze or not.
        cell_size (int): The size of each cell in pixels.
        wall_width (int): The width of the walls in pixels.
        animation (bool): Whether to animate the maze generation or not.
        speed_animation (str): The speed of the animation \
            ("slow", "medium", "fast").
    """

    width: int = Field(ge=MIN_COLS)
    height: int = Field(ge=MIN_ROWS)
    entry: tuple[int, int] = Field(ge=(0, 0))
    exit: tuple[int, int] = Field(ge=(0, 0))
    output_file: str
    perfect: StrictBool
    cell_size: int = 1
    wall_width: int = 1
    animation: bool = False
    speed_animation: str = "medium"
    seed: str | None = None

    @field_validator("entry", "exit", mode="before")
    @classmethod
    def check_tuple(cls, value: str) -> tuple[int, int] | None:
        """
        Validate that the entry and exit points are in the correct format
        and convert them to tuples of integers.
        """
        clean_value: str = value.replace(")", "").replace("(", "").strip()
        values: list[str] = clean_value.split(",")
        if len(values) != 2:
            raise ValueError("Wrong format tuple. Must be '(number,number)")
        try:
            val_1: int = int(values[0])
            val_2: int = int(values[1])
            return (val_2, val_1)
        except ValueError:
            raise ValueError("Entry and exit must be integers!")

    @model_validator(mode="after")
    def check_values(self) -> "EnvVariables":
        """
        Validate that entry and exit points are different
        and within maze dimensions.
        """
        if self.entry == self.exit:
            raise ValueError("Entry and exit points must be different")
        if self.entry[0] >= self.height or self.entry[1] >= self.width:
            raise ValueError("Entry coordinates must be within the maze"
                             " dimensions")
        if self.exit[0] >= self.height or self.exit[1] >= self.width:
            raise ValueError("Exit coordinates must be within the maze"
                             " dimensions")
        return self


def parsing_config(file_name: str) -> EnvVariables:
    """
    Parse the configuration file and return an
    EnvVariables instance with the values.
    """
    results: dict[str, Any] = {
        "width": None,
        "height": None,
        "entry": None,
        "exit": None,
        "output_file": None,
        "perfect": None,
        "cell_size": 40,
        "wall_width": 10,
    }
    try:
        with open(file_name, "r") as file:
            line: str = file.readline()
            while line:
                if line[0] != "#":
                    string_split: list[Any] = line.split("=")
                    if len(string_split) == 2:
                        string_split[1] = string_split[1].strip("\n").strip()
                        if string_split[0].lower() == "output_file":
                            if not string_split[1]:
                                raise MissingKey(
                                    "Missing a value for output_file variable!"
                                )
                            elif not string_split[1].endswith(".txt"):
                                raise FormatError(
                                    "Output file must end with .txt extension!"
                                )
                        if string_split[0].lower() == "seed":
                            if string_split[1].lower() == "false":
                                string_split[1] = None
                        if string_split[0].lower() in ["perfect", "animation"]:
                            if string_split[1].lower() == "true":
                                string_split[1] = True
                            elif string_split[1].lower() == "false":
                                string_split[1] = False
                            else:
                                raise MissingKey(
                                    "Missing a value for perfect variable!"
                                )
                        results[string_split[0].lower()] = string_split[1]
                    else:
                        raise FormatError("You need to use <key>=<value>"
                                          " format")
                line = file.readline()
        if len(results) > 11:
            raise TooManyVar("Too much variables in configuration file!")
        for key, value in results.items():
            if not value and key in [
                "width",
                "height",
                "entry",
                "exit",
                "output_file",
            ]:
                raise MissingKey(f"Missing a value for {key} variable!")
    except (ConfigError, OSError) as e:
        print(e)
        sys.exit(1)

    try:
        return EnvVariables(**results)
    except ValidationError as e:
        print(
            f"\nCaught a {type(e).__name__} error during parsing config.txt:",
            file=sys.stderr,
        )
        for error in e.errors():
            # Get location, defaulting to 'Configuration' if empty
            # Model validation errors may not have a specific field
            loc_tuple = error.get("loc", ())
            field = loc_tuple[0] if loc_tuple else "Configuration"
            msg = error.get("msg", "Unknown error")

            print(f"  Field '{field}': {msg}", file=sys.stderr)
        sys.exit(1)


def is_valid_window(
    env_variable: EnvVariables,
    screen_width: int,
    screen_height: int,
    win_width: int,
    win_height: int,
) -> bool:
    """
    Validate that the window dimensions are within the screen size and
    above the minimum pixel requirements.
    """

    max_width: int = int((
        screen_width - PANEL_WIDTH - env_variable.cell_size
    ) / env_variable.cell_size - 1)
    max_height: int = int((
        screen_height - env_variable.wall_width
    ) / env_variable.cell_size - 1)
    print(f"Max width for this window: {max_width}")
    print(f"Max height for this window: {max_height}\n")
    return (
        MIN_PIXEL_WIDTH < win_width <= screen_width
        and MIN_PIXEL_HEIGHT < win_height <= screen_height
    )
