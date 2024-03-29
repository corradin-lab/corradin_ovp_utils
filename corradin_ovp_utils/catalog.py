# AUTOGENERATED! DO NOT EDIT! File to edit: catalog.ipynb (unless otherwise specified).

__all__ = ['cd', 'change_cwd_dir', 'get_config', 'get_catalog', 'reload_catalog', 'reload', 'package_outer_folder',
           'catalog_folder', 'test_patterns', 'conf_test_data_catalog', 'test_data_catalog', 'test_patterns',
           'conf_test_data_catalog', 'test_data_catalog']

# Cell

from kedro.config import ConfigLoader
from kedro.io import DataCatalog
from fastcore.meta import delegates

# Cell

from functools import wraps
from contextlib import contextmanager

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

def change_cwd_dir(new_dir):
    def decorator(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            with cd(new_dir):
                func_result = func(*args, **kwargs)
            return func_result
        return wrapped_func
    return decorator



# Cell

from kedro.config import ConfigLoader
from kedro.io import DataCatalog
import os
from pathlib import Path

package_outer_folder = Path(__file__).parents[1]
catalog_folder = Path(__file__).parents[0]

@change_cwd_dir(new_dir = catalog_folder)
def get_config(env="base", patterns=['catalog*', 'catalog*/*/','catalog*/*/*']):
    # Initialise a ConfigLoader
    conf_loader = ConfigLoader(f"conf/{env}")
    yaml_patterns = [f"{pattern}.yaml" for pattern in patterns]
    yml_patterns = [f"{pattern}.yml" for pattern in patterns]

    all_patterns = yml_patterns + yaml_patterns
    # Load the data catalog configuration from catalog.yml
    conf= conf_loader.get(*all_patterns)

    return conf


@change_cwd_dir(new_dir = catalog_folder)
def get_catalog(env="base", patterns=['catalog*', 'catalog*/*/','catalog*/*/*']):
    conf_catalog = get_config(env=env, patterns = patterns)

    # Create the DataCatalog instance from the configuration
    catalog = DataCatalog.from_config(conf_catalog)
    catalog.load = change_cwd_dir(catalog_folder)(catalog.load)
    catalog.env = env
    catalog.patterns = patterns
    catalog.reload = reload.__get__(catalog)
    return catalog

def reload_catalog(catalog):
    return get_catalog(catalog.env, catalog.patterns)

def reload(self):
    return reload_catalog(self)

test_patterns = ["test_catalog*/*", "test_catalog"]
conf_test_data_catalog = get_config(patterns = test_patterns)
test_data_catalog = get_catalog(patterns = test_patterns)
#test_parameters = get_config("base", ["parameters*.yml","parameters*.yaml", "parameters*/*.yml", "parameters*/*.yaml"])



# Cell
test_patterns = ["test_catalog*/*", "test_catalog*"]
conf_test_data_catalog = get_config(patterns = test_patterns)
test_data_catalog = get_catalog(patterns = test_patterns)
#test_data_catalog_cluster = get_catalog(patterns = test_patterns, env = "cluster")