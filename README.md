# HBNB - The Console

Welcome to HBNB Console! This repository hosts the initial phase of a student project aimed at creating a clone of the popular AirBnB website. In this stage, we have developed a backend interface, or console, to manage program data. Through console commands, users can create, update, and destroy objects, as well as manage file storage. Persistent storage is facilitated using JSON serialization/deserialization.

---

## Project Tasks and Repository Contents

The repository contents are organized according to the tasks completed for the project:

| Tasks | Files | Description |
| ----- | ----- | ----------- |
| 0: Authors/README File | [AUTHORS](https://github.com/justinmajetich/AirBnB_clone/blob/dev/AUTHORS) | Lists project authors |
| 1: Pep8 | N/A | All code is pep8 compliant |
| 2: Unit Testing | [/tests](https://github.com/justinmajetich/AirBnB_clone/tree/dev/tests) | Unit tests for all class-defining modules |
| 3. Make BaseModel | [/models/base_model.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/base_model.py) | Defines a parent class inherited by all model classes |
| 4. Update BaseModel w/ kwargs | [/models/base_model.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/base_model.py) | Adds functionality to recreate an instance from a dictionary representation |
| 5. Create FileStorage class | [/models/engine/file_storage.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/engine/file_storage.py), [/models/__init__.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/__init__.py), [/models/base_model.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/base_model.py) | Manages persistent file storage system |
| 6. Console 0.0.1 | [console.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/console.py) | Adds basic functionality to console program for quitting, handling empty lines, and ^D |
| 7. Console 0.1 | [console.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/console.py) | Updates console with methods for creating, destroying, showing, and updating stored data |
| 8. Create User class | [console.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/console.py), [/models/engine/file_storage.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/engine/file_storage.py), [/models/user.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/user.py) | Dynamically implements a user class |
| 9. More Classes | [/models/user.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/user.py), [/models/place.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/place.py), [/models/city.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/city.py), [/models/amenity.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/amenity.py), [/models/state.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/state.py), [/models/review.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/review.py) | Dynamically implements more classes |
| 10. Console 1.0 | [console.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/console.py), [/models/engine/file_storage.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/engine/file_storage.py) | Updates console and file storage system to work dynamically with all classes and updates file storage |

## General Usage

1. Clone this repository.

2. Navigate to the cloned directory.

3. Run the console.py file:

    ```bash
    /AirBnB_clone$ ./console.py
    ```

4. The console prompt `(hbnb)` will appear, indicating you are in the HBNB console. Various commands are available for interaction.

#### Commands

- `create`: Creates an instance based on the given class.
- `destroy`: Destroys an object based on class and UUID.
- `show`: Shows an object based on class and UUID.
- `all`: Shows all objects the program has access to, or all objects of a given class.
- `update`: Updates existing attributes of an object based on class name and UUID.
- `quit`: Exits the program (EOF will as well).

#### Alternative Syntax

Advanced syntax is implemented for the following commands:

- `all`: Shows all objects the program has access to, or all objects of a given class.
    - `count`: Returns the number of object instances by class.
- `show`: Shows an object based on class and UUID.
    - `destroy`: Destroys an object based on class and UUID.
- `update`: Updates existing attributes of an object based on class name and UUID.

## Examples

### Primary Command Syntax

#### Example 0: Create an object

Usage: `create <class_name>`

```bash
(hbnb) create BaseModel

