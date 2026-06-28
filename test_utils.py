import utils

utils.ensure_directories()

utils.check_dependencies()

utils.info("Hola")

utils.warn("Advertencia")

utils.ok("Todo correcto")

with utils.Timer():
    sum(range(10_000_000))
