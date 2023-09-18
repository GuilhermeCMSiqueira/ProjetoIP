class Projetil:
    tamanho_projetil = 10
    velocidade_projetil = 5
    cor_projetil = verde

    def __init__(self, x, y, direcao_x, direcao_y):
        self.x = x
        self.y = y
        self.direcao_x = direcao_x
        self.direcao_y = direcao_y

    def mover(self):
        self.x += self.direcao_x * self.velocidade_projetil
        self.y += self.direcao_y * self.velocidade_projetil

    def desenhar(self):
        pygame.draw.rect(tela, self.cor_projetil, (self.x - self.tamanho_projetil // 2, self.y, self.tamanho_projetil, self.tamanho_projetil))
