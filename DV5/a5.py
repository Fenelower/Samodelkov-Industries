import open3d as o3d
import numpy as np
import copy

# ================= НАСТРОЙКИ =================
# путь к твоей 3D-модели (.ply / .obj / .stl / .off)
MODEL_PATH = "heatmap_model_from_generated_png.ply"
# пример абсолютного пути:
# MODEL_PATH = r"C:\Users\Пользователь\Desktop\DV5\heatmap_model_from_generated_png.ply"

VOXEL_SIZE = 0.05      # размер вокселя для шага 4
POISSON_DEPTH = 8      # глубина Poisson-реконструкции
GRADIENT_AXIS = "z"    # ось для экстремумов: 'x', 'y' или 'z'
# ==================================================


def print_mesh_info(name: str, mesh: o3d.geometry.TriangleMesh):
    vertices = np.asarray(mesh.vertices)
    triangles = np.asarray(mesh.triangles)

    print(f"\n=== {name} ===")
    print(f"Количество вершин:        {len(vertices)}")
    print(f"Количество треугольников: {len(triangles)}")
    print(f"Цвет есть:                {mesh.has_vertex_colors()}")
    print(f"Нормали есть:             {mesh.has_vertex_normals()}")


def print_pcd_info(name: str, pcd: o3d.geometry.PointCloud):
    points = np.asarray(pcd.points)

    print(f"\n=== {name} ===")
    print(f"Количество вершин (точек): {len(points)}")
    print(f"Цвет есть:                  {pcd.has_colors()}")
    print(f"Нормали есть:               {pcd.has_normals()}")


def print_voxel_info(name: str, voxel_grid: o3d.geometry.VoxelGrid):
    voxels = voxel_grid.get_voxels()
    print(f"\n=== {name} ===")
    print(f"Количество вокселей: {len(voxels)}")
    has_color = hasattr(voxel_grid, "colors") and len(voxel_grid.colors) > 0
    print(f"Цвет есть:            {has_color}")


def clip_mesh_with_plane(mesh: o3d.geometry.TriangleMesh,
                         point_on_plane: np.ndarray,
                         plane_normal: np.ndarray) -> o3d.geometry.TriangleMesh:
    """
    Удаляем все вершины/треугольники, которые лежат "по правую сторону"
    от плоскости (там, где (p - point_on_plane)·n > 0).
    """
    plane_normal = plane_normal / np.linalg.norm(plane_normal)

    v = np.asarray(mesh.vertices)
    t = np.asarray(mesh.triangles)

    signed_dist = (v - point_on_plane) @ plane_normal
    keep_mask_v = signed_dist <= 0.0
    keep_idx = np.where(keep_mask_v)[0]

    index_map = -np.ones(len(v), dtype=int)
    index_map[keep_idx] = np.arange(len(keep_idx))

    keep_mask_t = keep_mask_v[t].all(axis=1)
    t_kept = t[keep_mask_t]
    t_new = index_map[t_kept]

    new_mesh = o3d.geometry.TriangleMesh()
    new_mesh.vertices = o3d.utility.Vector3dVector(v[keep_idx])
    new_mesh.triangles = o3d.utility.Vector3iVector(t_new)

    if mesh.has_vertex_colors():
        vc = np.asarray(mesh.vertex_colors)[keep_idx]
        new_mesh.vertex_colors = o3d.utility.Vector3dVector(vc)
    if mesh.has_vertex_normals():
        vn = np.asarray(mesh.vertex_normals)[keep_idx]
        new_mesh.vertex_normals = o3d.utility.Vector3dVector(vn)

    new_mesh.compute_triangle_normals()
    return new_mesh


def create_wireframe_cube(center, size, color=[1, 0, 0]):
    """Создаёт wireframe-куб вокруг точки."""
    cx, cy, cz = center
    s = size / 2.0

    vertices = np.array([
        [cx - s, cy - s, cz - s],
        [cx + s, cy - s, cz - s],
        [cx + s, cy + s, cz - s],
        [cx - s, cy + s, cz - s],
        [cx - s, cy - s, cz + s],
        [cx + s, cy - s, cz + s],
        [cx + s, cy + s, cz + s],
        [cx - s, cy + s, cz + s],
    ])

    lines = np.array([
        [0, 1], [1, 2], [2, 3], [3, 0],   # нижний квадрат
        [4, 5], [5, 6], [6, 7], [7, 4],   # верхний квадрат
        [0, 4], [1, 5], [2, 6], [3, 7],   # вертикальные рёбра
    ])

    colors = np.tile(np.array(color), (lines.shape[0], 1))

    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(vertices)
    line_set.lines = o3d.utility.Vector2iVector(lines)
    line_set.colors = o3d.utility.Vector3dVector(colors)
    return line_set


