from dataclass import dataclass

@dataclass
class Virus:
  """Represents an illness."""

  def __init__(self, infection_probability, mortality_probability):
    self.infection_probability = infection_probability
    self.mortality_probability = mortality_probability
    self.number_of_infections = 0

  #name: str
  infection_probability: float
  mortality_probability: float
  reinfection_multiplier: float = 0.25
  #recovery_probability: float

  def __post_init__(self) -> None:
    if not 0 <= self.infection_probability <= 1:
      raise ValueError(
        "The infection probability must be between 0 and 1."
    )

  def attempts_infection(self, suspectibility: float = 1.0) -> bool:
    """Return True if one infection attempt succeeds."""
    #probability = self.infection_probability * suspectibility
    return (random.random() < self.infection_probability * suspectibility)
