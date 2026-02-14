import sys
from pydantic import (
    BaseModel,
    Field,
    StrictBool,
    ValidationError,
    field_validator,
    model_validator,
)
from .errors import FormatError, MissingKey, ConfigError, TooManyVar


class EnvVariables(BaseModel):
    width: int = Field(ge=7)
    height: int = Field(ge=7)
    entry: tuple[int, int] = Field(ge=(0, 0))
    exit: tuple[int, int] = Field(ge=(0, 0))
    output_file: str
    perfect: StrictBool
    cell_size: int = 40
    wall_width: int = 10
    animation: bool = False
    speed_animation: str = "medium"
    seed: str | None

    @field_validator("entry", "exit", mode="before")
    @classmethod
    def check_tuple(cls, value: str):
        clean_value: str = value.replace(")", "").replace("(", "").strip()
        values: list = clean_value.split(",")
        if len(values) != 2:
            raise ValueError("Wrong format tuple. Must be '(number,number)")
        try:
            val_1: int = int(values[0])
            val_2: int = int(values[1])
            return (val_2, val_1)
        except ValueError:
            raise ValueError("Entry and exit must be integers!")

    @model_validator(mode="after")
    def check_values(self):
        if self.entry[0] < 0 or self.entry[1] < 0:
            raise ValueError("Entry coordinates must be non-negative")
        if self.exit[0] < 0 or self.exit[1] < 0:
            raise ValueError("Exit coordinates must be non-negative")
        if self.entry == self.exit:
            raise ValueError("Entry and exit points must be different")
        if self.entry[0] >= self.height or self.entry[1] >= self.width:
            raise ValueError(
                "Entry coordinates must be within the maze dimensions")
        if self.exit[0] >= self.height or self.exit[1] >= self.width:
            raise ValueError(
                "Exit coordinates must be within the maze dimensions")
        return self


def parsing_config(file_name: str) -> EnvVariables:
    results = {
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
                    string_split: list = line.split("=")
                    if len(string_split) == 2:
                        string_split[1] = string_split[1].strip("\n").strip()
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
                                    "Missing a value for perfect variable!")
                        results[string_split[0].lower()] = string_split[1]
                    else:
                        raise FormatError(
                            "You need to use <key>=<value> format")
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
            f"\nCaught a {type(e).__name__} error during parsing:",
            file=sys.stderr,
        )
        print(e.errors()[0]["msg"], "\n", file=sys.stderr)
        sys.exit(1)


def is_valid_window(
    screen_width: int, screen_height: int, win_width: int, win_height: int
) -> bool:
    return 0 < win_width <= screen_width and 0 < win_height <= screen_height