def main():
    # ===================== 1. ЗАГРУЗКА И ВИЗУАЛИЗАЦИЯ =====================
    print("Шаг 1: Загрузка исходной 3D-модели")
    mesh = o3d.io.read_triangle_mesh(MODEL_PATH)

    if len(mesh.vertices) == 0:
        print("ВНИМАНИЕ: mesh пустой. Проверь MODEL_PATH!")
    if not mesh.has_vertex_normals():
        mesh.compute_vertex_normals()

    print_mesh_info("Исходный mesh", mesh)
    o3d.visualization.draw_geometries([mesh],
                                      window_name="1. Original Mesh")

    # ===================== 2. POINT CLOUD =====================
    print("\nШаг 2: Преобразование в облако точек")

    pcd = o3d.io.read_point_cloud(MODEL_PATH)
    if len(pcd.points) == 0:
        print("Файл не point cloud -> семплим точки с поверхности mesh.")
        pcd = mesh.sample_points_poisson_disk(number_of_points=40000)

    if not pcd.has_normals():
        pcd.estimate_normals()

    print_pcd_info("Облако точек", pcd)
    o3d.visualization.draw_geometries([pcd],
                                      window_name="2. Point Cloud")

    # ===================== 3. POISSON RECONSTRUCTION =====================
    print("\nШаг 3: Реконструкция поверхности из облака точек (Poisson)")

    pcd.estimate_normals()
    poisson_mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=POISSON_DEPTH
    )

    bbox = pcd.get_axis_aligned_bounding_box()
    poisson_mesh_crop = poisson_mesh.crop(bbox)

    if not poisson_mesh_crop.has_vertex_normals():
        poisson_mesh_crop.compute_vertex_normals()

    print_mesh_info("Реконструированный mesh (после crop)", poisson_mesh_crop)
    o3d.visualization.draw_geometries([poisson_mesh_crop],
                                      window_name="3. Reconstructed Mesh (Poisson)")

    # ===================== 4. ВОКСЕЛИЗАЦИЯ =====================
    print("\nШаг 4: Вокселизация облака точек")

    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(
        pcd, voxel_size=VOXEL_SIZE
    )

    print_voxel_info("Воксельная модель", voxel_grid)
    o3d.visualization.draw_geometries([voxel_grid],
                                      window_name="4. Voxelized Model")

    # ===================== 5. ПЛОСКОСТЬ + МЕШ =====================
    print("\nШаг 5: Добавление плоскости в сцену")

    bbox = poisson_mesh_crop.get_axis_aligned_bounding_box()
    center = bbox.get_center()
    extent = bbox.get_extent()
    size = max(extent)

    plane = o3d.geometry.TriangleMesh.create_box(
        width=2.0 * size,
        height=2.0 * size,
        depth=0.02 * size
    )
    plane.paint_uniform_color([0.3, 0.3, 0.3])

    plane_vertices = np.asarray(plane.vertices)
    plane_center = plane_vertices.mean(axis=0)

    plane.translate(center - plane_center - np.array([0.0, 0.0, 0.3 * size]))

    R = plane.get_rotation_matrix_from_xyz(
        (np.deg2rad(35.0), 0.0, np.deg2rad(-15.0))
    )
    plane.rotate(R, center=center)

    print_mesh_info("Плоскость (plane)", plane)
    o3d.visualization.draw_geometries([poisson_mesh_crop, plane],
                                      window_name="5. Plane + Original Mesh")

    # ===================== 6. КЛИППИНГ =====================
    print("\nШаг 6: Обрезка модели (клиппинг)")

    point_on_plane = center
    plane_normal = np.array([1.0, 0.0, 0.0])  # нормаль вдоль +X

    clipped_mesh = clip_mesh_with_plane(poisson_mesh_crop,
                                        point_on_plane,
                                        plane_normal)

    print_mesh_info("Mesh после обрезки (клиппинга)", clipped_mesh)
    o3d.visualization.draw_geometries([clipped_mesh],
                                      window_name="6. Clipped Mesh")

    # ===================== 7. ГРАДИЕНТ + ЭКСТРЕМУМЫ (КУБЫ) =================
    print("\nШаг 7: Градиент цвета и поиск экстремумов")

    pcd_for_step7 = poisson_mesh_crop.sample_points_poisson_disk(8000)
    pcd_for_step7.estimate_normals()
    pcd_for_step7.orient_normals_consistent_tangent_plane(30)

    pcd_grad = copy.deepcopy(pcd_for_step7)
    points = np.asarray(pcd_grad.points)

    axis_map = {"x": 0, "y": 1, "z": 2}
    axis_idx = axis_map[GRADIENT_AXIS.lower()]

    coord = points[:, axis_idx]
    c_min, c_max = coord.min(), coord.max()
    norm_coord = (coord - c_min) / (c_max - c_min + 1e-9)

    # градиент: синий → фиолетовый/розовый (как на скрине)
    colors = np.zeros((len(points), 3))
    colors[:, 2] = 1.0                 # базовый синий
    colors[:, 0] = norm_coord * 0.8    # добавляем красный
    pcd_grad.colors = o3d.utility.Vector3dVector(colors)

    idx_min = np.argmin(coord)
    idx_max = np.argmax(coord)
    p_min = points[idx_min]
    p_max = points[idx_max]

    print("\nКоординаты экстремумов по оси", GRADIENT_AXIS.upper())
    print("Минимум:", p_min)
    print("Максимум:", p_max)

    cube_size = 0.15 * size
    cube_min = create_wireframe_cube(p_min, cube_size, color=[1, 0, 0])
    cube_max = create_wireframe_cube(p_max, cube_size, color=[1, 0, 0])

    o3d.visualization.draw_geometries(
        [pcd_grad, cube_min, cube_max],
        window_name="7. 3D Model with Z-Extremes and Axes"
    )

    print("\nВсе 7 шагов выполнены.")


if __name__ == "__main__":
    main()
