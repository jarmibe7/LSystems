"""
Main program for lsystems
"""
from pathlib import Path
import yaml

from .ruleset import Rule
from .lsystem_2d import LSystem2D
from .render import RenderLSystem2D

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
    lsystem = LSystem2D(config['axiom'], rules)
    code = lsystem.generate(config['num_gen'])
    
    # Render LSystem
    renderer = RenderLSystem2D(config['turtle']['distance'], config['turtle']['theta'], update_freq=10)
    renderer.draw(code)

    print('\n*** STARTING ***')
    return


if __name__ == "__main__":
    main()