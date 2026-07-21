from virus import Virus
from population import Population
from simulation import Simulation

def main() -> None:
  try:
    population_density = float(
      input("Population density in percent: ")
    )

    infection_probability_percent = float(
      input(
        "Infection probability per neighbour "
        "in percent: "
      )
    )

    mortality_probability_percent = float(
        input("Mortality rate in percent: ")
    )

    virus = Virus(
        infection_probability=(infection_probability_percent / 100),
        mortality_probability=(mortality_probability_percent / 100),
        #recovery_probability=(recovery_probability_percent / 100)
    )

    population = Population(
      rows=60,
      columns=60,
      density_percent=population_density
    )

    population.infect_random_person(virus)

    simulation = Simulation(
      population=population,
      number_of_steps=50,
      interval_milliseconds=500
    )

    simulation.run()

  except ValueError as error:
    print(f"Invalid input: {error}")

  print(
      "Total infections: ", population.total_infections()
  )

  print(
      "Average infections per person:", population.average_infections_per_person()
  )

  print(
      "Average duration of recovered infections:", population.average_recovered_infection_duration()
  )

  print(
      "Average duration before death:", population.average_duration_before_death()
  )

if __name__ == "__main__":
  main()
