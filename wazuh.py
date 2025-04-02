class WazuhBenchmark:
    def __init__(self, id: int, title: str, description: str, rationale: str, remediation: str, compliance: dict[str, list[str]], references: list[str], condition: str, rules: list[str]) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.rationale = rationale
        self.remediation = remediation
        self.compliance = compliance
        self.references = references
        self.condition = condition
        self.rules = rules
