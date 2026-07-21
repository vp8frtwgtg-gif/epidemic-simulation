class Person:
  """Represents one person in the population."""

  def __init__(self) -> None:
    self.virus: Optional[Virus] = None
    self.alive = True
    self.infection_frames_remaining = 0
    self.immunity_frames_remaining = 0

    #Statistics
    self.number_of_infections = 0
    self.current_infection_duration = 0
    self.completed_infection_durations = []
    self.infection_duration_before_death = None

  def die(self) -> None:
    self.infection_duration_before_death = (
        self.current_infection_duration
    )
    self.alive = False
    self.virus = None
    self.infection_frames_remaining = 0
    self.immunity_frames_remaining = 0

  def recover(self) -> None:
    self.completed_infection_durations.append(
        self.current_infection_duration
    )
    self.virus = None
    self.infection_frames_remaining = 0

    #The person remains partly protected for 4 frames.
    self.immunity_frames_remaining = 4
    self.current_infection_duration = 0

  @property
  def is_recovered(self)-> bool:
    return (
        self.alive
        and not self.is_infected
        and self.immunity_frames_remaining > 0
    )

  @property
  def is_dead(self):
    return not self.alive

  @property
  def is_infected(self) -> bool:
    return self.virus is not None

  def infect(self, virus: Virus) -> None:
    """Infect this person with a virus."""
    if not self.alive or self.is_infected:
      return

    self.virus = virus

    #The infection lasts randomly 1 to 3 timeframes.
    self.infection_frames_remaining = random.randint(1, 3)

    #A new infection ends the temporary recovery state.
    self.immunity_frames_remaining = 0
    self.number_of_infections += 1
    self.current_infection_duration = 0

  def expose_to(self, virus: Virus) -> bool:
    """
    Expose the person to a virus.

    Returns True if the person becomes newly infected.
    """
    if not self.alive or self.is_infected:
      return False

    if self.is_recovered:
      suspectibility = virus.reinfection_multiplyer
    else:
      suspectibility = 1.0

    if virus.attempts_infection(suspectibility):
      self.infect(virus)
      return True

    return False
