from typing import List

from fastapi import FastAPI

from spaas import models
from spaas.optimizer import SciPyDifferentialEvolutionOptimizer

app = FastAPI()


@app.post('/productionplan')
async def production_plan(power_load: models.PowerLoad) -> List[models.UnitCommitment]:
    result = SciPyDifferentialEvolutionOptimizer(target_load=power_load.load,
                                                 fuels=power_load.fuels,
                                                 power_plants=power_load.powerplants) \
        .optimize()
    return [models.UnitCommitment(name=pp.name, p=power)
            for power, pp in zip(result.x, power_load.powerplants)]
