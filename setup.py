from distutils.core import setup

setup(
    name='md2pdf',
    version='1.0',
    py_modules=['md2pdf', 'tempfileServer'],
    entry_points={
        'console_scripts': [
            'md2pdf = md2pdf:main',
        ],
    }
)

