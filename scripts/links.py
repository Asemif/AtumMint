import main
import gui
import math

grid_x, grid_y, grid = [], [], []
for x in range(0, math.ceil(main.SCREEN_WIDTH/(16+(64+16*2.1)))):
    grid_x.append(16*1.5+(64+16*2.1)*x)
for y in range(0, math.floor(main.SCREEN_HEIGHT/(104+9))):
    grid_y.append(16+(104+9)*y)

for i in grid_x:
    for j in grid_y:
        grid.append([j, i])

unititled_normal = "exe"

main.links.add(gui.Link(grid[0][0], grid[0][1], "Менеджер\nПрограм\nModern", "main.windows.add(ProgramManModern(150, 150))", unititled_normal, gui.font_size-1))
main.links.add(gui.Link(grid[1][0], grid[1][1], "Менеджер\nТем Modern", "main.windows.add(ThemeManModern(150, 150))", unititled_normal, gui.font_size-1))
main.links.add(gui.Link(grid[2][0], grid[2][1], "Тест", "main.windows.add(Base(150, 150))", unititled_normal, gui.font_size-1))
main.links.add(gui.Link(grid[3][0], grid[3][1], "Тест 2", "exec(open('apps/test.py', encoding='UTF-8').read())", unititled_normal, gui.font_size-1))