import sys
import pygame
from bullet import Bullet
from alien import Alien


def check_events(ai_settings, screen, ship, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """
    键盘按下事件
    :param bullets:
    :param screen:
    :param ai_settings:
    :param event:
    :param ship:
    """
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """
    键盘抬起事件
    :param event:
    :param ship:
    """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, ship, aliens, bullets):
    """更新屏幕上的图像，并切换到新屏幕上"""
    screen.fill(ai_settings.bg_color)

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()

    aliens.draw(screen)

    # 让最近的屏幕可见
    pygame.display.flip()


def update_bullets(aliens, bullets):
    """
    更新子弹的位置， 并删除已消失的子弹
    :param aliens:
    :param bullets:
    """
    # 更新子弹的位置
    bullets.update()
    # 删除以消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # 检查是否有子弹击中了外星人
    # 如果击中，删除相对应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)


def fire_bullet(ai_settings, screen, ship, bullets):
    """
    如果没有达到子弹限制，发射子弹
    :param ai_settings:
    :param screen:
    :param ship:
    :param bullets:
    """
    # 创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, aliens_width):
    """
    计算每行可容纳多少外星人
    :param ai_settings:
    :param aliens_width:
    """
    available_space_x = ai_settings.screen_width - 2 * aliens_width
    number_aliens_x = int(available_space_x / (2 * aliens_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """
    创建外星人，并将其放在当前行
    :param ai_settings:
    :param screen:
    :param aliens:
    :param alien_number:
    """
    alien = Alien(ai_settings, screen)
    aliens_width = alien.rect.width
    alien.x = aliens_width + 2 * aliens_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """
    创建外星人群
    :param ship:
    :param ai_settings:
    :param screen:
    :param aliens:
    """
    alien = Alien(ai_settings, screen)
    aliens_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, aliens_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 创建一个外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_rows(ai_settings, ship_height, alien_height):
    """
    计算屏幕可容纳多少行外星人
    :param ai_settings:
    :param ship_height:
    :param alien_height:
    """
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)


def update_aliens(ai_settings, aliens):
    """
    检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    :param ai_settings:
    :param aliens:
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()


def change_fleet_direction(ai_settings, aliens):
    """
    将整群外星人下移，并改变他们的方向
    :param ai_settings:
    :param aliens:
    """
    for alien in aliens:
        alien.rect.y += ai_settings.alien_drop_speed
    ai_settings.fleet_direction *= -1
