runNeighborhoodsPipeline([
    project: 'river-ci',
    tests: [
        'Dev/User environment Comparison': 'pipenv-devcheck',
        'Unit testing': 'python -m pytest',
        'Linting/Style Checking': "python -m flake8 river/ test/ --max-line-length 100"
    ],
])
