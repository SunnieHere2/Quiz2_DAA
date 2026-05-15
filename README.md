# MinesweeperPlus

A custom implementation of the classic Minesweeper game built using Python and the **Pygame** library.

## 📋 Table of Contents
- [About](#about)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Project Structure](#project-structure)
- [Credits](#credits)

## 🧐 About
MinesweeperPlus is a strategy logic puzzle game. The objective is to clear a rectangular board containing hidden "mines" or bombs without detonating any of them, with help from clues about the number of neighboring mines in each field.

## 🛠 Prerequisites
Before running the game, ensure you have the following installed on your machine:

1.  **Python 3.x**: [Download Python](https://www.python.org/downloads/)
2.  **Pygame Library**: This project relies on Pygame for rendering and game logic.

## ⚙️ Installation

1.  **Clone the Repository**
    Open your terminal or command prompt and run the following command to download the project:
    ```bash
    git clone [https://github.com/BismantakaRD/MinesweeperPlus.git](https://github.com/BismantakaRD/MinesweeperPlus.git)
    ```

2.  **Navigate to the Directory**
    Enter the project folder:
    ```bash
    cd MinesweeperPlus
    ```

3.  **Install Dependencies**
    Install the required Pygame library using pip:
    ```bash
    pip install pygame
    ```

## 🚀 How to Run

Based on the repository structure, the source code is located inside the inner `MinesweeperPlus` folder. Follow these steps to launch the game:

1.  **Navigate to the Source Code**
    Make sure you are in the directory containing `main.py`. If you are in the root folder, type:
    ```bash
    cd MinesweeperPlus
    ```

2.  **Execute the Game**
    Run the `main.py` file to start the application:
    ```bash
    python main.py
    ```
    *(Note: If `python` doesn't work, try using `python3` instead).*

## 📂 Project Structure

Here is a brief overview of the files in this project:

* **`main.py`**: The entry point of the game. Run this file to play.
* **`game_logic.py`**: Handles the core mechanics (mine generation, neighbor calculation).
* **`cell.py`**: Defines the properties of a single cell on the board.
* **`menu.py`**: Manages the game menus and UI states.
* **`renderer.py`**: Handles the drawing of graphics to the screen.
* **`constants.py`**: Stores configuration variables (screen size, colors, grid size).
* **`how_to_play.py`**: Instructions for the player.

## 👤 Credits

**Made by:** Bismantaka Revano D., Razan Widya Reswara, Ramasyamsi Ahmad Shabri
