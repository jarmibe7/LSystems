"""
Main program for lsystems
"""
from pathlib import Path
import yaml

from .ruleset import Rule
from .lsystem import LSystem
from .render2d import RenderLSystem2D
from .render3d import RenderLSystem3D, RenderLSystem3DFly

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / "config"

def main():
    print('*** STARTING ***\n')
    # Load config
    # ---------- CONFIG HERE ----------
    config_name = '2d2'
    # ---------- CONFIG HERE ----------
    with open(CONFIG_PATH / f'{config_name}.yaml', "r") as f:
        config = yaml.full_load(f)

    # Create rules dictionary
    rules = {}
    for k in config['rules'].keys():
        mappings = []
        r = config['rules'][k]
        for kk in r.keys():
            if kk == 'ax': continue
            mappings.append(r[kk])

        rules[r['ax']] = Rule(mappings)

    # Create LSystem and generate
    lsystem = LSystem(config['axiom'], rules)
    code = lsystem.generate(config['num_gen'])
    
    # Render LSystem
    if config['should_render']:
        if config['type'] == '2D':
            renderer = RenderLSystem2D(config['render']['distance'], config['render']['theta'], update_freq=10)
            renderer.draw(code)
        elif config['type'] == '3D':
            renderer = RenderLSystem3D(config['render']['distance'], config['render']['theta'])
            renderer.draw(code)
        elif config['type'] == '3D_fly':
            renderer = RenderLSystem3DFly(config['render']['distance'], config['render']['theta'])
            renderer.draw(code)
        else:
            raise ValueError(f'Render type {config['type']} not supported...')
    else:
        print(f'Final code is: {code}')


    print('\n*** DONE ***')
    return


if __name__ == "__main__":
    main()