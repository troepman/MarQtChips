"""Setup the BlueChips application"""
import logging

from bluechips.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup bluechips here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Load the models
    from bluechips.model import meta
    meta.metadata.bind = meta.engine

    # Create the tables if they aren't there already
    meta.metadata.create_all(checkfirst=True)
