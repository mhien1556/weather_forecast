"""Wind streak overlay — mỏng, nhẹ, chỉ dùng ở lớp tốc độ gió."""

PARTICLES_SCRIPT = r"""
(function () {
  if (window.weatherMapParticles) return;

  const WIND = {
    count: 650,
    speed: 2.0,
    line: 0.65,
    trail: 7,
    rgb: '255,255,255',
    alpha: 0.55,
    swirl: 0.9,
  };

  function findLeafletMap(canvas) {
    if (window.__niceguiLeafletMap) return window.__niceguiLeafletMap;
    const root = canvas?.closest('.map-stage')?.querySelector('.leaflet-container');
    if (!root) return null;
    for (const k of Object.keys(root)) {
      const v = root[k];
      if (v?.latLngToContainerPoint && v?.getBounds) {
        window.__niceguiLeafletMap = v;
        return v;
      }
    }
    return null;
  }

  class WindStreaks {
    constructor(canvas) {
      this.canvas = canvas;
      this.ctx = canvas.getContext('2d', { alpha: true });
      this.particles = [];
      this.enabled = false;
      this.windDeg = 180;
      this.frame = 0;
      this.map = null;
      this._resize = this._resize.bind(this);
      window.addEventListener('resize', this._resize);
      this._resize();
      this._seed();
      this._loop = this._loop.bind(this);
      requestAnimationFrame(this._loop);
    }

    _resize() {
      if (!this.map) this.map = findLeafletMap(this.canvas);
      const stage = this.canvas.closest('.map-stage');
      const rect = (stage || this.canvas).getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      this.canvas.width = Math.max(1, Math.floor(rect.width * dpr));
      this.canvas.height = Math.max(1, Math.floor(rect.height * dpr));
      this.canvas.style.width = rect.width + 'px';
      this.canvas.style.height = rect.height + 'px';
      this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      this.w = rect.width;
      this.h = rect.height;
    }

    _angle(x, y) {
      const base = (this.windDeg * Math.PI) / 180;
      const nx = (x / this.w) * 6.28;
      const ny = (y / this.h) * 6.28;
      const t = this.frame * 0.003;
      return base
        + Math.sin(nx * 1.6 + t) * WIND.swirl
        + Math.cos(ny * 1.9 - t) * WIND.swirl * 0.65;
    }

    _spawn(bounds) {
      if (bounds && this.map) {
        return {
          lat: bounds.getSouth() + Math.random() * (bounds.getNorth() - bounds.getSouth()),
          lon: bounds.getWest() + Math.random() * (bounds.getEast() - bounds.getWest()),
          trail: [],
          geo: true,
          life: 0,
        };
      }
      const x = Math.random() * this.w;
      const y = Math.random() * this.h;
      return { x, y, trail: [{ x, y }], geo: false, life: 0 };
    }

    _seed() {
      if (!this.map) this.map = findLeafletMap(this.canvas);
      const bounds = this.map?.getBounds() || null;
      this.particles = Array.from({ length: WIND.count }, () => this._spawn(bounds));
    }

    onMapMove() {
      if (!this.map) this.map = findLeafletMap(this.canvas);
      this._seed();
    }

    apply(opts) {
      if (typeof opts.enabled === 'boolean') this.enabled = opts.enabled;
      if (typeof opts.windDeg === 'number') this.windDeg = opts.windDeg;
      if (!this.enabled) {
        this.ctx.clearRect(0, 0, this.w, this.h);
        return;
      }
      if (!this.map) this.map = findLeafletMap(this.canvas);
      this._seed();
    }

    _drawStreak(trail) {
      const n = trail.length;
      if (n < 2) return;
      const ctx = this.ctx;
      const tail = trail[0];
      const head = trail[n - 1];
      const grad = ctx.createLinearGradient(tail.x, tail.y, head.x, head.y);
      grad.addColorStop(0, `rgba(${WIND.rgb},0)`);
      grad.addColorStop(0.55, `rgba(${WIND.rgb},${WIND.alpha * 0.35})`);
      grad.addColorStop(1, `rgba(${WIND.rgb},${WIND.alpha})`);
      ctx.beginPath();
      ctx.strokeStyle = grad;
      ctx.lineWidth = WIND.line;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.moveTo(trail[0].x, trail[0].y);
      for (let i = 1; i < n; i++) ctx.lineTo(trail[i].x, trail[i].y);
      ctx.stroke();
    }

    _step(p) {
      if (p.geo && this.map) {
        const pt = this.map.latLngToContainerPoint([p.lat, p.lon]);
        const a = this._angle(pt.x, pt.y);
        const m = WIND.speed * 0.00012;
        p.lat += Math.cos(a) * m;
        p.lon += Math.sin(a) * m / Math.max(0.35, Math.cos((p.lat * Math.PI) / 180));
        const pt2 = this.map.latLngToContainerPoint([p.lat, p.lon]);
        p.trail.push({ x: pt2.x, y: pt2.y });
      } else {
        const a = this._angle(p.x, p.y);
        const m = WIND.speed * 0.75;
        p.x += Math.sin(a) * m;
        p.y -= Math.cos(a) * m;
        p.trail.push({ x: p.x, y: p.y });
      }
      while (p.trail.length > WIND.trail) p.trail.shift();
      this._drawStreak(p.trail);
      p.life += 1;
    }

    _loop() {
      this.frame += 1;
      if (!this.enabled) {
        requestAnimationFrame(this._loop);
        return;
      }
      this.ctx.clearRect(0, 0, this.w, this.h);
      if (!this.map) this.map = findLeafletMap(this.canvas);
      const bounds = this.map?.getBounds();
      for (const p of this.particles) {
        this._step(p);
        if (p.geo && bounds && !bounds.contains([p.lat, p.lon])) {
          Object.assign(p, this._spawn(bounds));
        } else if (!p.geo && (p.x < -30 || p.x > this.w + 30 || p.y < -30 || p.y > this.h + 30)) {
          Object.assign(p, this._spawn(null));
        }
        if (p.life > 180) {
          Object.assign(p, this._spawn(bounds));
        }
      }
      requestAnimationFrame(this._loop);
    }
  }

  window.weatherMapParticles = {
    _field: null,
    init() {
      const canvas = document.querySelector('.map-wind-particles');
      if (!canvas) return;
      if (!this._field) this._field = new WindStreaks(canvas);
      else this._field._resize();
    },
    apply(opts) {
      if (!this._field) this.init();
      this._field?.apply(opts || {});
    },
    onMapMove() {
      if (!this._field?.enabled) return;
      this._field?.onMapMove();
    },
  };

  const boot = () => setTimeout(() => window.weatherMapParticles.init(), 400);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
"""
