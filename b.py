import subprocess

for color in ['red', 'blue', 'green', 'yellow']:
    for i in range(10):
        subprocess.run(['mv', f'assets/cards/uno/lobby/{color}_{i}.png', f'assets/cards/uno/lobby/{i}_{color}.png'])