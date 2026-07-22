import random
import numpy as np

from typing import Optional
from person import Person
from virus import Virus

class Population:
  """Represents a grid containing people and empty fields."""

  NEIGHBOUR_DIRECTIONS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
  ]

  def __init__(
    self,
    rows: int,
    columns: int,
    density_percent: float
  ) -> None:
    if rows <= 0 or columns <= 0:
      raise ValueError(
        "Rows and columns must be positive."
      )

    if not 0 <= density_percent <= 100:
      raise ValueError(
        "Population density must be between 0 and 100."
    )

    self.rows = rows
    self.columns = columns

    # Each field contains either a Person or None.
    self.grid: list[list[Optional[Person]]] = [
      [None for _ in range(columns)]
      for _ in range(rows)
    ]

    self._place_people(density_percent)

  def _place_people(self, density_percent: float) -> None:
    """Randomly place the requested number of people."""

    number_of_fields = self.rows * self.columns
    number_of_people = round(
      density_percent / 100 * number_of_fields
    )

    all_positions = [
      (row, column)
      for row in range(self.rows)
      for column in range(self.columns)
    ]

    occupied_positions = random.sample(
      all_positions,
      number_of_people
    )

    for row, column in occupied_positions:
      self.grid[row][column] = Person()

  def get_people(self) -> list[Person]:
    """Return all people in the population."""

    return [
      person
      for row in self.grid
      for person in row
      if person is not None
      ]

  def infect_random_person(self, virus: Virus) -> None:
    """Infect one random person."""

    people = self.get_people()

    if not people:
      raise ValueError(
        "The population contains no people."
      )

    patient_zero = random.choice(people)
    patient_zero.infect(virus)

  def get_neighbours(
    self,
    row: int,
    column: int
  ) -> list[Person]:
    """Return the people in the eight neighbouring fields."""

    neighbours = []

    for row_change, column_change in self.NEIGHBOUR_DIRECTIONS:
      neighbour_row = row + row_change
      neighbour_column = column + column_change

      inside_grid = (
        0 <= neighbour_row < self.rows
        and 0 <= neighbour_column < self.columns
      )

      if not inside_grid:
        continue

      neighbour = self.grid[
        neighbour_row
      ][
        neighbour_column
      ]

      if neighbour is not None:
        neighbours.append(neighbour)

    return neighbours

  def spread_infection(self) -> int:
    """
    Perform one simulation step.

    Returns the number of newly infected people.
    """

    infections_to_apply: list[tuple[Person, Virus]] = []

    # Remember who was infected at the beginning of the frame.
    infected_people_at_start: list[Person] = []

    for row in range(self.rows):
      for column in range(self.columns):
        person = self.grid[row][column]

        if (
          person is None
          or not person.alive
          or not person.is_infected
        ):
          continue

        infected_people_at_start.append(person)

        virus = person.virus

        if virus is None:
          continue

        for neighbour in self.get_neighbours(row, column):
          if not neighbour.alive or neighbour.is_infected:
            continue

          # Recovered people are less likely to be infected.
          if neighbour.immunity_frames_remaining > 0:
            susceptibility = virus.reinfection_multiplier
          else:
            susceptibility = 1.0

          if virus.attempts_infection(susceptibility):
            infections_to_apply.append(
              (neighbour, virus)
            )

    newly_infected = 0
    already_processed: set[Person] = set()

    for person, virus in infections_to_apply:
      if person in already_processed:
        continue

      person.infect(virus)
      already_processed.add(person)
      newly_infected += 1

    # Death or recovery for people who were infected
    # at the beginning of this frame.
    for person in infected_people_at_start:
      if not person.alive or not person.is_infected:
        continue

      virus = person.virus

      if virus is None:
        continue

      person.current_infection_duration += 1

      if random.random() < virus.mortality_probability:
        person.die()
        continue

      person.infection_frames_remaining -= 1

      if person.infection_frames_remaining <= 0:
        person.recover()

    # Reduce temporary immunity for recovered people.
    for person in self.get_people():
      if (
        person.alive
        and not person.is_infected
        and person.immunity_frames_remaining > 0
      ):
        person.immunity_frames_remaining -= 1

    return newly_infected

  def count_healthy(self) -> int:
    return sum(
      person.alive
      and not person.is_infected
      for person in self.get_people()
    )

  def count_infected(self) -> int:
    return sum(
      person.is_infected
      for person in self.get_people()
    )


  def to_numeric_grid(self) -> np.ndarray:
    """
    Convert the object grid into numbers for Matplotlib.

    0 = empty
    1 = healthy
    2 = infected
    3 = temporarily recovered
    4 = dead
    """

    numeric_grid = np.zeros(
      (self.rows, self.columns),
      dtype=int
    )

    for row in range(self.rows):
      for column in range(self.columns):
        person = self.grid[row][column]

        if person is None:
          numeric_grid[row, column] = 0
        elif person.is_dead:
          numeric_grid[row, column] = 4
        elif person.is_recovered:
          numeric_grid[row, column] = 3
        elif person.is_infected:
          numeric_grid[row, column] = 2
        else:
          numeric_grid[row, column] = 1

    return numeric_grid

  def count_dead(self) -> int:
    return sum(
        person.is_dead
        for person in self.get_people()
    )
    
  def total_infections(self) -> int:
    return sum(
        person.number_of_infections
        for person in self.get_people()
    )

  def average_infections_per_person(self) -> float:
    people = self.get_people()

    if not people:
      return 0.0

    return(
        self.total_infections() / len(people)
    )

  def average_recovered_infection_duration(self) -> float:
    durations = [
        duration
        for person in self.get_people()
        for duration in person.completed_infection_durations
    ]

    if not durations:
      return 0.0

    return sum(durations) / len(durations)

  def average_duration_before_death(self) -> float:
    durations = [
        person.infection_duration_before_death
        for person in self.get_people()
        if person.infection_duration_before_death is not None
    ]

    if not durations:
      return 0.0

    return sum(durations) / len(durations)
