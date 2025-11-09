import numpy as np
import matplotlib.pyplot as plt
import noise


def perlin_field(width, height, scale=0.05, seed=0):
    field = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            field[y, x] = noise.pnoise2(x * scale, y * scale, base=seed)
    # Normalize to [0, 1]
    field = (field - field.min()) / (field.max() - field.min())
    return field

def gaussian_kernel(size=5, sigma=1.0):
    """Generate a normalized 2D Gaussian kernel."""
    ax = np.arange(-size // 2 + 1, size // 2 + 1)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    kernel /= np.sum(kernel)
    return kernel

def worley_noise(width=100, height=100, cell_size=3, num_values=8, seed=0):
    rng = np.random.default_rng(seed)

    # Determine grid of cells
    grid_x = width // cell_size + 2
    grid_y = height // cell_size + 2

    # Generate random feature points and assign integer values
    feature_points = {}
    for gx in range(grid_x):
        for gy in range(grid_y):
            fx = gx * cell_size + rng.random() * cell_size
            fy = gy * cell_size + rng.random() * cell_size
            val = rng.integers(1, num_values + 1)
            feature_points[(gx, gy)] = (fx, fy, val)

    # Prepare noise map
    noise_map = np.zeros((height, width), dtype=int)

    # Compute nearest feature point for each pixel
    for y in range(height):
        for x in range(width):
            gx, gy = int(x // cell_size), int(y // cell_size)
            min_dist = float('inf')
            value = 0

            # Check the surrounding cells for nearest feature point
            for nx in range(gx - 1, gx + 2):
                for ny in range(gy - 1, gy + 2):
                    if (nx, ny) in feature_points:
                        fx, fy, val = feature_points[(nx, ny)]
                        dist = (x - fx)**2 + (y - fy)**2
                        if dist < min_dist:
                            min_dist = dist
                            value = val

            noise_map[y, x] = value

    return noise_map

def gaussian_blur(image, sigma):
    """Apply Gaussian blur to a 2D array using convolution."""
    kernel = gaussian_kernel(5, sigma)
    h, w = image.shape
    kh, kw = kernel.shape
    pad_y, pad_x = kh // 2, kw // 2

    # Pad the image to handle edges
    padded = np.pad(image, ((pad_y, pad_y), (pad_x, pad_x)), mode='reflect')
    blurred = np.zeros_like(image, dtype=float)

    for y in range(h):
        for x in range(w):
            region = padded[y:y+kh, x:x+kw]
            blurred[y, x] = np.sum(region * kernel)

    return blurred

def add_static_noise(image, num_dots=50, num_values=8, seed=0):
    """
    Add small random dots to an integer image.

    Parameters:
        image : np.ndarray
            2D array of integers (1–num_values)
        num_dots : int
            Total number of random dots to add
        num_values : int
            Maximum integer value in the image
        seed : int
            RNG seed for reproducibility

    Returns:
        np.ndarray
            New image with random dots
    """
    rng = np.random.default_rng(seed)
    h, w = image.shape
    noisy_image = image.copy()
    
    for _ in range(num_dots):
        x = rng.integers(0, w)
        y = rng.integers(0, h)
        noisy_image[y, x] = rng.integers(1, num_values + 1)
    
    return noisy_image

# Generate and plot
width=100
height=100

worleyImage = worley_noise(width=width, height=height)

blur0 = worleyImage  # original (no blur)
blur1 = gaussian_blur(worleyImage, sigma=0.1)
blur2 = gaussian_blur(worleyImage, sigma=1.0)
blur3 = gaussian_blur(worleyImage, sigma=1.5)

noise_map = perlin_field(width, height, scale=0.1)
# Normalize to [0, 1]
noise_map = (noise_map - noise_map.min()) / (noise_map.max() - noise_map.min())

# Map Perlin noise to [0, 1]
n = noise_map

composite = np.zeros_like(worleyImage, dtype=float)

# Region 1: between blur1 and blur2
mask1 = n < 0.5
t1 = n / 0.5  # remap 0→0.5 to 0→1
composite[mask1] = (1 - t1[mask1]) * blur1[mask1] + t1[mask1] * blur2[mask1]

# Region 2: between blur2 and blur3
mask2 = n >= 0.5
t2 = (n[mask2] - 0.5) / 0.5  # remap 0.5→1 to 0→1
composite[mask2] = (1 - t2) * blur2[mask2] + t2 * blur3[mask2]

noised = add_static_noise(composite, num_dots=5000)

quantized = np.rint(noised)  # round to nearest integer
final_image = np.clip(quantized, 1, 8).astype(int)

plt.imshow(final_image, cmap='tab10', interpolation='nearest')
plt.title("Funny Noise (8 integer groups)")
plt.colorbar()
plt.show()

# Suppose `final_image` is your 2D integer array
filename = "noiseSubmition.txt"

# Lines you want to prepend
header_lines = [
    "{} {}".format(final_image.shape[1], final_image.shape[0])
]

# Open file and write header + array
with open(filename, "w") as f:
    for line in header_lines:
        f.write(line + "\n")
    
    # Now write the array, one row per line
    for row in final_image:
        # Convert row to space-separated integers
        f.write(" ".join(map(str, row)) + "\n")
