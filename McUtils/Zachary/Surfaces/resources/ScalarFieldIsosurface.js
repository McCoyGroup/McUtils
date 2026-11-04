// Numerical counterpart of Zachary's table-based marching_cubes extractor.
// Tables and lossless scalar samples come from the Python ScalarField objects.
function createScalarFieldIsosurfaceEvaluator(data) {
    const fields = data.fields.map(field => {
        if (field.encoding !== 'float64-le-base64') throw new Error('Unsupported scalar field encoding');
        const bytes = Uint8Array.from(atob(field.values), c => c.charCodeAt(0));
        const view = new DataView(bytes.buffer);
        const values = new Float64Array(bytes.length / 8);
        for (let i = 0; i < values.length; i++) values[i] = view.getFloat64(i * 8, true);
        if (values.length !== field.shape.reduce((a, b) => a * b, 1)) throw new Error('Scalar grid size mismatch');
        return {...field, values};
    });
    const {corners, edges, triangles} = data.tables;
    const candidates = data.tracks.map(() => new Map());
    function activeCells(trackIndex, segment) {
        const cached = candidates[trackIndex];
        if (cached.has(segment)) return cached.get(segment);
        const track = data.tracks[trackIndex];
        const a = fields[track.fields[segment]], b = fields[track.fields[segment + 1]];
        const [nx, ny, nz] = a.shape, sy = nz, sx = ny * nz;
        const offsets = corners.map(c => c[0] * sx + c[1] * sy + c[2]);
        const cells = [];
        // A pointwise linear field/level blend cannot cross zero outside the
        // range bounded by these endpoint corner differences. This pruning
        // retains all possible intermediate cells, including new components.
        for (let x = 0; x < nx - 1; x++) for (let y = 0; y < ny - 1; y++) for (let z = 0; z < nz - 1; z++) {
            const base = x * sx + y * sy + z;
            let low = Infinity, high = -Infinity;
            for (const offset of offsets) {
                const v = a.values[base + offset] - track.isovalues[segment];
                const w = b.values[base + offset] - track.isovalues[segment + 1];
                low = Math.min(low, v, w); high = Math.max(high, v, w);
            }
            if (low < 0 && high >= 0) cells.push(base);
        }
        const result = {cells, offsets, sx, sy};
        cached.set(segment, result);
        return result;
    }
    function extract(trackIndex, segment, alpha) {
        const track = data.tracks[trackIndex];
        const a = fields[track.fields[segment]], b = fields[track.fields[segment + 1]];
        const iso = alpha === 0 ? track.isovalues[segment] : alpha === 1 ? track.isovalues[segment + 1]
            : (1 - alpha) * track.isovalues[segment] + alpha * track.isovalues[segment + 1];
        const {cells, offsets, sx, sy} = activeCells(trackIndex, segment);
        const vertices = [], faces = [], cache = new Map(), values = new Float64Array(8);
        const axes = a.axes, origin = a.origin, scale = track.coordinate_scale, matrix = track.transform;
        for (const base of cells) {
            let mask = 0;
            for (let corner = 0; corner < 8; corner++) {
                const index = base + offsets[corner];
                const v = alpha === 0 ? a.values[index] : alpha === 1 ? b.values[index]
                    : (1 - alpha) * a.values[index] + alpha * b.values[index];
                values[corner] = v;
                if (v < iso) mask |= 1 << corner;
            }
            if (mask === 0 || mask === 255) continue;
            const x = Math.floor(base / sx), y = Math.floor((base - x * sx) / sy), z = base % sy;
            function vertex(edge) {
                const key = base * 12 + edge;
                if (cache.has(key)) return cache.get(key);
                const [c0, c1] = edges[edge], p = corners[c0], q = corners[c1];
                const v = values[c0], w = values[c1];
                const t = Math.abs(w - v) < 1.e-10 ? .5 : (iso - v) / (w - v);
                const u = [x + p[0] + t * (q[0] - p[0]), y + p[1] + t * (q[1] - p[1]), z + p[2] + t * (q[2] - p[2])];
                const world = origin.map((o, j) => (o + u[0] * axes[0][j] + u[1] * axes[1][j] + u[2] * axes[2][j]) * scale);
                const transformed = matrix.slice(0, 3).map(row => row[3] + row[0] * world[0] + row[1] * world[1] + row[2] * world[2]);
                const index = vertices.length;
                vertices.push(transformed); cache.set(key, index);
                return index;
            }
            const row = triangles[mask];
            for (let i = 0; i < row.length && row[i] !== -1; i += 3) {
                const face = [vertex(row[i]), vertex(row[i + 1]), vertex(row[i + 2])];
                if (iso < 0) [face[0], face[1]] = [face[1], face[0]];
                if (track.reverse_winding) [face[1], face[2]] = [face[2], face[1]];
                faces.push(face);
            }
        }
        return {vertices, faces, isovalue: iso};
    }
    function evaluate(fraction) {
        if (!Number.isFinite(fraction) || fraction < 0 || fraction > 1) throw new RangeError('fraction must lie between zero and one');
        let segment = 0;
        while (segment + 1 < data.times.length - 1 && data.times[segment + 1] <= fraction) segment++;
        const alpha = (fraction - data.times[segment]) / (data.times[segment + 1] - data.times[segment]);
        return {fraction, segment, alpha, meshes: data.tracks.map((_, index) => extract(index, segment, alpha))};
    }
    return {evaluate};
}
