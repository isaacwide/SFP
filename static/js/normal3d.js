// a qui va ir las funciones para simumar una normal en 2 variables
function normal(n, mu, sigma) {
    let x = [];
    for (let i = 0; i < n; i++) {
        let u1 = Math.random();
        let u2 = Math.random();
        let z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
        x.push(z0 * sigma + mu);
    }
    return x;
}

document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("formulario");
    if (form) {
        form.addEventListener("submit", function(e) {
            e.preventDefault();

            const rho = parseFloat(document.getElementById('rho').value);
            const mu1 = parseFloat(document.getElementById('miu1').value);
            const mu2 = parseFloat(document.getElementById('miu2').value);
            const sigma1 = parseFloat(document.getElementById('sigma1').value);
            const sigma2 = parseFloat(document.getElementById('sigma2').value);
            const n = parseInt(document.getElementById('n').value);

            // Validar inputs
            if (isNaN(rho) || isNaN(mu1) || isNaN(mu2) || isNaN(sigma1) || isNaN(sigma2) || isNaN(n)) {
                alert("Por favor ingresa valores numéricos válidos");
                return;
            }

            // Generar normales estándar
            let z1 = normal(n, 0, 1);
            let z2 = normal(n, 0, 1);

            // Generar normales correlacionadas
            let x_vals = [];
            let y_vals = [];
            let z_vals = [];
            for (let i = 0; i < n; i++) {
                let x = mu1 + sigma1 * z1[i];
                let y = mu2 + sigma2 * (rho * z1[i] + Math.sqrt(1 - rho * rho) * z2[i]);
                x_vals.push(x);
                y_vals.push(y);
                z_vals.push(i); // Iteración como eje z
            }

            // Crear traza 3D
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
                }
            };

            // Configuración del layout
            let layout = {
                margin: { l: 0, r: 0, b: 0, t: 0 },
                scene: {
                    xaxis: { title: 'X' },
                    yaxis: { title: 'Y' },
                    zaxis: { title: 'Iteración' },
                    camera: {
                        eye: { x: 1.5, y: 1.5, z: 1.5 }
                    }
                }
            };

            // Dibujar gráfica
            Plotly.newPlot('grafica3d', [trace], layout);
        });
    }
});