# Inisialisasi Pygame
import pygame

# Memanggil font dan mixer(untuk sound)
pygame.font.init()
pygame.mixer.init()

# Membuat screen dengan menentukan lebar dan tinggi. Didefinisikan sesuai dengan variable di bawah.
# WIDTH untuk lebar screen, HEIGHT untuk tinggi screen, dan SCR untuk window screen
WIDTH, HEIGHT = 800, 600 # lebar dan tinggi screen
SCR = pygame.display.set_mode((WIDTH, HEIGHT)) # mendifinisikan dan membuat variabel screen
pygame.display.set_caption("Covid-19 Battle!") # mengganti judul game

# Mengubah icon untuk game COVID-19 Battle!
# Image icon diunduh dari flaticon.com
ICON = pygame.image.load('icon.png') # mengganti icon game
pygame.display.set_icon(ICON)

# Membuat variabel warna-warna yang akan digunakan
# Warna putih untuk background, warna hitam untuk font, warna bright_navy_blue untuk peluru virus, warna bittersweet untuk peluru antibody
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHT_NAVY_BLUE = (21, 131, 209)
BITTERSWEET = (249, 110, 90)

# Membuat batas antara player 1 dan player 2 menggunakan .Rect() function karena berbentuk persegi panjang di tengah dengan ketebalan 10.
BATAS = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Membuat variabel sound untuk fire(ketika menembakkan bullet) dan hit(ketika terkena tembakan) 
HIT_SOUND = pygame.mixer.Sound('Explosion.mp3')
FIRE_SOUND = pygame.mixer.Sound('Bullet.mp3')

# Membuat variabel font untuk keterangan nyawa/health dan pemenang battle
HEALTH_FONT = pygame.font.SysFont('comicsansms', 30) # font comicsansms dengan ukuran 30
WINNER_FONT = pygame.font.SysFont('comicsansms', 100) # font comicsansms dengan ukuran 100

# Membuat variabel waktu looping, kecepatan player, kecepatan peluru, jumlah peluru maksimal dan dimensi player
FPS = 60 # frame per second (60x/detik)
VEL = 5 # velocity/kecepatan player
BULLET_VEL = 7 # kecepatan bullet
MAX_BULLETS = 3 # maximum bullet
CHAR_WIDTH, CHAR_HEIGHT = 64, 64 # dimensi player diunduh dari flaticon.com dengan 64x64 pixels

# Membuat variabel ketika terkena tembakan
VIRUS_HIT = pygame.USEREVENT + 1 # -->
ANTIBODY_HIT = pygame.USEREVENT + 2 # -->

# Menambahkan image player 1, player 2, dan background image
# Image player diunduh dari flaticon.com dan image background diunduh dari freepik.com
VIRUS = pygame.image.load('virus.png')
ANTIBODY = pygame.image.load('antibody.png')
SCREEN = pygame.image.load('screen.png')

# Mengatur font dan warna untuk setiap variabel yang membutuhkan font dan warna
def draw_window(antibody, virus, antibody_bullets, virus_bullets, antibody_health, virus_health):
    SCR.blit(SCREEN, (0, 0)) # menampilkan screen
    pygame.draw.rect(SCR, WHITE, BATAS) # memanggil warna screen putih

    antibody_health_text = HEALTH_FONT.render("Health: " + str(antibody_health), 1, BLACK) # membuat variable text health untuk antibody
    virus_health_text = HEALTH_FONT.render("Health: " + str(virus_health), 1, BLACK) # membuat variable text health untuk virus
    SCR.blit(antibody_health_text, (WIDTH - antibody_health_text.get_width() - 10, 10)) # menampilkan text health untuk antibody
    SCR.blit(virus_health_text, (10, 10)) # menampilkan text health untuk virus

    SCR.blit(VIRUS, (virus.x, virus.y)) # mengatur posisi text health untuk virus
    SCR.blit(ANTIBODY, (antibody.x, antibody.y)) # mengatur posisi text health untuk antibody

    for bullet in antibody_bullets:
        pygame.draw.rect(SCR, BRIGHT_NAVY_BLUE, bullet) # mengatur warna dan dimensi bullets untuk antibody

    for bullet in virus_bullets:
        pygame.draw.rect(SCR, BITTERSWEET, bullet) # mengatur warna dan dimensi bullets untuk virus

    pygame.display.update() # update untuk mengeluarkan warna

