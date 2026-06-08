from .layer_config import LAYER_CONFIG

MAP_LAYERS = [
    (key, cfg['label'], cfg['icon'], f"{cfg['legend_min']} ... {cfg['legend_max']}")
    for key, cfg in LAYER_CONFIG.items()
]
