class Simulation:
  """Controls and displays the simulation."""

  def __init__(
    self,
    population: Population,
    number_of_steps: int = 50,
    interval_milliseconds: int = 500
  ) -> None:
    self.population = population
    self.number_of_steps = number_of_steps
    self.interval_milliseconds = interval_milliseconds

    self.figure, self.axis = plt.subplots(
      figsize=(7, 7)
    )

    self.colour_map = ListedColormap([
      "white", #empty
      "green", #healthy
      "red", #infected
      "blue", #immune and recovered
      "black", #dead
    ])

    self.image = self.axis.imshow(
      self.population.to_numeric_grid(),
      cmap=self.colour_map,
      vmin=0,
      vmax=4
    )

    self._configure_grid()

  def _configure_grid(self) -> None:
    self.axis.set_xticks(
      np.arange(
        -0.5,
        self.population.columns,
        1
      ),
      minor=True
    )

    self.axis.set_yticks(
      np.arange(
        -0.5,
        self.population.rows,
        1
      ),
      minor=True
    )

    self.axis.grid(
      which="minor",
      linewidth=0.25
    )

    self.axis.tick_params(
      which="both",
      bottom=False,
      left=False,
      labelbottom=False,
      labelleft=False
    )

  def update(self, frame):
    newly_infected = 0
    
    if frame > 0:
      newly_infected = self.population.spread_infection()

    self.image.set_data(
        self.population.to_numeric_grid()
    )

    self.axis.set_title(
      f"Week {frame} | "
      f"Healthy: {self.population.count_healthy()} | "
      f"Infected: {self.population.count_infected()} | "
      f"New: {newly_infected}"
    )

    return self.image,

  def run(self):
    self.animation = FuncAnimation(
      self.figure,
      self.update,
      frames=53,
      interval=500,
      repeat=False
    )

    plt.close(self.figure)
    display(HTML(self.animation.to_jshtml()))
    #plt.show()
