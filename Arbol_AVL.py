import pygame
import sys
from pygame.locals import *

class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0

class AVL:
    def __init__(self):
        self.root = None
        self.size = 0


    def newHeight(self, node):
        while node is not None:
            height_left = node.left.height if node.left else 0
            height_right = node.right.height if node.right else 0
            node.height = 1 + max(height_left, height_right)
            node = node.parent

    def add(self, value):
        new_node = Node(value)
        if self.root is None:
            self.root = new_node
        else:
            node = self.root
            while node is not None:
                if value < node.value:
                    if node.left is None:
                        node.left = new_node
                        new_node.parent = node
                        break
                    else:
                        node = node.left
                elif value > node.value:
                    if node.right is None:
                        node.right = new_node
                        new_node.parent = node
                        break
                    else:
                        node = node.right
                else:
                    break
        self.newHeight(new_node)
        self.balance(new_node)

    def find(self, value):
        node = self.root
        while node is not None:
            if value == node.value:
                return node
            elif value < node.value:
                node = node.left
            else:
                node = node.right
        return None

    def delete(self, value):
        node = self.root
        while node is not None:
            if value == node.value:
                if node.left is None and node.right is None:
                    if node == self.root:
                        self.root = None
                    else:
                        if node.parent.left == node:
                            node.parent.left = None
                        else:
                            node.parent.right = None
                elif node.left is not None and node.right is not None:
                    temp = node.right
                    while temp.left is not None:
                        temp = temp.left
                    node.value = temp.value
                    node = temp
                    if node.right:
                        node.parent.left = node.right
                        node.right.parent = node.parent
                    else:
                        if node.parent.left == node:
                            node.parent.left = None
                        else:
                            node.parent.right = None
                else:
                    child = node.left if node.left else node.right
                    if node == self.root:
                        self.root = child
                    else:
                        if node.parent.left == node:
                            node.parent.left = child
                        else:
                            node.parent.right = child
                    if child is not None:
                        child.parent = node.parent

                if node.parent:
                    self.newHeight(node.parent)
                    self.balance(node.parent)
                break
            elif value < node.value:
                node = node.left
            else:
                node = node.right

    def balance(self, node):
        while node is not None:
            height_left = node.left.height if node.left else 0
            height_right = node.right.height if node.right else 0
            balance_factor = height_left - height_right
            if balance_factor > 1:
                if node.left and node.left.right:
                    self.left_R(node.left)
                self.right_R(node)
            elif balance_factor < -1:
                if node.right and node.right.left:
                    self.right_R(node.right)
                self.left_R(node)
            node = node.parent

    def left_R(self, node):
        newRoot = node.right
        if newRoot is None:
            return
        node.right = newRoot.left
        if newRoot.left:
            newRoot.left.parent = node
        newRoot.parent = node.parent
        if node == self.root:
            self.root = newRoot
        elif node == node.parent.left:
            node.parent.left = newRoot
        else:
            node.parent.right = newRoot
        newRoot.left = node
        node.parent = newRoot
        self.newHeight(node)
        self.newHeight(newRoot)

    def right_R(self, node):
        newRoot = node.left
        if newRoot is None:
            return
        node.left = newRoot.right
        if newRoot.right:
            newRoot.right.parent = node
        newRoot.parent = node.parent
        if node == self.root:
            self.root = newRoot
        elif node == node.parent.right:
            node.parent.right = newRoot
        else:
            node.parent.left = newRoot
        newRoot.right = node
        node.parent = newRoot
        self.newHeight(node)
        self.newHeight(newRoot)

    def double_left_R(self, node):
        self.right_R(node.left)
        self.left_R(node)

    def double_right_R(self, node):
        self.left_R(node.right)
        self.right_R(node)

    def is_empty(self):
        return self.root is None

    def in_order(self, node):
        return (self.in_order(node.left) + [node.value] + self.in_order(node.right)) if node else []

    def pre_order(self, node):
        return [node.value] + self.pre_order(node.left) + self.pre_order(node.right) if node else []

    def post_order(self, node):
        return self.post_order(node.left) + self.post_order(node.right) + [node.value] if node else []

    def get_root(self):
        return self.root


pygame.init()
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Árbol AVL con Pygame")
font = pygame.font.Font(None, 24)  # Tamaño de fuente
input_box = pygame.Rect(100, 20, 110, 30)
button_rect_insert = pygame.Rect(230, 20, 80, 30)
button_rect_remove = pygame.Rect(320, 20, 81, 30)
button_rect_preorder = pygame.Rect(411, 20, 90, 30)
button_rect_inorder = pygame.Rect(511, 20, 81, 30)
button_rect_postorder = pygame.Rect(602, 20, 95, 30)
button_rect_find = pygame.Rect(700, 20, 80, 30)
input_text = ''
active = False
color_active = pygame.Color('dodgerblue2')
color_inactive = pygame.Color('lightskyblue3')
color = color_inactive
arbol = AVL()
order_output = ""
find_output = ""


