# Epidemic Simulation

An object-oriented epidemic simulation written in Python.

The program models the spread of an infectious disease through a two-dimensional population.
People occupy randomly selected cells in a grid and may infect individuals in any of their eight neighbouring cells.

The simulation includes infection, recovery, temporary partial immunity, reinfection and mortality.
The development of the epidemic is displayed as an animated grid.

## Features

- Adjustable population density
- Adjustable infection probability
- Adjustable mortality probability
- Infection through all eight neighbouring cells
- Random infection duration of one to three simulation steps (interpreted as weeks)
- Temporary partial immunity for four simulation steps/weeks after recovery
- Reduced probability of reinfection
- Random placement of people in the population
- Animated visualization with Matplotlib
- Tracking of infection and mortality statistics

## Individual States

The animation uses the following colours:

| Colour | State |
|---|---|
| White | Empty cell |
| Green | Healthy person |
| Red | Infected person |
| Blue | Temporarily recovered person |
| Black | Dead person |

## Project Structure

epidemic-simulation/
├── main.py
├── virus.py
├── person.py
├── population.py
├── simulation.py
├── requirements.txt
└── README.md

### virus.py

Defines the Virus class and stores the infection probability, mortality probability and reinfection multiplier.

### person.py

Defines the Person class. A person can be healthy, infected, temporarily recovered or dead.
The class also records individual infection statistics.

### population.py

Defines the Population class.
It creates the grid, places people, finds neighbours and performs the epidemic transitions during each simulation step.

### simulation.py

Defines the Simulation class and produces the animated Matplotlib visualization.

### main.py

Requests the model parameters from the user, creates the objects and starts the simulation.

## Model

The population is represented by a rectangular cellular grid.
Every occupied cell contains one Person.

Each infected person can attempt to infect people in the eight surrounding cells.
Infection attempts are probabilistic.

To prevent a newly infected person from spreading the illness immediately, all infections are collected first and applied only after the infection attempts for the current simulation step have been completed.

An infected person remains infected for a randomly selected duration of one to three simulation steps.
During each infected step, the person may die according to the configured mortality probability.

After recovery, a person has temporary partial immunity for four simulation steps.
During this period, the infection probability is multiplied by the virus's reinfection multiplier.

## Statistics

The program currently reports:

- Total number of infection episodes
- Average number of infections per person
- Average duration of completed infections
- Average infection duration before death
- Number of healthy people during each simulation step
- Number of infected people during each simulation step
- Number of newly infected people during each simulation step

A person can contribute more than once to the total number of infections if they become reinfected.

## Requirements

- Python 3
- NumPy
- Matplotlib
- IPython or Google Colab for notebook animation output

Install the required packages with:

```bash
pip install numpy matplotlib ipython
```

Alternatively, install them from requirements.txt:

```bash
pip install -r requirements.txt
```

## Running the Simulation

Run:

```bash
python main.py
```

The program asks for:

1. Population density in percent
2. Infection probability per neighbouring person in percent
3. Mortality probability in percent

Example input:

text
Population density in percent: 70
Infection probability per neighbour in percent: 25
Mortality rate in percent: 3


## Limitations

This is a simplified stochastic model and is not intended to predict the spread of a real disease.

In particular:

- People do not move.
- Every person has the same infection and mortality probabilities.
- Infection is possible only between neighbouring grid cells.
- Age, vaccination status and other individual differences are not modelled.
- One simulation step does not necessarily correspond to a real calendar week.

## Possible Future Improvements

- Run repeated simulations and compare average outcomes
- Record peak infection numbers and the time of the peak
- Display graphs of infections and deaths over time
- Introduce age-dependent mortality
- Add vaccination
- Add movement between cells
- Support different neighbourhood structures
- Export simulation statistics to a file

## Purpose

This project was created to practise:

- Object-oriented programming in Python
- Stochastic simulation
- Cellular automata
- Collection and evaluation of simulation statistics
- Data visualization with Matplotlib
- Organizing a Python program across multiple modules

## Example Simulation

![Simulation](epidemic_simulation.mov)
