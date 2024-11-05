import random
import numpy as np

def set_terrain(length, width, field_resolution, difficulty):
    """
    Rotating platforms and moving blocks course testing balancing and jumping abilities 
    with increased complexity as difficulty ramps up.
    """

    def m_to_idx(m):
        """Converts meters to quantized indices."""
        return np.round(m / field_resolution).astype(np.int16) if not (isinstance(m, list) or isinstance(m, tuple)) else [round(i / field_resolution) for i in m]

    height_field = np.zeros((m_to_idx(length), m_to_idx(width)))
    goals = np.zeros((8, 2))

    # Set up dimensions for rotating platforms and moving blocks
    platform_length = 1.0 - 0.3 * difficulty
    platform_length = m_to_idx(platform_length)
    platform_width = 1.0 - 0.2 * difficulty
    platform_width = m_to_idx(platform_width)
    block_size = 0.5 - 0.1 * difficulty
    block_size = m_to_idx(block_size)
    gap_length = 0.1 + 0.4 * difficulty
    gap_length = m_to_idx(gap_length)

    mid_y = m_to_idx(width) // 2

    def add_platform(start_x, end_x, mid_y):
        half_width = platform_width // 2
        x1, x2 = start_x, end_x
        y1, y2 = mid_y - half_width, mid_y + half_width
        platform_height = np.random.uniform(0.1, 0.2) * difficulty
        height_field[x1:x2, y1:y2] = platform_height

    def add_moving_block(start_x, end_x, mid_y):
        half_size = block_size // 2
        x1, x2 = start_x, end_x
        y1, y2 = mid_y - half_size, mid_y + half_size
        block_height = np.random.uniform(0.2, 0.3) * difficulty
        height_field[x1:x2, y1:y2] = block_height

    dx_min, dx_max = -0.1, 0.1
    dx_min, dx_max = m_to_idx(dx_min), m_to_idx(dx_max)
    dy_min, dy_max = -0.3, 0.3
    dy_min, dy_max = m_to_idx(dy_min), m_to_idx(dy_max)

    # Set spawn area to flat ground
    spawn_length = m_to_idx(2)
    height_field[0:spawn_length, :] = 0
    # Put first goal at spawn
    goals[0] = [spawn_length - m_to_idx(0.5), mid_y]  

    # Set remaining area to be a pit
    height_field[spawn_length:, :] = -1.0

    cur_x = spawn_length

    for i in range(3):  # Set up 3 rotating platforms
        dx = np.random.randint(dx_min, dx_max)
        dy = np.random.randint(dy_min, dy_max)
        add_platform(cur_x + dx, cur_x + platform_length + dx, mid_y + dy)

        # Put goal in the center of the platform
        goals[i+1] = [cur_x + (platform_length + dx) / 2, mid_y + dy]

        cur_x += platform_length + dx + gap_length

    for i in range(3):  # Set up 3 moving blocks
        dx = np.random.randint(dx_min, dx_max)
        dy = np.random.randint(dy_min, dy_max)
        
        add_moving_block(cur_x + dx, cur_x + block_size + dx, mid_y + dy)

        # Put goal in the center of the block
        goals[i + 4] = [cur_x + (block_size + dx) / 2, mid_y + dy]

        cur_x += block_size + dx + gap_length

    # Add final goal behind the last obstacle, fill in the remaining gap
    goals[-1] = [cur_x + m_to_idx(0.5), mid_y]
    height_field[cur_x:, :] = 0

    return height_field, goals