def draw_tree(node, x, y, offset_x):
    if node is not None:
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 20)  # Nodo blanco
        pygame.draw.circle(screen, (0, 0, 0), (x, y), 20, 2)  # Borde negro
        text_surface = font.render(str(node.value), True, (0, 0, 0))  # Texto negro
        screen.blit(text_surface, (x - 10, y - 10))

        if node.left:
            pygame.draw.line(screen, (0, 0, 0), (x, y + 20), (x - offset_x, y + 60), 2)
            draw_tree(node.left, x - offset_x, y + 60, offset_x // 2)
        if node.right:
            pygame.draw.line(screen, (0, 0, 0), (x, y + 20), (x + offset_x, y + 60), 2)
            draw_tree(node.right, x + offset_x, y + 60, offset_x // 2)


def split_text(text, font, max_width):
    lines = []
    words = text.split(' ')
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def main():
    global input_text, active, color, order_output, find_output

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive

                if button_rect_insert.collidepoint(event.pos):
                    if input_text.isdigit():
                        arbol.add(int(input_text))
                    input_text = ''

                if button_rect_remove.collidepoint(event.pos):
                    if input_text.isdigit():
                        arbol.delete(int(input_text))
                    input_text = ''

                if button_rect_find.collidepoint(event.pos):
                    if input_text.isdigit():
                        found_node = arbol.find(int(input_text))
                        find_output = f"Nodo encontrado: {found_node.value}" if found_node else "Nodo no encontrado"
                    input_text = ''

                if button_rect_preorder.collidepoint(event.pos):
                    order_output = "Recorrido en Preorden: " + ' '.join(map(str, arbol.pre_order(arbol.get_root())))
                if button_rect_inorder.collidepoint(event.pos):
                    order_output = "Recorrido en Inorden: " + ' '.join(map(str, arbol.in_order(arbol.get_root())))
                if button_rect_postorder.collidepoint(event.pos):
                    order_output = "Recorrido en Postorden: " + ' '.join(map(str, arbol.post_order(arbol.get_root())))

            if event.type == KEYDOWN:
                if active:
                    if event.key == K_RETURN:
                        if input_text.isdigit():
                            arbol.add(int(input_text))
                        input_text = ''
                    elif event.key == K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        screen.fill((255, 255, 255))  # Fondo blanco
        pygame.draw.rect(screen, color, input_box, 2)
        text_surface = font.render(input_text, True, color)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        pygame.draw.rect(screen, (128, 128, 255), button_rect_insert)
        pygame.draw.rect(screen, (128, 128, 255), button_rect_remove)
        pygame.draw.rect(screen, (128, 128, 255), button_rect_preorder)
        pygame.draw.rect(screen, (128, 128, 255), button_rect_inorder)
        pygame.draw.rect(screen, (128, 128, 255), button_rect_postorder)
        pygame.draw.rect(screen, (128, 128, 255), button_rect_find)

        insert_text = font.render('Insertar', True, (0, 0, 0))
        remove_text = font.render('Eliminar', True, (0, 0, 0))
        preorder_text = font.render('Preorder', True, (0, 0, 0))
        inorder_text = font.render('Inorder', True, (0, 0, 0))
        postorder_text = font.render('Postorder', True, (0, 0, 0))
        find_text = font.render('Buscar', True, (0, 0, 0))

        screen.blit(insert_text, (button_rect_insert.x + 10, button_rect_insert.y + 5))
        screen.blit(remove_text, (button_rect_remove.x + 10, button_rect_remove.y + 5))
        screen.blit(preorder_text, (button_rect_preorder.x + 10, button_rect_preorder.y + 5))
        screen.blit(inorder_text, (button_rect_inorder.x + 10, button_rect_inorder.y + 5))
        screen.blit(postorder_text, (button_rect_postorder.x + 10, button_rect_postorder.y + 5))
        screen.blit(find_text, (button_rect_find.x + 10, button_rect_find.y + 5))

        draw_tree(arbol.get_root(), SCREEN_WIDTH // 2, 100, 150)
        output_lines = split_text(order_output, font, SCREEN_WIDTH - 40)
        for i, line in enumerate(output_lines):
            output_surface = font.render(line, True, (0, 0, 0))
            screen.blit(output_surface, (20, SCREEN_HEIGHT - 50 + i * 25))
        find_output_lines = split_text(find_output, font, SCREEN_WIDTH - 40)
        for i, line in enumerate(find_output_lines):
            output_surface = font.render(line, True, (0, 0, 0))
            screen.blit(output_surface, (20, SCREEN_HEIGHT - 150 + i * 25))

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()