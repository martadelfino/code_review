# Adapting your project

The following are general guidelines you can follow to migrate your Python project successfully.

## Analyze your current structure

- **Identify and Organize Components**: Examine your current codebase and identify its main logical components, such as core functionality, utility functions, models, data analysis scripts, experimental setups, and result processing utilities. Without necessarily refactoring your code, organize these components into modules based on their functionality. This organization will aid in mapping your code into the `src` directory structure efficiently, facilitating easier navigation and maintenance.
- **Dependency Review**: List all external dependencies your project relies on. This will be crucial for updating the `requirements.txt` and `requirements-dev.txt` files. Use the first to list runtime packages and libraries, and the latter for all development-only packages.

## Integrate Codebase

- **Migrate Source Code**:
    - `src/`: Place your project’s primary source code into the `src` directory. If your project is module-based, each module should have its own sub-directory within `src/` and include an empty `__init__.py`.
    - Ensure to adjust any import statements if the directory structure changes during the migration.
- **Adapt Tests**: Move your tests into the `tests/` directory. It’s a good practice to mirror your project’s structure in the `tests/` directory to make it easier to locate tests for specific modules. You can use a flat hierarchy of tests if there are not many. Don't forget to adapt the `pytest` configuration file to point to the correct source code and tests directories.
- **Static Configuration Files**: Review and possibly integrate any existing configuration files (e.g., for databases, external services) with the setup already present in the repository. You may need to adapt file paths or settings based on the new structure.

## Utilize Development Tools

- **Code Quality Tools**: Leverage the pre-configured tools (`flake8`, `mypy`, `pylint`, `ruff`) to review your code and make necessary adjustments to meet the code quality standards set by the template.
- **Pre-commit Hooks**: Ensure that the `pre-commit` hooks are installed and configured to run automatically. This will help maintain code quality standards with every commit.

## Documentation

- **`README.md`**: Update the `README` to reflect your project's specifics, including its purpose, how to run it, and how to contribute. Remove or update sections that are specific to the template and not applicable to your project.
- **`CONTRIBUTING.md`**: If not already present, consider adding a contributing guide that outlines how others can contribute to your project, including coding standards, commit message guidelines, and the pull request process.

## Testing and Validation

- **Run Tests**: Ensure all tests pass in the new setup. This verifies that the integration has not broken any existing functionality.
- **Code Quality Checks**: Run the configured linters and static type checkers to identify any issues that need to be addressed to maintain code quality.
- **Manual Testing**: Perform manual tests to ensure that the application behaves as expected in its new environment.

## Final Steps

- **Commit Changes**: Once you're satisfied with the integration and all checks pass, commit your changes to the repository. Make sure to write a comprehensive commit message that describes the migration process and any significant changes made.
- **Continuous Learning**: As you adapt your project, you might discover new tools or practices that could enhance your development workflow. Keep an open mind and consider incorporating these improvements into your project.
