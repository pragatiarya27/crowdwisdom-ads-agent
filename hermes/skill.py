class BaseSkill:
    name: str = "base_skill"

    def run(self, input: dict) -> dict:
        raise NotImplementedError("Each skill must implement run()")

    def __repr__(self):
        return f"Skill({self.name})"