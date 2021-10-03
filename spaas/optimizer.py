from typing import List, Iterable

import numpy as np
from scipy.optimize import differential_evolution, NonlinearConstraint, Bounds

from spaas import models


class SciPyDifferentialEvolutionOptimizer:
    def __init__(self, target_load: int, fuels: models.FuelsCosts, power_plants: List[models.PowerPlantData]):
        self.target_load = target_load
        self.fuels = fuels
        self.power_plants = power_plants
        self.power_plant_type_to_fuel = {
            'gasfired': self.fuels.gas,
            'turbojet': self.fuels.kerosene
        }

        pass

    def calc_system_load(self, x):
        sys_load = 0
        for power, pp in zip(x, self.power_plants):
            sys_load += power
        return np.array(sys_load)

    def cost_function(self, x):
        cost = 0
        for power, pp in zip(x, self.power_plants):
            fuel_cost = self.power_plant_type_to_fuel.get(pp.type, 0)
            if pp.type == 'gasfired':
                pp_cost = power * fuel_cost / pp.efficiency + power * self.fuels.co2
            else:
                pp_cost = power * fuel_cost / pp.efficiency
            cost += pp_cost
        return cost

    def generate_bounds(self) -> Iterable[Bounds]:
        def power_plant_is_on(permutation, permutation_idx):
            return ((permutation >> permutation_idx) & 1) == 1

        def power_bounds(power_plant):
            if power_plant.type == 'windturbine':
                wind_power = self.fuels.wind / 100
                return power_plant.pmin * wind_power, power_plant.pmax * wind_power
            return power_plant.pmin, power_plant.pmax

        wind_pct = self.fuels.wind / 100
        power_plants_with_min = [pp for pp in self.power_plants if pp.pmin != 0]
        for permutation in range(2 ** len(power_plants_with_min)):
            bounds = list()
            permutation_idx = 0
            for pp in self.power_plants:
                if pp.pmin != 0:
                    permutation_idx += 1
                    if power_plant_is_on(permutation, permutation_idx):
                        bounds.append(power_bounds(pp))
                    else:
                        bounds.append((0, 0))
                else:
                    bounds.append(power_bounds(pp))
            yield Bounds(*zip(*bounds))
        return Bounds(*zip(*[power_bounds(pp) for pp in self.power_plants]))

    def optimize(self):
        constraint = NonlinearConstraint(self.calc_system_load, self.target_load, +np.inf)
        best_result = None
        for bounds in self.generate_bounds():
            result = differential_evolution(self.cost_function,
                                            bounds=bounds,
                                            constraints=constraint,
                                            workers=8)
            if not result.success:
                continue
            if best_result is None:
                best_result = result
            elif self.cost_function(result.x) < self.cost_function(best_result.x):
                best_result = result
        return best_result
