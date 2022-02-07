setup(name='pgn2docx',
    version='0.1',
    description='generates a docx file for each game in a pgn-file',
    url='https://github.com/hlotze/pgn2docx',
    author='hlotze',
    author_email='hlotze@yahoo.com',
    license='GNU v2.0',
    packages=['pgn2docx'],
          install_requires=[
          'numpy',
          'pandas',
          'chess',
          'docx'
      ],
    zip_safe=False
)