# Menentukan cara mengoperasikan dan pergerakan players. 
# Operasi game ini menggunakan keyboard dengan player 1 di sebelah kiri, player 2 di sebelah kanan sebagai berikut:

# Menentukan cara mengoperasikan dan pergerakan player 1
# Tombol yang dipakai pada player 1 adalah a, d, w, s
def virus_handle_movement(keys_pressed, virus):
    if keys_pressed[pygame.K_a] and virus.x - VEL > 0:  # LEFT
        virus.x -= VEL # jika tombol a ditekan, maka koordinat x dari virus berkurang sesuai dengan VEL/kecepatan tombol
        # di sini maksudnya adalah sesuai dengan seberapa lama tombol ditekan dan kemudian dilepas, berlaku seterusnya
    if keys_pressed[pygame.K_d] and virus.x + VEL + virus.width < BATAS.x:  # RIGHT
        virus.x += VEL # koordinat x ditambah VEL karena ke kanan
    if keys_pressed[pygame.K_w] and virus.y - VEL > 0:  # UP
        virus.y -= VEL # koordinat y dikurang VEL karena ke atas
    if keys_pressed[pygame.K_s] and virus.y + VEL + virus.height < HEIGHT - 15:  # DOWN
        virus.y += VEL # koordinat y ditambah VEL karena ke bawah

# # Menentukan cara mengoperasikan dan pergerakan player 2
# Tombol yang dipakai pada player 1 adalah left, right, up, down
def antibody_handle_movement(keys_pressed, antibody):
    if keys_pressed[pygame.K_LEFT] and antibody.x - VEL > BATAS.x + BATAS.width:  # LEFT
        antibody.x -= VEL # --> prinsip sama dengan player 1, hanya berbeda letak, dan dihitung dari batas tengah
    if keys_pressed[pygame.K_RIGHT] and antibody.x + VEL + antibody.width < WIDTH:  # RIGHT
        antibody.x += VEL # --> dihitung berdasarkan lebar screen
    if keys_pressed[pygame.K_UP] and antibody.y - VEL > 0:  # UP
        antibody.y -= VEL # --> # --> dihitung dari bawah (0)
    if keys_pressed[pygame.K_DOWN] and antibody.y + VEL + antibody.height < HEIGHT - 15:  # DOWN
        antibody.y += VEL # --> dihitung dari atas (tinggi screen)

# Menentukan cara mengoperasikan, pergerakan peluru, dan collission pada masing-masing player
def handle_bullets(virus_bullets, antibody_bullets, virus, antibody):
    # Mengatur pergerakan bullet yang berasal dari virus
    for bullet in virus_bullets:
        bullet.x += BULLET_VEL # Posisi bullet akan mengikuti BULLET_VEL/kecepatan yang sudah didefinisikan di atas
        if antibody.colliderect(bullet): # fungsi .colliderect() untuk ketika terkena tembakan/hit memanggil event ANTIBODY_HIT
            pygame.event.post(pygame.event.Event(ANTIBODY_HIT))
            virus_bullets.remove(bullet) # setelah terkena di badan antibody, bullet hilang
        elif bullet.x > WIDTH: # Jika bullet tidak terkena badan antibody, maka dy akan hilang jika sudah sampai batas WIDTH/lebar layar
            virus_bullets.remove(bullet) 

    # Mengatur pergerakan bullet yang berasal dari antibody. prinsip sama dengan bullet yang berasal dari virus
    for bullet in antibody_bullets:
        bullet.x -= BULLET_VEL
        if virus.colliderect(bullet): # fungsi .colliderect() untuk ketika terkena tembakan/hit memanggil event VIRUS_HIT
            pygame.event.post(pygame.event.Event(VIRUS_HIT)) 
            antibody_bullets.remove(bullet)
        elif bullet.x < 0: # Jika bullet tidak terkena badan antibody, maka dy akan hilang jika sudah sampai batas layar sebelah kiri: 0
            antibody_bullets.remove(bullet)

