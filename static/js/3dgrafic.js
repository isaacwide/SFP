function x_y(y) {
    let u = Math.random();
    const discriminant = 4 * (y*y + 3*y + 1 + u*(6*y + 8));
    return (-3*y - 2 + Math.sqrt(Math.max(0, discriminant))) / 2;
}

function y_x(x) {
    let u = Math.random();
    const base = x + 1;
    const discriminant = base*base + 3*u*(2*x + 5);
    return 2*(-base + Math.sqrt(Math.max(0, discriminant))) / 3;
}

function gebbs(n, x, y) {
    let x0 = x;
    let y0 = y;
    let samples = [[x0, y0]];

    for (let i = 0; i < n; i++) {
        let x_n = x_y(samples[i][1]);
        let y_n = y_x(samples[i][0]);
        samples.push([x_n, y_n]);
    }
    return samples;
}

// Funcion para calcular histograma 2D
function calculate2DHistogram(x, y, bins) {
    // Encontrar rangos
    const xMin = Math.min(...x);
    const xMax = Math.max(...x);
    const yMin = Math.min(...y);
    const yMax = Math.max(...y);
    
    // Calcular tamaño de bins
    const xBinSize = (xMax - xMin) / bins;
    const yBinSize = (yMax - yMin) / bins;
    
    // Inicializar matriz de conteo
    const counts = Array(bins).fill().map(() => Array(bins).fill(0));
    
    // Contar puntos en cada bin
    for (let i = 0; i < x.length; i++) {
        const xBin = Math.min(bins - 1, Math.floor((x[i] - xMin) / xBinSize));
        const yBin = Math.min(bins - 1, Math.floor((y[i] - yMin) / yBinSize));
        counts[xBin][yBin]++;
    }
    
    // Preparar datos para surface plot
    const xCenters = [];
    const yCenters = [];
    
    for (let i = 0; i < bins; i++) {
        xCenters.push(xMin + (i + 0.5) * xBinSize);
        yCenters.push(yMin + (i + 0.5) * yBinSize);
    }
    
    return {
        x: xCenters,
        y: yCenters,
        z: counts
    };
}

document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("formulario");
    if (form) {
        form.addEventListener("submit", function(e) {
            e.preventDefault();

            const x = Number(document.getElementById('x').value);
            const y = Number(document.getElementById('y').value);
            const n = Number(document.getElementById('n').value);

            // Validar inputs
            if (isNaN(x) || isNaN(y) || isNaN(n)) {
                alert("Por favor ingresa valores numericos validos");
                return;
            }

            // Calcular muestras
            let samples = gebbs(n, x, y);

            // Preparar datos para la grafica
            let x_vals = samples.map(p => p[0]);
            let y_vals = samples.map(p => p[1]);
            let z_vals = samples.map((p, i) => 0.5); // Iteracion como eje z

            // Crear traza 3D de dispersion
            let trace = {
                x: x_vals,
                y: y_vals,
                z: z_vals,
                mode: 'markers',
                type: 'scatter3d',
                marker: { 
                    size: 3, 
                    color: z_vals, 
                    colorscale: 'Viridis',
                    opacity: 0.8
                },
                name: 'Muestras Gibbs'
            };

            // Crear histograma 2D
            let hist2d = {
                x: x_vals,
                y: y_vals,
                type: "histogram2d",
                colorscale: "Viridis",
                name: 'Histograma 2D'
            };

            // Calcular histograma 3D
            const histogramData = calculate2DHistogram(x_vals, y_vals, 20);
            
            // Crear traza 3D para el histograma
            let histogram3DTrace = {
                x: histogramData.x,
                y: histogramData.y,
                z: histogramData.z,
                type: 'surface',
                colorscale: 'Viridis',
                opacity: 0.8,
                name: 'Histograma 3D'
            };

            // Configuracion del layout
            let layout = {
                margin: { l: 0, r: 0, b: 0, t: 0 },
                scene: {
                    xaxis: { title: 'X' },
                    yaxis: { title: 'Y' },
                    zaxis: { title: 'Iteracion' },
                    camera: {
                        eye: { x: 1.5, y: 1.5, z: 1.5 }
                    }
                }
            };

            // Almacenar trazas y layout para alternar entre ellas
            window.currentTraces = {
                scatter: trace,
                histogram3d: histogram3DTrace,
                histogram2d: hist2d
            };
            window.currentLayout = layout;

            // Dibujar grafica inicial (scatter3d)
            Plotly.newPlot('grafica3d', [trace], layout);
            Plotly.newPlot("histo3d", [hist2d]);
        });
    }
});