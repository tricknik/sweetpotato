from distutils.core import setup
setup(name='sweetpotato',
    version='0.1',
    description='Process Automation System',
    author='Dmytri Kleiner',
    author_email='dk@telekommunisten.net',
    url='http://www.telekommunisten.net/sweetpotato',
    scripts=['sp'],
    packages=['sweetpotato', 'sweetpotato.tasks', 'sweetpotato.extensions'],
)

