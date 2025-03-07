import math
from typing import List, Tuple
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def calculate_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """İki nokta arasındaki Öklid mesafesini hesaplar."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def closest_pair_divide_and_conquer(points: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], Tuple[float, float], float]:
    """Divide and Conquer ile en yakın çifti bulur."""
    def closest_in_strip(strip: List[Tuple[float, float]], d: float) -> Tuple[Tuple[float, float], Tuple[float, float], float]:
        """Orta bölgede en yakın çifti bulur."""
        min_dist = d
        closest_pair = None
        strip.sort(key=lambda p: p[1])  # Y eksenine göre sıralama
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if (strip[j][1] - strip[i][1]) >= min_dist:
                    break
                dist = calculate_distance(strip[i], strip[j])
                if dist < min_dist:
                    min_dist = dist
                    closest_pair = (strip[i], strip[j])
        return closest_pair[0], closest_pair[1], min_dist

    def closest_pair_recursive(points_sorted: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], Tuple[float, float], float]:
        """Rekürsif olarak en yakın çifti bulur."""
        n = len(points_sorted)
        if n <= 3:
            min_dist = float('inf')
            closest_pair = None
            for i in range(n):
                for j in range(i + 1, n):
                    dist = calculate_distance(points_sorted[i], points_sorted[j])
                    if dist < min_dist:
                        min_dist = dist
                        closest_pair = (points_sorted[i], points_sorted[j])
            return closest_pair[0], closest_pair[1], min_dist

        mid = n // 2
        mid_point = points_sorted[mid]

        left_closest = closest_pair_recursive(points_sorted[:mid])
        right_closest = closest_pair_recursive(points_sorted[mid:])
        min_pair = left_closest if left_closest[2] < right_closest[2] else right_closest

        strip = [p for p in points_sorted if abs(p[0] - mid_point[0]) < min_pair[2]]
        strip_closest = closest_in_strip(strip, min_pair[2])

        return min_pair if min_pair[2] < strip_closest[2] else strip_closest

    points_sorted = sorted(points, key=lambda p: p[0])
    return closest_pair_recursive(points_sorted)

def visualize_with_divide_and_conquer(points: List[Tuple[float, float]]):
    """Divide and Conquer algoritmasını animasyonla görselleştirir."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(*zip(*points), s=50, color='blue', label='Points')
    ax.legend()
    ax.set_title("Closest Pair (Divide and Conquer) Animation")

    # Çizgi ve metin elemanları
    line, = ax.plot([], [], 'r-', lw=2, label='Current Pair')
    closest_line, = ax.plot([], [], 'g--', lw=2, label='Closest Pair')
    text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

    # Divide and Conquer algoritmasını çalıştır
    closest_pair_result = []

    def divide_and_conquer_step(points_sorted: List[Tuple[float, float]], depth=0):
        """Divide and Conquer adımları için bir jeneratör."""
        n = len(points_sorted)
        if n <= 3:
            for i in range(n):
                for j in range(i + 1, n):
                    dist = calculate_distance(points_sorted[i], points_sorted[j])
                    yield (points_sorted[i], points_sorted[j], dist)
            return

        mid = n // 2
        mid_point = points_sorted[mid]

        left_generator = divide_and_conquer_step(points_sorted[:mid], depth + 1)
        right_generator = divide_and_conquer_step(points_sorted[mid:], depth + 1)

        # Sol ve sağ bölgenin sonuçlarını döndür
        for pair in left_generator:
            yield pair
        for pair in right_generator:
            yield pair

        # Orta bölgede kontrol yap
        strip = [p for p in points_sorted if abs(p[0] - mid_point[0]) < float('inf')]
        strip.sort(key=lambda p: p[1])
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if (strip[j][1] - strip[i][1]) >= float('inf'):
                    break
                dist = calculate_distance(strip[i], strip[j])
                yield (strip[i], strip[j], dist)

    points_sorted = sorted(points, key=lambda p: p[0])
    pairs = list(divide_and_conquer_step(points_sorted))

    def update(frame):
        """Her adımda iki noktayı ve mesafeyi gösterir."""
        nonlocal closest_pair_result
        p1, p2, dist = pairs[frame]

        # Geçerli çift için kırmızı çizgiyi güncelle
        line.set_data([p1[0], p2[0]], [p1[1], p2[1]])

        # En kısa mesafeyi kontrol et ve güncelle
        if not closest_pair_result or dist < closest_pair_result[2]:
            closest_pair_result = (p1, p2, dist)
            closest_line.set_data([p1[0], p2[0]], [p1[1], p2[1]])

        # Mesafeyi metin olarak yazdır
        text.set_text(f"Distance: {dist:.6f} | Closest: {closest_pair_result[2]:.6f}")
        return line, closest_line, text

    ani = FuncAnimation(
        fig,
        update,
        frames=len(pairs),  # Toplam çerçeve sayısı
        interval=100,      # Geçiş süresi (ms cinsinden)
        blit=True           # Blit özelliği
    )

    plt.show()

def main():
    filename = "points_.txt"  # Nokta dosyası
    points = read_points_from_file(filename)

    if not points:
        print("Error: No points loaded from file.")
        return

    visualize_with_divide_and_conquer(points)

def read_points_from_file(filename: str) -> List[Tuple[float, float]]:
    """Dosyadan noktaları okur. 111111111111111"""
    points = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                x, y = map(float, line.strip().split())
                points.append((x, y))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    return points

if __name__ == "__main__":
    main()
