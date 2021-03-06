import pathlib
import collections
import toml

SAVEFILE = pathlib.Path(__file__).parent / "save.toml"
SAVEFILE.touch()


class _UserData(collections.UserDict):
    def __init__(self):
        self.data = toml.load(SAVEFILE)

    def save(self):
        assert all(
            isinstance(key, str) for key in self.data
        ), "all TOML keys must be strings."
        with SAVEFILE.open("w") as f:
            toml.dump(self.data, f)

    def unlocked(self, level: int) -> bool:
        return self.completed(level - 1) or level == 0

    def completed(self, level: int) -> bool:
        return str(level) in self

    def complete(self, level: int, stars=0):
        self[str(level)] = max(stars, self.stars_in(level, 0))
        self.save()

    def stars_in(self, level: int, default=None):
        return self.get(str(level), default)


user_data = _UserData()
