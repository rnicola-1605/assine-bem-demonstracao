import os
import json


def __get_directory():
    """."""
    import pathlib

    return pathlib.Path(__file__).parent.resolve()


def main():
    """Gera os arquivos products.cfg."""
    path = __get_directory()
    if not os.path.exists("{}/run.ack".format(path)):

        instance_path = os.environ['INSTANCE_PATH']

        path_conf = "{}/etc/zope.conf".format(instance_path)

        with open(
            "{}/products_template.cfg".format(path)) as template, open(
            path_conf, "a"
        ) as products, open("/run/secrets/pag_secrets") as secrets:

            render = "\n" + template.read().format(
                **json.loads(secrets.read())
            )
            products.write(render)

        with open("{}/run.ack".format(path), "w") as run:
            run.write("Already ran")


if __name__ == "__main__":
    main()
else:
    raise NotImplementedError("Module should not be imported.")
