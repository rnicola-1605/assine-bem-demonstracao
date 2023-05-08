from Products.AppPalestra import AppPalestra as App


def initialize(context):
    """
    Inicializa o AppPalestra.

    Fazendo com que apareca na lista de produtos do zope.
    """
    context.registerClass(
        App.AppPalestra,
        constructors=(
            App.addForm,
            App.add_action,
        ),
        icon="favicon.png"
    )
