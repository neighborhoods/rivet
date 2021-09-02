runNeighborhoodsPipeline([
    project: 'rivet-ci',
    tests: [
        'Dev/User environment Comparison': 'pipenv-devcheck',
        'Unit testing': 'python -m pytest test/',
        'Linting/Style Checking': "python -m flake8 rivet/ test/ --max-line-length 100"
    ],
])