# Membuat display pemenang battle
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, BLACK) # --> Text pemenang dirender dari variable WINNER_FONT dengan warna hitam
    SCR.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2)) # Pengaturan text di tengah
    pygame.display.update() # --> we have to update to update pygame to display our image and colors
    pygame.time.delay(5000) # --> time delay dalam menampilkan pemenang

# Game loop
def main():
    antibody = pygame.Rect(630, 300, CHAR_WIDTH, CHAR_HEIGHT) # --> posisi dan dimensi antibody di layar 
    virus = pygame.Rect(100, 300, CHAR_WIDTH, CHAR_HEIGHT) # --> posisi dan dimensi virus di layar 

    antibody_bullets = []
    virus_bullets = []

    antibody_health = 20 # --> jumlah health pada antibody
    virus_health = 20 # --> jumlah health pada antibody

    clock = pygame.time.Clock() # memanggil clock
    # run game loop
    running = True
    while running:
        clock.tick(FPS) # menentukan fps per loop
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Menentukan kapan game selesai
                running = False
                pygame.quit()

            # Memanggil sound setiap kali bullets ditembakkan dari player 1 (virus)
            if event.type == pygame.KEYDOWN: 
                # Untuk virus, bullet keluar ketika ditekan tombol Ctrl sebelah kiri
                if event.key == pygame.K_LCTRL and len(virus_bullets) < MAX_BULLETS: 
                    bullet = pygame.Rect(virus.x + virus.width, virus.y + virus.height//2 - 2, 10, 5) # dimensi bullet
                    virus_bullets.append(bullet)
                    FIRE_SOUND.play()

                # Memanggil sound setiap kali bullets ditembakkan dari player 2 (antibody)
                # Untuk virus, bullet keluar ketika ditekan tombol Ctrl sebelah kanan
                if event.key == pygame.K_RCTRL and len(antibody_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(antibody.x, antibody.y + antibody.height//2 - 2, 10, 5) # dimensi bullet
                    antibody_bullets.append(bullet)
                    FIRE_SOUND.play()

            if event.type == ANTIBODY_HIT: # memanggil sound setiap kali antibody terkena tembakan
                antibody_health -= 1
                HIT_SOUND.play()

            if event.type == VIRUS_HIT: # memanggil sound setiap kali virus terkena tembakan
                virus_health -= 1
                HIT_SOUND.play()

        # menampilkan pemenang
        winner_text = ""
        # Jika health pada antibody sudah 0, maka tampilkan Virus Wins!
        if antibody_health <= 0:
            winner_text = "Virus Wins!"

        # Jika health pada virus sudah 0, maka tampilkan Antibody Wins!
        if virus_health <= 0:
            winner_text = "Antibody Wins!"

        if winner_text != "": # menampilkan text winner
            draw_winner(winner_text)
            break # SELESAI

        keys_pressed = pygame.key.get_pressed()
        virus_handle_movement(keys_pressed, virus) # Memanggil operasi dan pergerakan virus ke dalam loop
        antibody_handle_movement(keys_pressed, antibody) # Memanggil operasi dan pergerakan antibody ke dalam loop

        handle_bullets(virus_bullets, antibody_bullets, virus, antibody) # Memanggil operasi dan pergerakan peluru ke dalam loop

        # agar window selalu aktif selama looping
        draw_window(antibody, virus, antibody_bullets, virus_bullets, antibody_health, virus_health) 

    main()


if __name__ == "__main__": # --> untuk memanggil hanya specific file name tersebut
    main()