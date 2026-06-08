"""Wind streak overlay — Đã vô hiệu hóa hoàn toàn logic hạt gió"""

PARTICLES_SCRIPT = r"""
(function () {
  // Tạo stub object để tránh lỗi gọi hàm từ NiceGUI client
  window.weatherMapParticles = {
    init() {},
    apply(opts) {},
    onMapMove() {}
  };
})();
"""